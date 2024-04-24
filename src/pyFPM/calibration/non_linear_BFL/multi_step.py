from pyFPM.setup.Data import Rawdata
from pyFPM.setup.Setup_parameters import Setup_parameters
from pyFPM.setup.Imaging_system import LED_calibration_parameters
from pyFPM.calibration.non_linear_BFL.edge_detection import detect_edges_per_image
from pyFPM.calibration.non_linear_BFL.shared import (Calibration_parameters, 
                                                              calculate_centers_and_radius, 
                                                              evaluate_circle_score_non_linear)
from pyFPM.calibration.non_linear_BFL.plotting import plot_calibration_results


from scipy.optimize import minimize



def non_linear_BFL_multi_step(data: Rawdata, setup_parameters: Setup_parameters, 
                              assumed_calibration_parameters: Calibration_parameters,
                              result_folder, step_nr, otsu_exponent, canny_sigma,
                              image_boundary_filter_distance, downsample_edges_factor,
                              binning_factor, NA_only):
            
    pixel_size = setup_parameters.camera.camera_pixel_size*binning_factor/setup_parameters.lens.magnification
    LED_pitch = setup_parameters.LED_info.LED_pitch    

    edges_per_image, n_values, m_values = detect_edges_per_image(
                                                images = data.images**otsu_exponent, 
                                                canny_sigma = canny_sigma,
                                                image_boundary_filter_distance = image_boundary_filter_distance,
                                                LED_indices = data.LED_indices, 
                                                center_indices = setup_parameters.LED_info.center_indices,
                                                downsample_edges = downsample_edges_factor)

    if not NA_only:
        optimal_calibration_parameters, optimization_result \
            = optimize_bright_field_edge(edges_per_image = edges_per_image,
                                        n_values = n_values, m_values = m_values,
                                        pixel_size = pixel_size, LED_pitch = LED_pitch,
                                        assumed_parameters = assumed_calibration_parameters)
    else:
        optimal_calibration_parameters, optimization_result \
            = optimize_bright_field_edge_NA_only(edges_per_image = edges_per_image,
                                                n_values = n_values, m_values = m_values,
                                                pixel_size = pixel_size, LED_pitch = LED_pitch,
                                                assumed_parameters = assumed_calibration_parameters)
    
    plot_calibration_results(n_values = n_values, 
                             m_values = m_values, 
                             LED_pitch = LED_pitch, 
                             pixel_size = pixel_size,
                             setup_parameters = setup_parameters, 
                             data = data,
                             calibration_parameters = optimal_calibration_parameters,
                             edges_per_image = edges_per_image, 
                             result_folder = result_folder, 
                             step_nr = step_nr
                             )
    

    return optimal_calibration_parameters, optimization_result

def optimize_bright_field_edge(edges_per_image, n_values, m_values,
                               LED_pitch, pixel_size,
                               assumed_parameters: Calibration_parameters):
    initialization = [
        assumed_parameters.delta_x,
        assumed_parameters.delta_y,
        assumed_parameters.rotation,
        assumed_parameters.numerical_aperture_times_LED_distance,
        assumed_parameters.distance_ratio
    ]

    error_function = get_error_function(edges_per_image = edges_per_image,
                                        LED_n = n_values,
                                        LED_m = m_values,
                                        LED_pitch = LED_pitch,
                                        pixel_size = pixel_size)
    
    results = minimize(error_function, x0=initialization, method="Powell")

    delta_x, delta_y, rotation = results.x[0], results.x[1], results.x[2] 
    numerical_aperture_times_LED_distance, distance_ratio = results.x[3], results.x[4]


    return Calibration_parameters(
        delta_x=delta_x,
        delta_y=delta_y,
        rotation=rotation,
        numerical_aperture_times_LED_distance=numerical_aperture_times_LED_distance,
        distance_ratio=distance_ratio
    ), results




