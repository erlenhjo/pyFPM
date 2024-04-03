from pyFPM.setup.Data import Data_patch
from pyFPM.setup.Setup_parameters import Setup_parameters
from pyFPM.setup.Imaging_system import LED_calibration_parameters
from pyFPM.recovery.calibration.edge_detection import detect_edges_per_image
from pyFPM.recovery.calibration.non_linear_BFL import (get_centers_and_radii_function, 
                                                       calculate_centers_and_radii, 
                                                       evaluate_circle_score_non_linear,
                                                       plot_bright_field_images_with_BF_edge)

from typing import List
import matplotlib.pyplot as plt
import numpy as np
from dataclasses import dataclass
from scipy.optimize import minimize

@dataclass
class Calibration_parameters_plus:
    delta_x: float
    delta_y: float
    LED_distance: float
    alpha: float
    beta: float
    gamma: float
    numerical_aperture: float
    inverse_object_to_lens_distance: float


def series_non_linear_BFL(data_patches: List[Data_patch], setup_parameters: Setup_parameters, 
                         assumed_calibration_parameters: LED_calibration_parameters,
                         relative_LED_distances):
    
    pixel_size = setup_parameters.camera.camera_pixel_size/setup_parameters.lens.magnification
    LED_pitch = setup_parameters.LED_info.LED_pitch

    assumed_calibration_parameters = \
        Calibration_parameters_plus(
            delta_x = assumed_calibration_parameters.LED_x_offset,
            delta_y = assumed_calibration_parameters.LED_y_offset,
            LED_distance = assumed_calibration_parameters.LED_distance,
            alpha = 0,
            beta = 0,
            gamma = 0,
            numerical_aperture = setup_parameters.lens.NA,
            inverse_object_to_lens_distance = 0
        )


    otsu_power = 4 # 1 means that the otsu threshold is based on amplitude, 2 on intensity, 4 on intesity^2
    canny_sigma = 10

    all_optimal_calibration_parameters: List[Calibration_parameters_plus] = []
    
    for data in data_patches:
        edges_per_image, n_values, m_values = detect_edges_per_image(
                                                    images = data.amplitude_images**otsu_power, 
                                                    canny_sigma = canny_sigma,
                                                    LED_indices = data.LED_indices, 
                                                    center_indices = setup_parameters.LED_info.center_indices,
                                                    downsample_image = 4,
                                                    downsample_edges = 10)



        optimal_calibration_parameters: Calibration_parameters_plus \
            = optimize_bright_field_edge(edges_per_image = edges_per_image,
                                        n_values = n_values, m_values = m_values,
                                        pixel_size = pixel_size, LED_pitch = LED_pitch,
                                        assumed_parameters = assumed_calibration_parameters)

        all_optimal_calibration_parameters.append(optimal_calibration_parameters)
        print(optimal_calibration_parameters)

        centers_x, centers_y, radii = calculate_centers_and_radii(LED_n = n_values, 
                                                                LED_m = m_values,
                                                                LED_pitch = LED_pitch,
                                                                pixel_size = pixel_size,
                                                                inverse_object_to_lens_distance\
                                                                = optimal_calibration_parameters.inverse_object_to_lens_distance,
                                                                numerical_aperture = optimal_calibration_parameters.numerical_aperture, 
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
                                                    inverse_object_to_lens_distance = optimal_calibration_parameters.inverse_object_to_lens_distance,
                                                    numerical_aperture = optimal_calibration_parameters.numerical_aperture, 
                                                    array_size = int(np.sqrt(len(data.LED_indices))))

        plt.show()

    fig, axes = plt.subplots(2,4)
    axes: List[plt.Axes] = axes.flatten()
    axes[0].set_title("Delta x")
    axes[1].set_title("Delta y")
    axes[2].set_title("LED distance")
    axes[3].set_title("Alpha")
    axes[4].set_title("Beta")
    axes[5].set_title("Gamma")
    axes[6].set_title("Numerical aperture")
    axes[7].set_title("Inverse object to lens distance")

    for n, parameters in enumerate(all_optimal_calibration_parameters):
        
        axes[0].scatter(relative_LED_distances[n], parameters.delta_x)
        axes[1].scatter(relative_LED_distances[n], parameters.delta_y)
        axes[2].scatter(relative_LED_distances[n], parameters.LED_distance)
        axes[3].scatter(relative_LED_distances[n], parameters.alpha)
        axes[4].scatter(relative_LED_distances[n], parameters.beta)
        axes[5].scatter(relative_LED_distances[n], parameters.gamma)
        axes[6].scatter(relative_LED_distances[n], parameters.numerical_aperture)
        axes[7].scatter(relative_LED_distances[n], parameters.inverse_object_to_lens_distance)

    plt.show()



def optimize_bright_field_edge(edges_per_image, n_values, m_values,
                               LED_pitch, pixel_size,
                               assumed_parameters: Calibration_parameters_plus):
    initialization = [
        assumed_parameters.numerical_aperture,
        assumed_parameters.inverse_object_to_lens_distance,
        assumed_parameters.alpha,
        assumed_parameters.beta,
        assumed_parameters.gamma,
        assumed_parameters.delta_x,
        assumed_parameters.delta_y,
        assumed_parameters.LED_distance
    ]

    error_function = get_error_function(edges_per_image = edges_per_image,
                                        LED_n = n_values,
                                        LED_m = m_values,
                                        LED_pitch = LED_pitch,
                                        pixel_size = pixel_size)
    
    results = minimize(error_function, x0=initialization, method="Powell")

    numerical_aperture, inverse_object_to_lens_distance = results.x[0], results.x[1]
    alpha, beta, gamma = results.x[2], results.x[3], results.x[4]
    delta_x, delta_y, LED_distance = results.x[5], results.x[6], results.x[7] 



    return Calibration_parameters_plus(
        delta_x=delta_x,
        delta_y=delta_y,
        LED_distance=LED_distance,
        alpha=alpha,
        beta=beta,
        gamma=gamma,
        numerical_aperture=numerical_aperture,
        inverse_object_to_lens_distance=inverse_object_to_lens_distance
    )




def get_error_function(edges_per_image,
                       LED_n, LED_m, LED_pitch, pixel_size):
    center_and_radii_function = get_centers_and_radii_function(LED_n = LED_n,
                                                               LED_m = LED_m,
                                                               LED_pitch = LED_pitch,
                                                               pixel_size = pixel_size
                                                               )
    def simplified_error_function(args):
        numerical_aperture, inverse_object_to_lens_distance = args[0], args[1]
        alpha, beta, gamma = args[2], args[3], args[4]
        delta_x, delta_y, LED_distance = args[5], args[6], args[7]
            
        centers_x, centers_y, radii = center_and_radii_function(
            delta_x = delta_x, delta_y = delta_y, 
            LED_distance = LED_distance,
            alpha = alpha, beta = beta, gamma = gamma,
            inverse_object_to_lens_distance\
                = inverse_object_to_lens_distance,
            numerical_aperture = numerical_aperture 
        )
        return evaluate_circle_score_non_linear(edges_per_image = edges_per_image, 
                                                    centers_x_per_image = centers_x,
                                                    centers_y_per_image = centers_y, 
                                                    radius_per_image = radii)

    return simplified_error_function



