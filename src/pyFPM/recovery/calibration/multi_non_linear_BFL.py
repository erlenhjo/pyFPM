from pyFPM.setup.Data import Data_patch
from pyFPM.setup.Setup_parameters import Setup_parameters
from pyFPM.setup.Imaging_system import LED_calibration_parameters
from pyFPM.recovery.calibration.edge_detection import detect_edges_per_image
from pyFPM.recovery.calibration.non_linear_BFL import (get_centers_and_radii_function, 
                                                       calculate_centers_and_radii, 
                                                       evaluate_circle_score_non_linear,
                                                       Calibration_parameters,
                                                       plot_bright_field_images_with_BF_edge)

from typing import List
import matplotlib.pyplot as plt
import numpy as np
from dataclasses import dataclass
from scipy.optimize import minimize


def multi_non_linear_BFL(data_patches: List[Data_patch], setup_parameters: Setup_parameters, 
                         assumed_calibration_parameters: LED_calibration_parameters,
                         relative_LED_distances):
    otsu_power = 4 # 1 means that the otsu threshold is based on amplitude, 2 on intensity, 4 on intesity^2
    canny_sigma = 10
    
    edges_per_image_per_dataset = []
    for data in data_patches:
        edges_per_image, n_values, m_values = detect_edges_per_image(
                                                    images = data.amplitude_images**otsu_power, 
                                                    canny_sigma = canny_sigma,
                                                    LED_indices = data.LED_indices, 
                                                    center_indices = setup_parameters.LED_info.center_indices,
                                                    downsample_image = 4,
                                                    downsample_edges = 10)
        edges_per_image_per_dataset.append(edges_per_image)

    pixel_size = setup_parameters.camera.camera_pixel_size/setup_parameters.lens.magnification
    LED_pitch = setup_parameters.LED_info.LED_pitch
    assumed_inverse_object_to_lens_distance = 0
    assumed_numerical_aperture = setup_parameters.lens.NA

    assumed_calibration_parameters = \
        Calibration_parameters(
            delta_x = assumed_calibration_parameters.LED_x_offset,
            delta_y = assumed_calibration_parameters.LED_y_offset,
            LED_distance = assumed_calibration_parameters.LED_distance,
            alpha = 0,
            beta = 0,
            gamma = 0
        ) 

    all_optimal_calibration_parameters, optimal_numerical_aperture, optimal_inverse_object_to_lens_distance \
        = optimize_bright_field_edge(edges_per_image_per_dataset = edges_per_image_per_dataset,
                                     relative_LED_distances = relative_LED_distances, 
                                     n_values = n_values, m_values = m_values,
                                     pixel_size = pixel_size, LED_pitch = LED_pitch,
                                     assumed_inverse_object_to_lens_distance = assumed_inverse_object_to_lens_distance,
                                     assumed_numerical_aperture = assumed_numerical_aperture, 
                                     assumed_parameters = assumed_calibration_parameters)

    print("NA:", optimal_numerical_aperture)
    print("z1:", optimal_inverse_object_to_lens_distance)
    for optimal_calibration_parameters, data, edges_per_image in zip(all_optimal_calibration_parameters, data_patches, edges_per_image_per_dataset):
        print(optimal_calibration_parameters)

        centers_x, centers_y, radii = calculate_centers_and_radii(LED_n = n_values, 
                                                                LED_m = m_values,
                                                                LED_pitch = LED_pitch,
                                                                pixel_size = pixel_size,
                                                                inverse_object_to_lens_distance\
                                                                = optimal_inverse_object_to_lens_distance,
                                                                numerical_aperture = optimal_numerical_aperture, 
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
                                                    inverse_object_to_lens_distance = optimal_inverse_object_to_lens_distance,
                                                    numerical_aperture = optimal_numerical_aperture, 
                                                    array_size = 5)

        plt.show()

    return optimal_calibration_parameters 


def optimize_bright_field_edge(edges_per_image_per_dataset, n_values, m_values,
                               relative_LED_distances,
                               LED_pitch, pixel_size,
                               assumed_inverse_object_to_lens_distance,
                               assumed_numerical_aperture,
                               assumed_parameters: Calibration_parameters):
    initialization = [
        assumed_numerical_aperture,
        assumed_inverse_object_to_lens_distance,
        assumed_parameters.alpha,
        assumed_parameters.beta,
        assumed_parameters.gamma,
        assumed_parameters.delta_x,
        assumed_parameters.delta_y,
        assumed_parameters.LED_distance
    ]

    error_function = get_error_function(edges_per_image_per_dataset = edges_per_image_per_dataset,
                                        relative_LED_distances = relative_LED_distances,
                                        LED_n = n_values,
                                        LED_m = m_values,
                                        LED_pitch = LED_pitch,
                                        pixel_size = pixel_size)
    
    results = minimize(error_function, x0=initialization, method="Powell")

    all_optimized_parameters = []
    optimal_numerical_aperture, optimal_inverse_object_to_lens_distance = results.x[0], results.x[1]
    alpha, beta, gamma = results.x[2], results.x[3], results.x[4]
    delta_x, delta_y = results.x[5], results.x[6]
    for relative_LED_distance in relative_LED_distances:
        LED_distance= results.x[7] + relative_LED_distance

        optimized_parameters = Calibration_parameters(
            delta_x = delta_x,
            delta_y = delta_y,
            LED_distance = LED_distance,
            alpha = alpha,
            beta = beta,
            gamma = gamma  
        )
        all_optimized_parameters.append(optimized_parameters)

    return all_optimized_parameters, optimal_numerical_aperture, optimal_inverse_object_to_lens_distance




def get_error_function(edges_per_image_per_dataset,
                       relative_LED_distances,
                       LED_n, LED_m, LED_pitch, pixel_size):
    center_and_radii_function = get_centers_and_radii_function(LED_n = LED_n,
                                                               LED_m = LED_m,
                                                               LED_pitch = LED_pitch,
                                                               pixel_size = pixel_size
                                                               )
    def simplified_error_function(args):
        numerical_aperture, inverse_object_to_lens_distance = args[0], args[1]
        alpha, beta, gamma = args[2], args[3], args[4]
        delta_x, delta_y = args[5], args[6]
        error = 0
        for n in range(len(edges_per_image_per_dataset)):
            LED_distance = args[7] + relative_LED_distances[n]
            
            centers_x, centers_y, radii = center_and_radii_function(
                delta_x = delta_x, delta_y = delta_y, 
                LED_distance = LED_distance,
                alpha = alpha, beta = beta, gamma = gamma,
                inverse_object_to_lens_distance\
                    = inverse_object_to_lens_distance,
                numerical_aperture = numerical_aperture 
            )
            error += evaluate_circle_score_non_linear(edges_per_image = edges_per_image_per_dataset[n], 
                                                      centers_x_per_image = centers_x,
                                                      centers_y_per_image = centers_y, 
                                                      radius_per_image = radii)

        return error
    return simplified_error_function



