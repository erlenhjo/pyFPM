from pyFPM.setup.Data import Rawdata
from pyFPM.setup.Setup_parameters import Setup_parameters
from pyFPM.setup.Imaging_system import LED_calibration_parameters
from pyFPM.recovery.calibration.edge_detection import detect_edges_per_image

import matplotlib.pyplot as plt
import numpy as np
from dataclasses import dataclass
from scipy.optimize import minimize

@dataclass
class Calibration_parameters_advanced:
    delta_x: float
    delta_y: float
    rotation: float
    numerical_aperture_times_LED_distance: float
    distance_ratio: float


def advanced_non_linear_BFL(data: Rawdata, setup_parameters: Setup_parameters, 
                         assumed_calibration_parameters: LED_calibration_parameters,
                         result_folder, result_suffix, step_nr):
    
    pixel_size = setup_parameters.camera.camera_pixel_size/setup_parameters.lens.magnification
    LED_pitch = setup_parameters.LED_info.LED_pitch
    numerical_aperture = setup_parameters.lens.NA

    assumed_calibration_parameters = \
        Calibration_parameters_advanced(
            delta_x = assumed_calibration_parameters.LED_x_offset,
            delta_y = assumed_calibration_parameters.LED_y_offset,
            rotation = assumed_calibration_parameters.LED_rotation,
            numerical_aperture_times_LED_distance = numerical_aperture*assumed_calibration_parameters.LED_distance,
            distance_ratio = 0
        )


    otsu_power = 2 # 1/2 means that the otsu threshold is based on amplitude, 1 on intensity, 2 on intesity^2
    canny_sigma = 10

    edges_per_image, n_values, m_values = detect_edges_per_image(
                                                images = data.images**otsu_power, 
                                                canny_sigma = canny_sigma,
                                                LED_indices = data.LED_indices, 
                                                center_indices = setup_parameters.LED_info.center_indices,
                                                downsample_image = 4,
                                                downsample_edges = 10)

    optimal_calibration_parameters: Calibration_parameters_advanced \
        = optimize_bright_field_edge(edges_per_image = edges_per_image,
                                    n_values = n_values, m_values = m_values,
                                    pixel_size = pixel_size, LED_pitch = LED_pitch,
                                    assumed_parameters = assumed_calibration_parameters)

    centers_x, centers_y, radius = calculate_centers_and_radius_series(LED_n = n_values, 
                                                            LED_m = m_values,
                                                            LED_pitch = LED_pitch,
                                                            pixel_size = pixel_size,
                                                            delta_x = optimal_calibration_parameters.delta_x, 
                                                            delta_y = optimal_calibration_parameters.delta_y,
                                                            rotation = optimal_calibration_parameters.rotation,
                                                            numerical_aperture_times_LED_distance = optimal_calibration_parameters.numerical_aperture_times_LED_distance,
                                                            distance_ratio = optimal_calibration_parameters.distance_ratio
                                                            ) 
    
    fig1, axes = plt.subplots(1,1)

    for edges, center_x, center_y in zip(edges_per_image, centers_x, centers_y):
        axes.scatter(edges[:,0],edges[:,1])
        circle = plt.Circle([center_x, center_y], radius, fill=False, color="r", linestyle="dashed")
        axes.add_patch(circle)
        axes.set_xlim(left=-setup_parameters.camera.raw_image_size[0]//2, right=setup_parameters.camera.raw_image_size[0]//2)
        axes.set_ylim(bottom=-setup_parameters.camera.raw_image_size[1]//2, top=setup_parameters.camera.raw_image_size[1]//2)

    fig2 = plot_bright_field_images_with_BF_edge(data = data, 
                                                setup_parameters = setup_parameters, 
                                                calibration_parameters = optimal_calibration_parameters,
                                                array_size = int(np.sqrt(len(data.LED_indices))))
    
    plot_path = result_folder / f"edges_{step_nr}"
    fig1.savefig(plot_path.with_suffix(f".{result_suffix}"), format = result_suffix)

    plot_path = result_folder / f"BF_images_{step_nr}"
    fig2.savefig(plot_path.with_suffix(f".{result_suffix}"), format = result_suffix)

    # plt.show()

    plt.close(fig=fig1)
    plt.close(fig=fig2)

    return optimal_calibration_parameters

def optimize_bright_field_edge(edges_per_image, n_values, m_values,
                               LED_pitch, pixel_size,
                               assumed_parameters: Calibration_parameters_advanced):
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


    return Calibration_parameters_advanced(
        delta_x=delta_x,
        delta_y=delta_y,
        rotation=rotation,
        numerical_aperture_times_LED_distance=numerical_aperture_times_LED_distance,
        distance_ratio=distance_ratio
    )




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



def calculate_centers_and_radius_series(LED_n, LED_m, LED_pitch, pixel_size,
                                       delta_x, delta_y, rotation,
                                       numerical_aperture_times_LED_distance,
                                       distance_ratio
                                    ):
    r_xx = np.cos(rotation)
    r_xy = np.sin(rotation)
    r_yx = -np.sin(rotation)
    r_yy = np.cos(rotation)
    
    if (1+distance_ratio) == 0:
        distance_ratio -= 1e-6

    LEDs_x = LED_pitch*LED_n*r_xx + LED_pitch*LED_m*r_xy
    LEDs_y = LED_pitch*LED_n*r_yx + LED_pitch*LED_m*r_yy

    radius = numerical_aperture_times_LED_distance / pixel_size / (1 + distance_ratio)
    centers_x = (LEDs_x + delta_x) / pixel_size \
                / (1 + distance_ratio)
    centers_y = (LEDs_y + delta_y) / pixel_size \
                / (1 + distance_ratio)
    
    return centers_x, centers_y, radius


def get_centers_and_radius_function_series(LED_n, LED_m, LED_pitch, pixel_size):
    def simplified_centers_and_radius_function(delta_x, delta_y, rotation,
                                             numerical_aperture_times_LED_distance,
                                             distance_ratio
                                             ):
        return calculate_centers_and_radius_series(
                                LED_n = LED_n, LED_m = LED_m, 
                                LED_pitch = LED_pitch, pixel_size = pixel_size,
                                delta_x=delta_x, delta_y=delta_y, rotation=rotation,
                                numerical_aperture_times_LED_distance=numerical_aperture_times_LED_distance,
                                distance_ratio = distance_ratio
                                )

    return simplified_centers_and_radius_function

def evaluate_circle_score_non_linear(edges_per_image, centers_x_per_image,
                                    centers_y_per_image, radius):
    score = 0
    for edges, center_x, center_y in zip(edges_per_image, centers_x_per_image, centers_y_per_image):
        distance_from_center = np.sqrt((edges[:,0]-center_x)**2 + (edges[:,1]-center_y)**2)
        score += np.sum(np.abs(distance_from_center-radius)**2)/len(distance_from_center)
    return score

def plot_bright_field_images_with_BF_edge(data: Rawdata, setup_parameters: Setup_parameters, 
                                          calibration_parameters: Calibration_parameters_advanced,
                                          array_size: int):
    LED_indices = data.LED_indices

    center_indices = setup_parameters.LED_info.center_indices
    center_x = center_indices[0]
    center_y = center_indices[1]
    y_min = center_y - array_size//2
    x_min = center_x - array_size//2
    y_max = y_min + array_size
    x_max = x_min + array_size

    max_intensity = np.max(data.images)

    fig, axes = plt.subplots(nrows=array_size, ncols=array_size, figsize=(7,7), constrained_layout = True)

    for image_nr, indices in enumerate(LED_indices):
        x,y = indices
        if x>=x_min and x<x_max and y>=y_min and y<y_max:
            m = y_max-y-1
            n = x_max-x-1
            LED_n = x - center_x
            LED_m = y - center_y

            axes[m,n].matshow(data.images[image_nr], vmin=0, vmax=max_intensity)
            axes[m,n].axis("off")

            center, radius = calculate_BF_edge_circle(setup_parameters=setup_parameters,
                                                     calibration_parameters=calibration_parameters,
                                                     LED_n=LED_n, LED_m=LED_m)
            circle = plt.Circle(center, radius, fill=False, color="r", linestyle="dashed")
            axes[m,n].add_patch(circle)
            
    return fig

def calculate_BF_edge_circle(setup_parameters: Setup_parameters, 
                      calibration_parameters: Calibration_parameters_advanced,
                      LED_n, LED_m):
    pixel_size = setup_parameters.camera.camera_pixel_size/setup_parameters.lens.magnification
    LED_pitch = setup_parameters.LED_info.LED_pitch
    image_center_x = setup_parameters.camera.raw_image_size[0] // 2
    image_center_y = setup_parameters.camera.raw_image_size[1] // 2
    
    center_x, center_y, radius = calculate_centers_and_radius_series(
        LED_n = LED_n,
        LED_m = LED_m,
        LED_pitch = LED_pitch,
        pixel_size = pixel_size,
        delta_x = calibration_parameters.delta_x,
        delta_y = calibration_parameters.delta_y,
        rotation = calibration_parameters.rotation,
        numerical_aperture_times_LED_distance = calibration_parameters.numerical_aperture_times_LED_distance,
        distance_ratio = calibration_parameters.distance_ratio
    ) 

    
    return (center_x + image_center_x, center_y + image_center_y), radius