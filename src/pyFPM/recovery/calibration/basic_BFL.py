from pyFPM.setup.Data import Data_patch
from pyFPM.setup.Setup_parameters import Setup_parameters
from pyFPM.setup.Imaging_system import LED_calibration_parameters

from skimage.filters import threshold_otsu
from skimage.feature import canny
import matplotlib.pyplot as plt
import numpy as np


from pyFPM.setup.Data import Data_patch
from pyFPM.setup.Setup_parameters import Setup_parameters
from pyFPM.setup.Imaging_system import LED_calibration_parameters

from skimage.filters import threshold_otsu, threshold_multiotsu
from skimage.feature import canny
import matplotlib.pyplot as plt
import numpy as np
import numba
from numba import njit
from numba.typed import List

def basic_BFL(data: Data_patch, setup_parameters: Setup_parameters):
    otsu_power = 4 # 1 means that the otsu threshold is based on amplitude, 2 on intensity, 4 on intesity^2
    canny_sigma = 10
    ransac_threshold_pix = 10 #pixels
    downsample_image = 4
    downsample_edges = 4

    edges_per_image, n_values, m_values = detect_edges_per_image(images = data.amplitude_images**otsu_power, 
                                                   canny_sigma = canny_sigma,
                                                   LED_indices = data.LED_indices, 
                                                   center_indices = setup_parameters.LED_info.center_indices,
                                                   downsample_image = downsample_image,
                                                   downsample_edges= downsample_edges)

    pixel_size = setup_parameters.camera.camera_pixel_size/setup_parameters.lens.magnification
    LED_pitch = setup_parameters.LED_info.LED_pitch
    NA = setup_parameters.lens.NA

    best_distance_ratio, best_rotation, best_radius, best_delta_x, best_delta_y \
          = optimize_bright_field_edge(edges_per_image=edges_per_image, n_values=n_values, m_values=m_values,
                                       pixel_size=pixel_size, LED_pitch=LED_pitch, ransac_threshold_pix=ransac_threshold_pix)

    best_LED_distance = best_radius/NA*(1+best_distance_ratio)*pixel_size

    print(best_distance_ratio)

    calibration_parameters = LED_calibration_parameters(LED_distance = best_LED_distance,
                                                        LED_x_offset = best_delta_x*pixel_size,
                                                        LED_y_offset = best_delta_y*pixel_size,
                                                        LED_rotation = best_rotation
                                                        )

    return calibration_parameters


def detect_edges_per_image(images, canny_sigma, LED_indices, center_indices, downsample_image: int, downsample_edges: int):
    n_values = []
    m_values = []
    edges_per_image = List()

    images = images[:,::downsample_image, ::downsample_image]

    image_center = np.flip(images[0].shape) // 2
    threshold = threshold_otsu(images)

    for image, image_indices in zip(images, np.array(LED_indices)):
        binary = (image <= threshold)
        edge_image = canny(binary, sigma=canny_sigma)
        edge_points = np.flip(np.transpose(edge_image.nonzero()), axis=1) # points as an array of (x,y)

        fig, axes = plt.subplots()
        axes.matshow(image)
        axes.scatter(edge_points[:,0], edge_points[:,1])
        plt.show()
        
        if edge_points.shape[0]==0:
            continue
        n, m = image_indices - center_indices
        n_values.append(n)
        m_values.append(m)
        edges_per_image.append(((edge_points-image_center)*downsample_image)[::downsample_edges,:])

    

    return edges_per_image, np.array(n_values), np.array(m_values)


