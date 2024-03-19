from pyFPM.setup.Data import Data_patch
from pyFPM.setup.Setup_parameters import Setup_parameters
from pyFPM.setup.Imaging_system import LED_calibration_parameters

from skimage.filters import threshold_otsu
from skimage.feature import canny
import matplotlib.pyplot as plt
import numpy as np

def bright_field_localization(data: Data_patch, setup_parameters: Setup_parameters):
    otsu_power = 2
    canny_sigma = 10
    ransac_threshold = 1

    n_and_m_values = get_n_and_m_values(LED_indices=data.LED_indices, center_indices=setup_parameters.LED_info.center_indices)
    edges_per_image = detect_edges(data.amplitude_images**otsu_power, canny_sigma)

    pixel_size = setup_parameters.camera.camera_pixel_size/setup_parameters.lens.magnification
    LED_pitch = setup_parameters.LED_info.LED_pitch
    NA = setup_parameters.lens.NA

    bright_field_regions = find_bright_field_circles(edges_per_image, data.amplitude_images, ransac_threshold,
                                                     pixel_size=pixel_size, NA=NA)

    optimal_LED_distance = 0
    optimal_delta_x = 0
    optimal_delta_y = 0
    optimal_rotation = 0

    return LED_calibration_parameters(optimal_LED_distance, optimal_delta_x, optimal_delta_y, optimal_rotation)

def get_n_and_m_values(LED_indices, center_indices):
    return np.array(LED_indices) - np.array(center_indices)   

def detect_edges(images, canny_sigma):
    all_edges = []
    threshold = threshold_otsu(images)
    for image in images:
        binary = (image <= threshold)
        edge_image = canny(binary, sigma=canny_sigma)
        edge_points = np.flip(np.transpose(edge_image.nonzero()), axis=1) # points as an array of (x,y)
        all_edges.append(edge_points)

    return all_edges

def find_bright_field_circles(edges_per_image, images, ransac_threshold, pixel_size, NA):
    circle_centers = []
    circle_radii = []
    rng_gen = np.random.default_rng()
    
    fig2, axes2 = plt.subplots(1,1)
    axes2.grid(visible=True)
    fig3, axes3 = plt.subplots(1,1)

    for edge_points, image in zip(edges_per_image,images):
        if edge_points.shape[0]==0:
            circle_centers.append([0,0]) # no located circle
            circle_radii.append(0)
            continue

        center, radius = fit_circle_RANSAC(edge_points, rng_gen=rng_gen, ransac_threshold=ransac_threshold)
        
        if radius < 10000:
            fig, axes = plt.subplots(1,1)
            axes.scatter(edge_points[:,0],edge_points[:,1])
            axes.matshow(image)
            circle = plt.Circle(center, radius, fill=False, color="r", linestyle="dashed")
            axes.add_patch(circle)
            fig.suptitle(radius)
            axes2.scatter((center[0]-image.shape[1]//2)*pixel_size,(center[1]-image.shape[0]//2)*pixel_size)
            axes3.scatter(radius*pixel_size/NA,radius*pixel_size/NA)

        circle_centers.append(center)
        circle_radii.append(radius)

    print(circle_radii)
    plt.show()

    return circle_centers, circle_radii




def fit_circle_RANSAC(edge_points, rng_gen: np.random.Generator, ransac_threshold, iterations=100):
    indices = np.arange(edge_points.shape[0])
    best_center, best_radius, best_score = [0,0], 0, 0
    for n in range(iterations):
        (x1,y1),(x2,y2),(x3,y3) = rng_gen.choice(edge_points, size=3, replace=False)
        center, radius = circle_from_three_points(x1,y1,x2,y2,x3,y3)
        score = RANSAC_score_function(edges=edge_points, center=center,
                                      radius=radius, threshold=ransac_threshold)
        

        if score > best_score:
            best_center = center
            best_radius = radius
            best_score = score

    return best_center, best_radius

def RANSAC_score_function(edges, center, radius, threshold):
    distance_from_center = np.linalg.norm(edges-center, axis=1)
    return np.sum(np.abs(distance_from_center-radius)<threshold)

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
