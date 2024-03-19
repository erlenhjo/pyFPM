from pyFPM.setup.Data import Data_patch
from pyFPM.setup.Setup_parameters import Setup_parameters
from pyFPM.setup.Imaging_system import LED_calibration_parameters

from skimage.filters import threshold_otsu
from skimage.feature import canny
import matplotlib.pyplot as plt
import numpy as np
import numba
from numba import njit
from numba.typed import List

def alternative_BFL(data: Data_patch, setup_parameters: Setup_parameters, 
                    assumed_calibration_parameters: LED_calibration_parameters):
    otsu_power = 1 # 1 means that the otsu threshold is based on amplitude, 2 on intensity, 4 on intesity^2
    canny_sigma = 10
    ransac_threshold = 5    

    edges_per_image, n_values, m_values = detect_edges_per_image(images = data.amplitude_images**otsu_power, 
                                                   canny_sigma = canny_sigma,
                                                   LED_indices = data.LED_indices, 
                                                   center_indices = setup_parameters.LED_info.center_indices)

    pixel_size = setup_parameters.camera.camera_pixel_size/setup_parameters.lens.magnification
    LED_pitch = setup_parameters.LED_info.LED_pitch
    NA = setup_parameters.lens.NA

    best_LED_distance, best_rotation, best_delta_x, best_delta_y \
          = optimize_bright_field_edge(edges_per_image=edges_per_image, n_values=n_values, m_values=m_values,
                                       pixel_size=pixel_size, NA=NA, LED_pitch=LED_pitch, ransac_threshold=ransac_threshold)

    print(best_LED_distance, best_rotation, best_delta_x, best_delta_y)

    centers_x, centers_y, radius = calculate_centers_and_radius(LED_n=n_values, LED_m=m_values,
                                                    LED_pitch=LED_pitch, NA=NA, pixel_size=pixel_size,
                                                    LED_distance=best_LED_distance, rotation=best_rotation,
                                                    delta_x=best_delta_x, delta_y=best_delta_y,
                                                    inverse_object_to_lens_distance=0) 
    
    fig, axes = plt.subplots(1,1)

    for edges, center_x, center_y in zip(edges_per_image, centers_x, centers_y):
        axes.scatter(edges[:,0],edges[:,1])
        circle = plt.Circle([center_x, center_y], radius, fill=False, color="r", linestyle="dashed")
        axes.add_patch(circle)
        axes.set_xlim(left=-setup_parameters.camera.raw_image_size[0]//2, right=setup_parameters.camera.raw_image_size[0]//2)
        axes.set_ylim(bottom=-setup_parameters.camera.raw_image_size[1]//2, top=setup_parameters.camera.raw_image_size[1]//2)

    plt.show()


    calibration_parameters = LED_calibration_parameters(LED_distance = best_LED_distance,
                                                        LED_x_offset = best_delta_x,
                                                        LED_y_offset = best_delta_y,
                                                        LED_rotation = best_rotation
                                                        )

    return calibration_parameters


def detect_edges_per_image(images, canny_sigma, LED_indices, center_indices):
    n_values = []
    m_values = []
    edges_per_image = List()

    image_center = np.flip(images[0].shape) // 2 

    threshold = threshold_otsu(images)

    for image, image_indices in zip(images, np.array(LED_indices)):
        binary = (image <= threshold)
        edge_image = canny(binary, sigma=canny_sigma)
        edge_points = np.flip(np.transpose(edge_image.nonzero()), axis=1) # points as an array of (x,y)
        
        if edge_points.shape[0]==0:
            continue
        n, m = image_indices - center_indices
        n_values.append(n)
        m_values.append(m)
        edges_per_image.append(edge_points-image_center)

    return edges_per_image, np.array(n_values), np.array(m_values)

@njit(cache = True, parallel = True)
def optimize_bright_field_edge(edges_per_image, n_values, m_values,  
                               pixel_size, NA, LED_pitch, 
                               ransac_threshold, inverse_object_to_lens_distance=0):
    best_score = -1
    best_LED_distance = 0
    best_rotation = 0
    best_delta_x = 0
    best_delta_y = 0

    LED_distance_values = np.linspace(start=0.195, stop=0.205, num=20)
    rotation_values = np.linspace(start=-1, stop=1, num=10)
    delta_x_values = np.linspace(start=-100e-6, stop=100e-6, num=10)
    delta_y_values = np.linspace(start=-100e-6, stop=100e-6, num=10)

    for LED_distance in LED_distance_values:
        for rotation in rotation_values:
            for delta_x in delta_x_values:
                for delta_y in delta_y_values:

                    centers_x, centers_y, radius = calculate_centers_and_radius(LED_n=n_values, LED_m=m_values,
                                                                   LED_pitch=LED_pitch, NA=NA, pixel_size=pixel_size,
                                                                   LED_distance=LED_distance, rotation=rotation,
                                                                   delta_x=delta_x, delta_y=delta_y,
                                                                   inverse_object_to_lens_distance=inverse_object_to_lens_distance) 
                    

                    score = evaluate_circle_score_RANSAC(edges_per_image, centers_x, centers_y, radius, ransac_threshold)
                    if score > best_score:
                        best_score = score
                        best_LED_distance = LED_distance
                        best_rotation = rotation
                        best_delta_x = delta_x
                        best_delta_y = delta_y


    return best_LED_distance, best_rotation, best_delta_x, best_delta_y






@njit(cache=True)
def evaluate_circle_score_RANSAC(edges_per_image, centers_x_per_image, centers_y_per_image, radius, threshold):
    score = 0
    for edges, center_x, center_y in zip(edges_per_image, centers_x_per_image, centers_y_per_image):
        distance_from_center = np.sqrt((edges[:,0]-center_x)**2 + (edges[:,1]-center_y)**2)
        score += np.sum(np.abs(distance_from_center-radius)<threshold)
    return score

@njit(cache=True)
def calculate_centers_and_radius(LED_n, LED_m, LED_pitch, NA, pixel_size,
                                 rotation, delta_x, delta_y, LED_distance,
                                 inverse_object_to_lens_distance):
    rotation = rotation * np.pi/180
    radius = NA / pixel_size / (1/LED_distance + inverse_object_to_lens_distance)
    centers_x = (LED_pitch*LED_n*np.cos(rotation) - LED_pitch*LED_m*np.sin(rotation) + delta_x)\
                /pixel_size / (1+LED_distance*inverse_object_to_lens_distance)
    centers_y = (LED_pitch*LED_n*np.sin(rotation) + LED_pitch*LED_m*np.cos(rotation) + delta_y)\
                /pixel_size / (1+LED_distance*inverse_object_to_lens_distance)
    
    return centers_x, centers_y, radius