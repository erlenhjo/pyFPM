import matplotlib.pyplot as plt
import numpy as np

from pyFPM.setup.Data import Data_patch
from pyFPM.setup.Setup_parameters import Setup_parameters
from pyFPM.setup.Imaging_system import LED_calibration_parameters





def plot_bright_field_images(data_patch: Data_patch, setup_parameters: Setup_parameters, array_size: int):
    fig, axes = plt.subplots(nrows=array_size, ncols=array_size, figsize=(7,7), constrained_layout = True)
    plot_bright_field_images_internal(axes, data_patch, setup_parameters, array_size)
    return fig

def plot_bright_field_images_internal(axes, data_patch: Data_patch, setup_parameters: Setup_parameters, array_size: int):
    LED_indices = data_patch.LED_indices

    center_indices = setup_parameters.LED_info.center_indices
    center_x = center_indices[0]
    center_y = center_indices[1]
    y_min = center_y - array_size//2
    x_min = center_x - array_size//2
    y_max = y_min + array_size
    x_max = x_min + array_size

    max_intensity = np.max(data_patch.amplitude_images)**2

    for image_nr, indices in enumerate(LED_indices):
        x,y = indices
        if x>=x_min and x<x_max and y>=y_min and y<y_max:
            m = (array_size-1) - (y_max-y-1)
            n = (array_size-1) - (x_max-x-1)
            axes[m,n].matshow(data_patch.amplitude_images[image_nr]**2, vmin=0, vmax=max_intensity)
            axes[m,n].axis("off")


def plot_bright_field_images_with_BF_edge(data_patch: Data_patch, setup_parameters: Setup_parameters, 
                                          calibration_parameters: LED_calibration_parameters, 
                                          array_size: int):
    fig, axes = plt.subplots(nrows=array_size, ncols=array_size, figsize=(7,7), constrained_layout = True)
    plot_bright_field_images_with_BF_edge_internal(axes, data_patch, setup_parameters, 
                                                    calibration_parameters, array_size)
    return fig


def plot_bright_field_images_with_BF_edge_internal(axes, data_patch: Data_patch, setup_parameters: Setup_parameters, 
                                                    calibration_parameters: LED_calibration_parameters, 
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

    for image_nr, indices in enumerate(LED_indices):
        x,y = indices
        if x>=x_min and x<x_max and y>=y_min and y<y_max:
            m = (array_size-1) - (y_max-y-1)
            n = (array_size-1) - (x_max-x-1)
            LED_n = x - center_x
            LED_m = y - center_y

            axes[m,n].matshow(data_patch.amplitude_images[image_nr]**2, vmin=0, vmax=max_intensity)
            axes[m,n].axis("off")

            center, radius = calculate_BF_edge(setup_parameters=setup_parameters,
                                               calibration_parameters=calibration_parameters,
                                               LED_n=LED_n, LED_m=LED_m)
            circle = plt.Circle(center, radius, fill=False, color="r", linestyle="dashed")
            axes[m,n].add_patch(circle)
            

def calculate_BF_edge(setup_parameters: Setup_parameters, calibration_parameters: LED_calibration_parameters,
                      LED_n, LED_m):
    pixel_size = setup_parameters.camera.camera_pixel_size/setup_parameters.lens.magnification
    LED_pitch = setup_parameters.LED_info.LED_pitch
    image_center_x = setup_parameters.camera.raw_image_size[0] // 2
    image_center_y = setup_parameters.camera.raw_image_size[1] // 2
    z_0 = calibration_parameters.LED_distance
    z_q = setup_parameters.lens.effective_object_to_aperture_distance
    delta_x = calibration_parameters.LED_x_offset
    delta_y = calibration_parameters.LED_y_offset
    rotation = calibration_parameters.LED_rotation
    NA = setup_parameters.lens.NA
    

    rotation = rotation * np.pi/180 # convert to radians
    radius = NA*z_0 / (1 + z_0/z_q) / pixel_size
    center_x = (LED_pitch*LED_n*np.cos(rotation) - LED_pitch*LED_m*np.sin(rotation) + delta_x)\
                /pixel_size / (1+z_0/z_q)
    center_y = (LED_pitch*LED_n*np.sin(rotation) + LED_pitch*LED_m*np.cos(rotation) + delta_y)\
                /pixel_size / (1+z_0/z_q)

    
    return (center_x + image_center_x, center_y + image_center_y), radius