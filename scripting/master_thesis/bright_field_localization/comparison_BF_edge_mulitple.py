from pyFPM.NTNU_specific.components import (IDS_U3_31J0CP_REV_2_2, TELECENTRIC_3X, INFINITYCORRECTED_10X, 
                                            INFINITYCORRECTED_2X, COMPACT_2X_CALIBRATED, MAIN_LED_ARRAY, 
                                            HAMAMATSU_C11440_42U30)
from pyFPM.setup.Setup_parameters import Lens
from pyFPM.setup.Imaging_system import LED_calibration_parameters
from pyFPM.NTNU_specific.rawdata_from_files import get_rawdata_from_files
from pyFPM.NTNU_specific.setup_from_file import setup_parameters_from_file

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

main_data_folder = Path("E:") / "BFL step"
dataset_name_tele =  main_data_folder / "illum_75mm_telecentric3x"
dataset_name_comp =  main_data_folder / "illum_75mm_compact2x"
dataset_name_inf = main_data_folder / "illum_75mm_infcor10x"
main_result_folder = Path.cwd() / "results" / "master_thesis" / "modelling"

INF10X_MANUALCALIB = Lens(
    NA = np.tan(np.arcsin(0.28)),
    magnification=10,
    effectiv_object_to_aperture_distance = -23e-3,
    focal_length=None,
    working_distance=None,
    depth_of_field=None,
    max_FoV_sensor=None
)

TELE3X_MANUALCALIB = Lens(
    NA = 0.0865,
    magnification=3,
    effectiv_object_to_aperture_distance = np.inf,
    focal_length=None,
    working_distance=None,
    depth_of_field=None,
    max_FoV_sensor=None
)



def main():
    main_comp()
    main_tele()
    main_inf()
    main_inf2x_hamamatsu()
    plt.show()

def main_comp():
    lenses = [COMPACT_2X_CALIBRATED]
    lens_colors = ["yellow"]

    array_size = 3
    calibration_parameters = LED_calibration_parameters(LED_distance=0.102, 
                                                        LED_x_offset=0, 
                                                        LED_y_offset=0, 
                                                        LED_rotation=0)

    setup_parameters, rawdata = get_setup(array_size, dataset_name_comp, lenses[0])

    fig = plot_bright_field_images_with_BF_edge_comparative(rawdata, setup_parameters, 
                                                            calibration_parameters, 
                                                            lenses, lens_colors, array_size)
    
    fig.savefig(main_result_folder / "BF_edge_compact2x.pdf")
    

def main_tele():
    lenses = [TELECENTRIC_3X, TELE3X_MANUALCALIB]
    lens_colors = ["red","yellow"]

    array_size = 3
    calibration_parameters = LED_calibration_parameters(LED_distance=0.102, 
                                                        LED_x_offset=0, 
                                                        LED_y_offset=120e-6, 
                                                        LED_rotation=0)

    setup_parameters, rawdata = get_setup(array_size, dataset_name_tele, lenses[0])

    fig = plot_bright_field_images_with_BF_edge_comparative(rawdata, setup_parameters, 
                                                            calibration_parameters, 
                                                            lenses, lens_colors, array_size)
    
    fig.savefig(main_result_folder / "BF_edge_tele3x.pdf")

def main_inf():
    lenses = [INFINITYCORRECTED_10X, INF10X_MANUALCALIB]
    lens_colors = ["red", "yellow"]

    array_size = 11
    calibration_parameters = LED_calibration_parameters(LED_distance=0.102, 
                                                        LED_x_offset=-200e-6, 
                                                        LED_y_offset=400e-6, 
                                                        LED_rotation=0)

    setup_parameters, rawdata = get_setup(array_size, dataset_name_inf, lenses[0])

    fig = plot_bright_field_images_with_BF_edge_comparative(rawdata, setup_parameters, 
                                                            calibration_parameters, 
                                                            lenses, lens_colors, array_size)
    
    fig.savefig(main_result_folder / "BF_edge_inf10x.pdf")

def main_inf2x_hamamatsu():
    lenses = [INFINITYCORRECTED_2X]
    lens_colors = ["yellow"]
    camera=HAMAMATSU_C11440_42U30
    array_size = 5
    calibration_parameters = LED_calibration_parameters(LED_distance=0.200, 
                                                        LED_x_offset=0, 
                                                        LED_y_offset=0, 
                                                        LED_rotation=0)

    setup_parameters, rawdata = get_setup(array_size, r"C:\Users\erlen\Documents\GitHub\pyFPM\data\Illumination\infinity_2x_illumnation", lenses[0], camera)

    fig = plot_bright_field_images_with_BF_edge_comparative(rawdata, setup_parameters, 
                                                            calibration_parameters, 
                                                            lenses, lens_colors, array_size)
    
    fig.savefig(main_result_folder / "BF_edge_inf2x_hamamatsu.pdf")


def get_setup(array_size, dataset_name, lens, camera=IDS_U3_31J0CP_REV_2_2):
    LED_array = MAIN_LED_ARRAY 

    setup_parameters = setup_parameters_from_file(
        datadirpath = dataset_name,
        lens = lens,
        camera = camera,
        LED_array = LED_array,
        binning_factor = 10
        )

    rawdata = get_rawdata_from_files(
        datadirpath = dataset_name,
        image_format = setup_parameters.image_format,
        center_indices = setup_parameters.LED_info.center_indices,
        max_array_size = array_size,
        float_type = setup_parameters.camera.float_type,
        binning_factor = 10
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
    pixel_size = setup_parameters.camera.camera_pixel_size*setup_parameters.binning_factor/setup_parameters.lens.magnification
    LED_pitch = setup_parameters.LED_info.LED_pitch
    image_center_x = setup_parameters.camera.raw_image_size[0] // (2*setup_parameters.binning_factor)
    image_center_y = setup_parameters.camera.raw_image_size[1] // (2*setup_parameters.binning_factor)
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

    
    return (center_x + image_center_x, center_y + image_center_y), abs(radius)



if __name__ == "__main__":
    main()
