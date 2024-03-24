from pyFPM.setup.Data import Data_patch
from pyFPM.setup.Setup_parameters import Setup_parameters
from pyFPM.setup.Imaging_system import LED_calibration_parameters
from pyFPM.recovery.calibration.edge_detection import detect_edges_per_image


import matplotlib.pyplot as plt
import numpy as np
from dataclasses import dataclass
from scipy.optimize import minimize

@dataclass
class Calibration_parameters:
    delta_x: float
    delta_y: float
    LED_distance: float
    alpha: float
    beta: float
    gamma: float

def non_linear_BFL(data: Data_patch, setup_parameters: Setup_parameters, 
                    assumed_calibration_parameters: LED_calibration_parameters):
    otsu_power = 4 # 1 means that the otsu threshold is based on amplitude, 2 on intensity, 4 on intesity^2
    canny_sigma = 15
 
    edges_per_image, n_values, m_values = detect_edges_per_image(
                                                   images = data.amplitude_images**otsu_power, 
                                                   canny_sigma = canny_sigma,
                                                   LED_indices = data.LED_indices, 
                                                   center_indices = setup_parameters.LED_info.center_indices,
                                                   downsample_image = 1,
                                                   downsample_edges = 100)

    pixel_size = setup_parameters.camera.camera_pixel_size/setup_parameters.lens.magnification
    LED_pitch = setup_parameters.LED_info.LED_pitch
    inverse_object_to_lens_distance = 0
    numerical_aperture = setup_parameters.lens.NA

    assumed_calibration_parameters = \
        Calibration_parameters(
            delta_x = assumed_calibration_parameters.LED_x_offset,
            delta_y = assumed_calibration_parameters.LED_y_offset,
            LED_distance = assumed_calibration_parameters.LED_distance,
            alpha = 0,
            beta = 0,
            gamma = 0
        ) 

    optimal_calibration_parameters: Calibration_parameters \
          = optimize_bright_field_edge(edges_per_image = edges_per_image, 
                                       n_values = n_values, m_values = m_values,
                                       pixel_size = pixel_size, LED_pitch = LED_pitch,
                                       inverse_object_to_lens_distance=inverse_object_to_lens_distance,
                                       numerical_aperture = numerical_aperture, 
                                       assumed_parameters = assumed_calibration_parameters)

    print(optimal_calibration_parameters)

    centers_x, centers_y, radii = calculate_centers_and_radii(LED_n = n_values, 
                                                              LED_m = m_values,
                                                              LED_pitch = LED_pitch,
                                                              pixel_size = pixel_size,
                                                              inverse_object_to_lens_distance\
                                                                = inverse_object_to_lens_distance,
                                                              numerical_aperture = numerical_aperture,
                                                              delta_x = optimal_calibration_parameters.delta_x, 
                                                              delta_y = optimal_calibration_parameters.delta_y,
                                                              LED_distance = optimal_calibration_parameters.LED_distance, 
                                                              alpha = optimal_calibration_parameters.alpha, 
                                                              beta = optimal_calibration_parameters.beta,
                                                              gamma = optimal_calibration_parameters.gamma
                                                              ) 
    
    fig, axes = plt.subplots(1,1)

    for edges, center_x, center_y, radius in zip(edges_per_image, centers_x, centers_y, radii):
        axes.scatter(edges[:,0],edges[:,1])
        circle = plt.Circle([center_x, center_y], radius, fill=False, color="r", linestyle="dashed")
        axes.add_patch(circle)
        axes.set_xlim(left=-setup_parameters.camera.raw_image_size[0]//2, right=setup_parameters.camera.raw_image_size[0]//2)
        axes.set_ylim(bottom=-setup_parameters.camera.raw_image_size[1]//2, top=setup_parameters.camera.raw_image_size[1]//2)

    fig = plot_bright_field_images_with_BF_edge(data_patch = data, 
                                                setup_parameters = setup_parameters, 
                                                calibration_parameters = optimal_calibration_parameters,
                                                inverse_object_to_lens_distance = inverse_object_to_lens_distance,
                                                numerical_aperture = numerical_aperture, 
                                                array_size = 5)

    plt.show()

    return optimal_calibration_parameters 


def optimize_bright_field_edge(edges_per_image, n_values, m_values,
                               LED_pitch, pixel_size,
                               inverse_object_to_lens_distance, 
                               numerical_aperture,
                               assumed_parameters: Calibration_parameters):
    initalization = [
        assumed_parameters.delta_x,
        assumed_parameters.delta_y,
        assumed_parameters.LED_distance,
        assumed_parameters.alpha,
        assumed_parameters.beta,
        assumed_parameters.gamma
    ]
    error_function = get_error_function(edges = edges_per_image,
                                        LED_n = n_values,
                                        LED_m = m_values,
                                        LED_pitch = LED_pitch,
                                        pixel_size = pixel_size,
                                        inverse_object_to_lens_distance = inverse_object_to_lens_distance,
                                        numerical_aperture = numerical_aperture
                                        )
    
    results = minimize(error_function, x0=initalization, method="Nelder-Mead")

    print(results.x)
    print(results.success)
    print(results.status)
    print(results.message)
    print(results.nit)





    delta_x, delta_y, LED_distance,\
        alpha, beta, gamma = results.x

    optimized_parameters = Calibration_parameters(
        delta_x = delta_x,
        delta_y = delta_y,
        LED_distance = LED_distance,
        alpha = alpha,
        beta = beta,
        gamma = gamma  
    )

    return optimized_parameters



def evaluate_circle_score_non_linear(edges_per_image, centers_x_per_image,
                                    centers_y_per_image, radius_per_image):
    score = 0
    for edges, center_x, center_y, radius in zip(edges_per_image, centers_x_per_image, centers_y_per_image, radius_per_image):
        distance_from_center = np.sqrt((edges[:,0]-center_x)**2 + (edges[:,1]-center_y)**2)
        score += np.sum(np.abs(distance_from_center-radius))/len(distance_from_center)
    return score



def calculate_centers_and_radii(LED_n, LED_m, LED_pitch, pixel_size,
                                inverse_object_to_lens_distance,
                                numerical_aperture,
                                delta_x, delta_y, LED_distance,
                                alpha, beta, gamma
                                 ):
    r_xx = np.cos(alpha)*np.cos(beta)
    r_xy = np.cos(alpha)*np.sin(beta)*np.sin(gamma) - np.sin(alpha)*np.cos(gamma)
    r_yx = np.sin(alpha)*np.cos(beta)
    r_yy = np.sin(alpha)*np.sin(beta)*np.sin(gamma) + np.cos(alpha)*np.cos(gamma)
    r_zx = -np.sin(beta)
    r_zy = np.cos(beta)*np.sin(gamma)

    LEDs_x = LED_pitch*LED_n*r_xx + LED_pitch*LED_m*r_xy
    LEDs_y = LED_pitch*LED_n*r_yx + LED_pitch*LED_m*r_yy
    LEDs_z = LED_pitch*LED_n*r_zx + LED_pitch*LED_m*r_zy
    LED_distances = LED_distance + LEDs_z


    radii = numerical_aperture / pixel_size / (1/LED_distances + inverse_object_to_lens_distance)
    centers_x = (LEDs_x + delta_x) / pixel_size \
                / (1+LED_distances*inverse_object_to_lens_distance)
    centers_y = (LEDs_y + delta_y) / pixel_size \
                / (1+LED_distances*inverse_object_to_lens_distance)
    
    return centers_x, centers_y, radii


def get_centers_and_radii_function(LED_n, LED_m, LED_pitch, pixel_size):
    def simplified_center_and_radii_function(delta_x, delta_y, LED_distance,
                                             alpha, beta, gamma,
                                             inverse_object_to_lens_distance,
                                             numerical_aperture
                                             ):
        return calculate_centers_and_radii(
                                LED_n = LED_n, LED_m = LED_m, 
                                LED_pitch = LED_pitch, pixel_size = pixel_size,
                                inverse_object_to_lens_distance\
                                    = inverse_object_to_lens_distance,
                                numerical_aperture = numerical_aperture,
                                delta_x = delta_x, delta_y = delta_y, 
                                LED_distance = LED_distance,
                                alpha = alpha, beta = beta, gamma = gamma
                                )

    return simplified_center_and_radii_function

def get_error_function(edges, LED_n, LED_m, LED_pitch, pixel_size, 
                       inverse_object_to_lens_distance, numerical_aperture):
    center_and_radii_function = get_centers_and_radii_function(LED_n = LED_n,
                                                               LED_m = LED_m,
                                                               LED_pitch = LED_pitch,
                                                               pixel_size = pixel_size
                                                               )
    def simplified_error_function(args):
        delta_x, delta_y, LED_distance,\
            alpha, beta, gamma = args
        centers_x, centers_y, radii = center_and_radii_function(
            delta_x = delta_x, delta_y = delta_y,
            LED_distance = LED_distance,
            alpha = alpha, beta = beta, gamma = gamma,
            inverse_object_to_lens_distance\
             = inverse_object_to_lens_distance,
            numerical_aperture = numerical_aperture
        )
        return evaluate_circle_score_non_linear(edges_per_image = edges, 
                                                centers_x_per_image = centers_x,
                                                centers_y_per_image = centers_y, 
                                                radius_per_image = radii)
    return simplified_error_function








def plot_bright_field_images_with_BF_edge(data_patch: Data_patch, setup_parameters: Setup_parameters, 
                                          calibration_parameters: LED_calibration_parameters,
                                          inverse_object_to_lens_distance, numerical_aperture, 
                                          array_size: int):
    LED_indices = data_patch.LED_indices

    center_indices = setup_parameters.LED_info.center_indices
    center_x = center_indices[0]
    center_y = center_indices[1]
    y_min = center_y - array_size//2
    x_min = center_x - array_size//2
    y_max = y_min + array_size
    x_max = x_min + array_size

    max_intensity = np.max(data_patch.amplitude_images)**2

    fig, axes = plt.subplots(nrows=array_size, ncols=array_size, figsize=(7,7), constrained_layout = True)

    mean_values = np.empty(shape=(array_size,array_size))

    for image_nr, indices in enumerate(LED_indices):
        x,y = indices
        if x>=x_min and x<x_max and y>=y_min and y<y_max:
            m = y_max-y-1
            n = x_max-x-1
            LED_n = x - center_x
            LED_m = y - center_y

            axes[m,n].matshow(data_patch.amplitude_images[image_nr]**2, vmin=0, vmax=max_intensity)
            axes[m,n].axis("off")
            mean_values[m,n] = np.mean(data_patch.amplitude_images[image_nr]**2)

            center, radius = calculate_BF_edge_circle(setup_parameters=setup_parameters,
                                                     calibration_parameters=calibration_parameters,
                                                     inverse_object_to_lens_distance=inverse_object_to_lens_distance,
                                                     numerical_aperture=numerical_aperture,
                                                     LED_n=LED_n, LED_m=LED_m)
            circle = plt.Circle(center, radius, fill=False, color="r", linestyle="dashed")
            axes[m,n].add_patch(circle)
            
    return fig

def calculate_BF_edge_circle(setup_parameters: Setup_parameters, 
                      calibration_parameters: Calibration_parameters,
                      inverse_object_to_lens_distance, numerical_aperture,
                      LED_n, LED_m):
    pixel_size = setup_parameters.camera.camera_pixel_size/setup_parameters.lens.magnification
    LED_pitch = setup_parameters.LED_info.LED_pitch
    image_center_x = setup_parameters.camera.raw_image_size[0] // 2
    image_center_y = setup_parameters.camera.raw_image_size[1] // 2
    
    center_x, center_y, radius = calculate_centers_and_radii(
        LED_n = LED_n,
        LED_m = LED_m,
        LED_pitch = LED_pitch,
        pixel_size = pixel_size,
        delta_x = calibration_parameters.delta_x,
        delta_y = calibration_parameters.delta_y,
        LED_distance = calibration_parameters.LED_distance,
        inverse_object_to_lens_distance = inverse_object_to_lens_distance,
        numerical_aperture = numerical_aperture,
        alpha = calibration_parameters.alpha,
        beta = calibration_parameters.beta,
        gamma = calibration_parameters.gamma
    ) 

    
    return (center_x + image_center_x, center_y + image_center_y), radius