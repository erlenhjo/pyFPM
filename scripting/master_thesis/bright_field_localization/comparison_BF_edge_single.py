from pyFPM.NTNU_specific.components import (IDS_U3_31J0CP_REV_2_2, COMPACT_2X_CALIBRATED, COMPACT_2X, MAIN_LED_ARRAY)
from pyFPM.setup.Imaging_system import LED_calibration_parameters
from pyFPM.NTNU_specific.rawdata_from_files import get_rawdata_from_files
from pyFPM.NTNU_specific.setup_from_file import setup_parameters_from_file
from pyFPM.NTNU_specific.simulate_images.only_illumination import simulate_illumination
from pyFPM.setup.Data import Data_patch
from pyFPM.setup.Setup_parameters import Camera

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import pickle

dataset_name_1 =  Path.cwd() / "data" / "Master_thesis" / "sapphire window" / "compact2x_usaf_200mm_illum"
dataset_name_2 =  Path.cwd() / "data" / "Master_thesis" / "sapphire window" / "compact2x_usaf_200mm"
main_result_folder = Path.cwd() / "results" / "master_thesis" / "BFL"


def main():
    lens = COMPACT_2X_CALIBRATED
    camera = Camera(
    camera_pixel_size = (2.74e-6)*2,
    raw_image_size = np.array([2848, 2844])//2,
    float_type = np.float64
)

    array_size = 3
    calibration_parameters = LED_calibration_parameters(LED_distance=0.20153892853221111, 
                                                        LED_x_offset=-0.00012446193565815314, 
                                                        LED_y_offset=-0.00012741088856773426, 
                                                        LED_rotation=-0.0010187545121927496)



    # setup_parameters, simulated_data_patch, imaging_system, illumination_pattern, applied_pupil, high_res_complex_object\
    #    = simulate_illumination(lens = lens, 
    #                            camera = camera,
    #                            correct_spherical_wave_illumination = True, 
    #                            correct_Fresnel_propagation = True,
    #                            arraysize=array_size,
    #                            calibration_parameters=calibration_parameters,
    #                            patch_offset=[0,0],
    #                            limit_LED_indices = [[16,16],[15,15]])

    # sim_path = Path.cwd() / "scripting" / "master_thesis" / "bright_field_localization" / "sim_data.obj"
    # with open(sim_path, "wb") as file:
    #     pickle.dump(simulated_data_patch, file)
    sim_path = Path.cwd() / "scripting" / "master_thesis" / "bright_field_localization" / "sim_data.obj"
    with open(sim_path, "rb") as file:
        simulated_data_patch = pickle.load(file)

    setup_parameters, rawdata_1 = get_setup(array_size, dataset_name=dataset_name_1)
    setup_parameters, rawdata_2 = get_setup(array_size, dataset_name=dataset_name_2)    

    fig1, fig2, fig3 = plot_bright_field_image_single(rawdata_1, rawdata_2, simulated_data_patch, 
                                         setup_parameters, calibration_parameters, array_size,
                                         NA_ratios=[0.85,1,1.15], NA_colors=["red", "yellow", "red"])
    
    fig1.savefig(main_result_folder / "comparison_BF_edge_singel_illum.png")
    fig1.savefig(main_result_folder / "comparison_BF_edge_singel_illum.pdf")
    fig2.savefig(main_result_folder / "comparison_BF_edge_singel_usaf.png")
    fig2.savefig(main_result_folder / "comparison_BF_edge_singel_usaf.pdf")
    fig3.savefig(main_result_folder / "comparison_BF_edge_singel_sim.png")
    fig3.savefig(main_result_folder / "comparison_BF_edge_singel_sim.pdf")
    plt.show()

def get_setup(array_size, dataset_name):
    LED_array = MAIN_LED_ARRAY 

    setup_parameters = setup_parameters_from_file(
        datadirpath = dataset_name,
        lens = COMPACT_2X_CALIBRATED,
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

def plot_bright_field_image_single(data1, data2, data3_amplitude, 
                                   setup_parameters, calibration_parameters: LED_calibration_parameters, 
                                   array_size: int, NA_ratios, NA_colors):
    lens = setup_parameters.lens
    center_indices = setup_parameters.LED_info.center_indices
    center_x = center_indices[0]
    center_y = center_indices[1]
    y_min = center_y - array_size//2
    x_min = center_x - array_size//2
    y_max = y_min + array_size
    x_max = x_min + array_size

    images1 = data1.images
    images2 = data2.images
    images3 = data3_amplitude.amplitude_images**2
    max_intensity = np.max([images1.max(), images2.max()])

    fig1, axes1 = plt.subplots(nrows=1, ncols=1, figsize=(4,4), constrained_layout = True)
    fig2, axes2 = plt.subplots(nrows=1, ncols=1, figsize=(4,4), constrained_layout = True)
    fig3, axes3 = plt.subplots(nrows=1, ncols=1, figsize=(4,4), constrained_layout = True)

    for images, axes, LED_indices, max_intensity in \
        zip([images1, images2, images3], [axes1, axes2, axes3], \
            [data1.LED_indices, data2.LED_indices, data3_amplitude.LED_indices],
            [max_intensity, max_intensity, images3.max()]):
        
        for image_nr, indices in enumerate(LED_indices):
            x,y = indices
            LED_n = x - center_x
            LED_m = y - center_y
            if LED_n == -1 and LED_m == -1:
                axes.matshow(images[image_nr], vmin=0, vmax=max_intensity)
                axes.axis("off")
                for ratio, color in zip(NA_ratios,NA_colors):
                    center, radius = calculate_BF_edge(setup_parameters=setup_parameters,
                                                    calibration_parameters=calibration_parameters,
                                                    lens = lens, LED_n=LED_n, LED_m=LED_m)
                    circle = plt.Circle(center, radius*ratio, fill=False, color=color, linestyle="dashed")
                    axes.add_patch(circle)
            
    return fig1, fig2, fig3

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