def get_error_function(edges_per_image,
                       LED_n, LED_m, LED_pitch, pixel_size):
    centers_and_radius_function = get_centers_and_radius_function_series(LED_n = LED_n,
                                                                    LED_m = LED_m,
                                                                    LED_pitch = LED_pitch,
                                                                    pixel_size = pixel_size
                                                                    )
    def simplified_error_function(args):
        delta_x, delta_y, rotation = args[0], args[1], args[2]
        numerical_aperture_times_LED_distance, distance_ratio = args[3], args[4]
        
            
        centers_x, centers_y, radius = centers_and_radius_function(
            delta_x = delta_x, delta_y = delta_y, rotation = rotation,
            numerical_aperture_times_LED_distance = numerical_aperture_times_LED_distance,
            distance_ratio = distance_ratio
        )
        return evaluate_circle_score_non_linear(edges_per_image = edges_per_image, 
                                                    centers_x_per_image = centers_x,
                                                    centers_y_per_image = centers_y, 
                                                    radius = radius)

    return simplified_error_function

def optimize_bright_field_edge_NA_only(edges_per_image, n_values, m_values,
                               LED_pitch, pixel_size,
                               assumed_parameters: Calibration_parameters):
    initialization = [
        assumed_parameters.delta_x,
        assumed_parameters.delta_y,
        assumed_parameters.rotation,
        assumed_parameters.numerical_aperture_times_LED_distance
    ]

    error_function = get_error_function_NA_only(edges_per_image = edges_per_image,
                                                distance_ratio = assumed_parameters.distance_ratio,
                                                LED_n = n_values,
                                                LED_m = m_values,
                                                LED_pitch = LED_pitch,
                                                pixel_size = pixel_size)
    
    results = minimize(error_function, x0=initialization, method="Powell")

    delta_x, delta_y, rotation = results.x[0], results.x[1], results.x[2] 
    numerical_aperture_times_LED_distance = results.x[3]


    return Calibration_parameters(
        delta_x=delta_x,
        delta_y=delta_y,
        rotation=rotation,
        numerical_aperture_times_LED_distance=numerical_aperture_times_LED_distance,
        distance_ratio=assumed_parameters.distance_ratio
    ), results


def get_error_function_NA_only(edges_per_image, distance_ratio,
                                LED_n, LED_m, LED_pitch, pixel_size):
    centers_and_radius_function = get_centers_and_radius_function_series(LED_n = LED_n,
                                                                    LED_m = LED_m,
                                                                    LED_pitch = LED_pitch,
                                                                    pixel_size = pixel_size
                                                                    )
    def simplified_error_function(args):
        delta_x, delta_y, rotation = args[0], args[1], args[2]
        numerical_aperture_times_LED_distance = args[3]
        
            
        centers_x, centers_y, radius = centers_and_radius_function(
            delta_x = delta_x, delta_y = delta_y, rotation = rotation,
            numerical_aperture_times_LED_distance = numerical_aperture_times_LED_distance,
            distance_ratio = distance_ratio
        )
        return evaluate_circle_score_non_linear(edges_per_image = edges_per_image, 
                                                    centers_x_per_image = centers_x,
                                                    centers_y_per_image = centers_y, 
                                                    radius = radius)

    return simplified_error_function



def get_centers_and_radius_function_series(LED_n, LED_m, LED_pitch, pixel_size):
    def simplified_centers_and_radius_function(delta_x, delta_y, rotation,
                                             numerical_aperture_times_LED_distance,
                                             distance_ratio
                                             ):
        return calculate_centers_and_radius(
                                LED_n = LED_n, LED_m = LED_m, 
                                LED_pitch = LED_pitch, pixel_size = pixel_size,
                                delta_x=delta_x, delta_y=delta_y, rotation=rotation,
                                numerical_aperture_times_LED_distance=numerical_aperture_times_LED_distance,
                                distance_ratio = distance_ratio
                                )

    return simplified_centers_and_radius_function


