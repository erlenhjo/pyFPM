from pyFPM.setup.Data import Rawdata
from pyFPM.setup.Setup_parameters import Setup_parameters
from pyFPM.setup.Imaging_system import LED_calibration_parameters
from pyFPM.calibration.non_linear_BFL.edge_detection import detect_edges_per_image
from pyFPM.calibration.non_linear_BFL.shared import (Calibration_parameters, 
                                                              calculate_centers_and_radius, 
                                                              evaluate_circle_score_non_linear)
from pyFPM.calibration.non_linear_BFL.plotting import plot_calibration_results


from scipy.optimize import minimize


def non_linear_BFL_single_step(data: Rawdata, setup_parameters: Setup_parameters, 
                               assumed_calibration_parameters: LED_calibration_parameters,
                               result_folder, otsu_exponent, canny_sigma,
                               image_boundary_filter_distance, downsample_edges_factor,
                               binning_factor):

    pixel_size = setup_parameters.camera.camera_pixel_size * binning_factor/setup_parameters.lens.magnification
    LED_pitch = setup_parameters.LED_info.LED_pitch
    inverse_object_to_lens_distance = 1/setup_parameters.lens.effective_object_to_aperture_distance
    numerical_aperture = setup_parameters.lens.NA

 
    edges_per_image, n_values, m_values = detect_edges_per_image(
                                                   images = data.images**otsu_exponent, 
                                                   canny_sigma = canny_sigma,
                                                   image_boundary_filter_distance=image_boundary_filter_distance,
                                                   LED_indices = data.LED_indices, 
                                                   center_indices = setup_parameters.LED_info.center_indices,
                                                   downsample_edges = downsample_edges_factor)


    optimal_LED_calibration_parameters: LED_calibration_parameters \
          = optimize_bright_field_edge(edges_per_image = edges_per_image, 
                                       n_values = n_values, m_values = m_values,
                                       pixel_size = pixel_size, LED_pitch = LED_pitch,
                                       inverse_object_to_lens_distance=inverse_object_to_lens_distance,
                                       numerical_aperture = numerical_aperture, 
                                       assumed_parameters = assumed_calibration_parameters)
    
    optimal_calibration_parameters \
        = Calibration_parameters(
            delta_x = optimal_LED_calibration_parameters.LED_x_offset,
            delta_y = optimal_LED_calibration_parameters.LED_y_offset,
            rotation = optimal_LED_calibration_parameters.LED_rotation,
            numerical_aperture_times_LED_distance \
                = optimal_LED_calibration_parameters.LED_distance * numerical_aperture,
            distance_ratio \
                = optimal_LED_calibration_parameters.LED_distance * inverse_object_to_lens_distance
        )

    plot_calibration_results(n_values = n_values, 
                             m_values = m_values, 
                             LED_pitch = LED_pitch, 
                             pixel_size = pixel_size,
                             setup_parameters = setup_parameters, 
                             data = data,
                             calibration_parameters = optimal_calibration_parameters,
                             edges_per_image = edges_per_image, 
                             result_folder = result_folder, 
                             step_nr = "single_step"
                             )


    return optimal_LED_calibration_parameters 


def optimize_bright_field_edge(edges_per_image, n_values, m_values,
                               LED_pitch, pixel_size,
                               inverse_object_to_lens_distance, 
                               numerical_aperture,
                               assumed_parameters: LED_calibration_parameters):
    initalization = [
        assumed_parameters.LED_x_offset,
        assumed_parameters.LED_y_offset,
        assumed_parameters.LED_distance,
        assumed_parameters.LED_rotation
    ]
    error_function = get_error_function(edges = edges_per_image,
                                        LED_n = n_values,
                                        LED_m = m_values,
                                        LED_pitch = LED_pitch,
                                        pixel_size = pixel_size,
                                        inverse_object_to_lens_distance = inverse_object_to_lens_distance,
                                        numerical_aperture = numerical_aperture
                                        )
    
    results = minimize(error_function, x0=initalization, method="Powell")

    delta_x, delta_y, \
        LED_distance, rotation = results.x

    optimized_parameters = LED_calibration_parameters(
        LED_x_offset = delta_x,
        LED_y_offset = delta_y,
        LED_distance = LED_distance,
        LED_rotation = rotation 
    )

    return optimized_parameters



def get_error_function(edges, LED_n, LED_m, LED_pitch, pixel_size, 
                       inverse_object_to_lens_distance, numerical_aperture):
    center_and_radius_function = get_centers_and_radius_function(LED_n = LED_n,
                                                               LED_m = LED_m,
                                                               LED_pitch = LED_pitch,
                                                               pixel_size = pixel_size
                                                               )
    def simplified_error_function(args):
        delta_x, delta_y, \
            LED_distance, rotation = args

        centers_x, centers_y, radius = center_and_radius_function(
            delta_x = delta_x, delta_y = delta_y,
            LED_distance = LED_distance, rotation=rotation,
            inverse_object_to_lens_distance\
             = inverse_object_to_lens_distance,
            numerical_aperture = numerical_aperture
        )
        return evaluate_circle_score_non_linear(edges_per_image = edges, 
                                                centers_x_per_image = centers_x,
                                                centers_y_per_image = centers_y, 
                                                radius = radius)
    return simplified_error_function


def get_centers_and_radius_function(LED_n, LED_m, LED_pitch, pixel_size):
    def simplified_center_and_radii_function(delta_x, delta_y, 
                                             LED_distance, rotation,
                                             inverse_object_to_lens_distance,
                                             numerical_aperture
                                             ):
        return calculate_centers_and_radius(
                                LED_n = LED_n, LED_m = LED_m, 
                                LED_pitch = LED_pitch, 
                                pixel_size = pixel_size,
                                delta_x = delta_x, 
                                delta_y = delta_y, 
                                rotation=rotation,
                                numerical_aperture_times_LED_distance\
                                    = numerical_aperture*LED_distance,
                                distance_ratio \
                                    = LED_distance * inverse_object_to_lens_distance 
                                )

    return simplified_center_and_radii_function
