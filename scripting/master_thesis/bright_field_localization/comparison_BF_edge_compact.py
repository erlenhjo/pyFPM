from pyFPM.NTNU_specific.components import (IDS_U3_31J0CP_REV_2_2, COMPACT_2X_CALIBRATED, COMPACT_2X, MAIN_LED_ARRAY)
from pyFPM.setup.Imaging_system import LED_calibration_parameters
from pyFPM.NTNU_specific.rawdata_from_files import get_rawdata_from_files
from pyFPM.NTNU_specific.setup_from_file import setup_parameters_from_file
from pyFPM.NTNU_specific.calibrate_BF.BFL_single import calibrate_dataset
from pyFPM.NTNU_specific.calibrate_BF.BFL_step import NBFL_parameters

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

dataset_name =  Path.cwd() / "data" / "Master_thesis" / "sapphire window" / "compact2x_usaf_200mm_illum"
#dataset_name =  Path.cwd() / "data" / "Master_thesis" / "sapphire window" / "compact2x_usaf_200mm"
main_result_folder = Path.cwd() / "results" / "master_thesis" / "BFL"


def main():
    lenses = [COMPACT_2X, COMPACT_2X_CALIBRATED]
    lens_colors = ["red", "yellow"]
    camera = IDS_U3_31J0CP_REV_2_2

    array_size = 5
    calibration_parameters = LED_calibration_parameters(LED_distance=0.20153892853221111, 
                                                        LED_x_offset=-0.00012446193565815314, 
                                                        LED_y_offset=-0.00012741088856773426, 
                                                        LED_rotation=-0.0010187545121927496)

    setup_parameters, rawdata = get_setup(array_size)

    fig = plot_bright_field_images_with_BF_edge_comparative(rawdata, setup_parameters, 
                                                            calibration_parameters, 
                                                            lenses, lens_colors, array_size)
    
    fig.savefig(main_result_folder / "comparison_BF_edge.pdf")
    plt.show()

def get_setup(array_size):
    LED_array = MAIN_LED_ARRAY 

    setup_parameters = setup_parameters_from_file(
        datadirpath = dataset_name,
        lens = COMPACT_2X,
        camera = IDS_U3_31J0CP_REV_2_2,
        LED_array = LED_array,
        binning_factor = 1
        )

    rawdata = get_rawdata_from_files(
        datadirpath = dataset_name,
        image_format = setup_parameters.image_format,
        center_indices = setup_parameters.LED_info.center_indices,
        max_array_size = array_size,
        float_type = setup_parameters.camera.float_type,
        binning_factor = 1
        )
    
    return setup_parameters, rawdata

def plot_bright_field_images_with_BF_edge_comparative(data, setup_parameters, 
                                                        calibration_parameters: LED_calibration_parameters, 
                                                        lenses, lens_colors,
                                                        array_size: int):
    LED_indices = data.LED_indices

    center_indices = setup_parameters.LED_info.center_indices
    center_x = center_indices[0]
    center_y = center_indices[1]
    y_min = center_y - array_size//2
    x_min = center_x - array_size//2
    y_max = y_min + array_size
    x_max = x_min + array_size

    images = data.images

    max_intensity = np.max(images)

    fig, axes = plt.subplots(nrows=array_size, ncols=array_size, figsize=(7,7), constrained_layout = True)

    for image_nr, indices in enumerate(LED_indices):
        x,y = indices
        if x>=x_min and x<x_max and y>=y_min and y<y_max:
            m = (array_size-1) - (y_max-y-1)
            n = (array_size-1) - (x_max-x-1)
            LED_n = x - center_x
            LED_m = y - center_y

            axes[m,n].matshow(images[image_nr], vmin=0, vmax=max_intensity)
            axes[m,n].axis("off")
            
            for lens, lens_color in zip(lenses, lens_colors):
                center, radius = calculate_BF_edge(setup_parameters=setup_parameters,
                                                   calibration_parameters=calibration_parameters,
                                                   lens = lens, LED_n=LED_n, LED_m=LED_m)
                circle = plt.Circle(center, radius, fill=False, color=lens_color, linestyle="dashed")
                axes[m,n].add_patch(circle)
            
    return fig

def calculate_BF_edge(setup_parameters, calibration_parameters: LED_calibration_parameters,
                      lens, LED_n, LED_m):
    pixel_size = setup_parameters.camera.camera_pixel_size/setup_parameters.lens.magnification
    LED_pitch = setup_parameters.LED_info.LED_pitch
    image_center_x = setup_parameters.camera.raw_image_size[0] // 2
    image_center_y = setup_parameters.camera.raw_image_size[1] // 2
    z_0 = calibration_parameters.LED_distance
    z_q = lens.effective_object_to_aperture_distance
    delta_x = calibration_parameters.LED_x_offset
    delta_y = calibration_parameters.LED_y_offset
    rotation = calibration_parameters.LED_rotation
    NA = lens.NA
    

    rotation = rotation * np.pi/180 # convert to radians
    radius = NA*z_0 / (1 + z_0/z_q) / pixel_size
    center_x = (LED_pitch*LED_n*np.cos(rotation) - LED_pitch*LED_m*np.sin(rotation) + delta_x)\
                /pixel_size / (1+z_0/z_q)
    center_y = (LED_pitch*LED_n*np.sin(rotation) + LED_pitch*LED_m*np.cos(rotation) + delta_y)\
                /pixel_size / (1+z_0/z_q)

    
    return (center_x + image_center_x, center_y + image_center_y), radius



if __name__ == "__main__":
    main()