def optimize_bright_field_edge(edges_per_image, n_values, m_values,  
                               pixel_size, LED_pitch, ransac_threshold_pix):
    best_score = -1
    best_distance_ratio = 0
    best_rotation = 0
    best_radius = 0
    best_delta_x = 0
    best_delta_y = 0

    rng_gen = np.random.default_rng()

    distance_ratios = [0]# np.linspace(start=1.7, stop=2.2, num=100)
    rotation_values = np.linspace(start=-3, stop=3, num=60)

    for distance_ratio in distance_ratios:
        for rotation in rotation_values:
            shifts = calculate_shifts(LED_n=n_values, LED_m=m_values,
                                      LED_pitch=LED_pitch, pixel_size=pixel_size,
                                      rotation=rotation, distance_ratio=distance_ratio)

            shifted_edges = np.array([edge - shift for (edges, shift) in zip(edges_per_image, shifts) for edge in edges])

            for n in range(100):
                (x1,y1),(x2,y2),(x3,y3) = rng_gen.choice(shifted_edges, size=3, replace=False)
                center, radius = circle_from_three_points(x1,y1,x2,y2,x3,y3)

                distances_from_center = np.linalg.norm(shifted_edges-center, axis=1) #np.sqrt((shifted_edges[:,:,0]-center[0])**2 + (shifted_edges[:,:,1]-center[1])**2)
                score = np.sum(np.abs(distances_from_center-radius) < ransac_threshold_pix)
                
                if score > best_score:
                    best_score = score
                    best_distance_ratio = distance_ratio
                    best_rotation = rotation            
                    best_radius = radius
                    best_delta_x = center[0]
                    best_delta_y = center[1]

    # plot best result
    shifts = calculate_shifts(LED_n=n_values, LED_m=m_values,
                            LED_pitch=LED_pitch, pixel_size=pixel_size,
                            rotation=best_rotation, distance_ratio=best_distance_ratio)

    shifted_edges = np.array([edge - shift for (edges, shift) in zip(edges_per_image, shifts) for edge in edges])

    center = np.array([best_delta_x, best_delta_y])
    distances_from_center = np.linalg.norm(shifted_edges-center, axis=1) #np.sqrt((shifted_edges[:,0]-center[0])**2 + (shifted_edges[:,1]-center[1])**2)


    hits = shifted_edges[np.where(np.abs(distances_from_center-best_radius) < ransac_threshold_pix)]
    misses = shifted_edges[np.where(np.abs(distances_from_center-best_radius) > ransac_threshold_pix)]

    fig,axes = plt.subplots(1,1)
    axes.scatter(hits[:,0],hits[:,1], color= "g", s=1, edgecolors=None)
    axes.scatter(misses[:,0],misses[:,1], color = "r", s=1, edgecolors=None)
    circle = plt.Circle([best_delta_x, best_delta_y], best_radius, fill=False, color="b", linestyle="dashed")
    axes.add_patch(circle)




    return best_distance_ratio, best_rotation, best_radius, best_delta_x, best_delta_y


def calculate_shifts(LED_n, LED_m, LED_pitch, pixel_size,
                     rotation, distance_ratio):
    rotation = rotation * np.pi/180
    shifts_x = (LED_pitch*LED_n*np.cos(rotation) - LED_pitch*LED_m*np.sin(rotation))\
                /pixel_size / (1+distance_ratio)
    shifts_y = (LED_pitch*LED_n*np.sin(rotation) + LED_pitch*LED_m*np.cos(rotation))\
                /pixel_size / (1+distance_ratio)
    
    return np.array([shifts_x, shifts_y]).transpose()


# based on answer by Scott at
# https://math.stackexchange.com/questions/213658/get-the-equation-of-a-circle-when-given-3-points
    
def circle_from_three_points(x1, y1, x2, y2, x3, y3):
    z1 = complex(x1,y1)
    z2 = complex(x2,y2)
    z3 = complex(x3,y3)

    try:
        w = (z3 - z1)/(z2 - z1)     
        c = (z2 - z1)*(w - abs(w)**2)/(2j*w.imag) + z1
        r = abs(z1 - c)
    except Exception as e:
        return np.array([0, 0]), 0



    return np.array([c.real, c.imag]), r
