from pyFPM.setup.Data import Rawdata
from pyFPM.setup.Setup_parameters import Setup_parameters
from pyFPM.calibration.non_linear_BFL.shared import calculate_centers_and_radius, Calibration_parameters


import numpy as np
import matplotlib.pyplot as plt

def plot_calibration_results(n_values, m_values, LED_pitch, pixel_size,
                             setup_parameters: Setup_parameters, data: Rawdata,
                             calibration_parameters: Calibration_parameters,
                             edges_per_image, result_folder, step_nr
                             ):
    centers_x, centers_y, radius = calculate_centers_and_radius(LED_n = n_values, 
                                                            LED_m = m_values,
                                                            LED_pitch = LED_pitch,
                                                            pixel_size = pixel_size,
                                                            delta_x = calibration_parameters.delta_x, 
                                                            delta_y = calibration_parameters.delta_y,
                                                            rotation = calibration_parameters.rotation,
                                                            numerical_aperture_times_LED_distance = calibration_parameters.numerical_aperture_times_LED_distance,
                                                            distance_ratio = calibration_parameters.distance_ratio
                                                            ) 


    fig1, axes = plt.subplots(1,1)

    for edges, center_x, center_y in zip(edges_per_image, centers_x, centers_y):
        axes.scatter(edges[:,0],edges[:,1])
        circle = plt.Circle([center_x, center_y], radius, fill=False, color="r", linestyle="dashed")
        axes.add_patch(circle)
        axes.set_xlim(left=-data.images[0].shape[1]//2, right=data.images[0].shape[1]//2)
        axes.set_ylim(bottom=-data.images[0].shape[0]//2, top=data.images[0].shape[0]//2)

    fig2 = plot_bright_field_images_with_BF_edge(data = data, 
                                                calibration_parameters = calibration_parameters,
                                                array_size = int(np.sqrt(len(data.LED_indices))),
                                                center_indices = setup_parameters.LED_info.center_indices,
                                                pixel_size = pixel_size,
                                                LED_pitch = LED_pitch)
    
    plot_path = result_folder / f"edges_{step_nr}"
    fig1.savefig(plot_path.with_suffix(f".pdf"), format = "pdf")
    fig1.savefig(plot_path.with_suffix(f".png"), format = "png")
    

    plot_path = result_folder / f"BF_images_{step_nr}"
    fig2.savefig(plot_path.with_suffix(f".pdf"), format = "pdf")
    fig2.savefig(plot_path.with_suffix(f".png"), format = "png")

    plt.close(fig=fig1)
    plt.close(fig=fig2)


def plot_bright_field_images_with_BF_edge(data: Rawdata,
                                          calibration_parameters: Calibration_parameters,
                                          array_size: int, 
                                          center_indices,
                                          pixel_size,
                                          LED_pitch
                                        ):
    LED_indices = data.LED_indices
    image_center_y, image_center_x = np.array(data.images[0].shape) // 2

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
            m = (array_size-1) - (y_max-y-1)
            n = (array_size-1) - (x_max-x-1)
            LED_n = x - center_x
            LED_m = y - center_y

            axes[m,n].matshow(data.images[image_nr], vmin=0, vmax=max_intensity)
            axes[m,n].axis("off")

            center, radius = calculate_BF_edge_circle(calibration_parameters=calibration_parameters,
                                                     LED_n=LED_n, LED_m=LED_m,
                                                     pixel_size = pixel_size, 
                                                     LED_pitch = LED_pitch, 
                                                     image_center_x = image_center_x, 
                                                     image_center_y = image_center_y)
            circle = plt.Circle(center, radius, fill=False, color="r", linestyle="dashed")
            axes[m,n].add_patch(circle)
            
    return fig

def calculate_BF_edge_circle(calibration_parameters: Calibration_parameters,
                             LED_n, LED_m, pixel_size, LED_pitch, 
                             image_center_x, image_center_y):
        
    center_x, center_y, radius = calculate_centers_and_radius(
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