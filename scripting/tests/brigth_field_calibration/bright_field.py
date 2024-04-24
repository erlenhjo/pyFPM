from pyFPM.experimental.plot_illumination import plot_bright_field_images_with_BF_edge
from pyFPM.NTNU_specific.simulate_images.only_illumination import simulate_illumination
from pyFPM.NTNU_specific.setup_from_file import setup_parameters_from_file
from pyFPM.NTNU_specific.rawdata_from_files import get_rawdata_from_files
from pyFPM.NTNU_specific.components import HAMAMATSU_C11440_42U30, MAIN_LED_ARRAY, INFINITYCORRECTED_2X, COMPACT_2X, TELECENTRIC_3X, DOUBLE_CONVEX
from pyFPM.setup.Imaging_system import LED_calibration_parameters
from pyFPM.setup.Setup_parameters import Setup_parameters
from pyFPM.setup.Data import Data_patch, Rawdata, Preprocessed_data

import matplotlib.pyplot as plt
from pathlib import Path

main_folder = Path.cwd() / "data"/ "Illumination" 

def main():
    simulation = False
    real = True

    #infcor_2x(simulation, real)
    telecentric_3x(simulation, real)
    #double_convex(simulation, real)
    #compact_2x(simulation, real)

    plt.show()
    
def infcor_2x(simulation, real):
    lens = INFINITYCORRECTED_2X
    datadirpath = main_folder / "infinity_2x_illumnation"
    calibration_parameters = LED_calibration_parameters(200e-3,0e-6,0e-6,0)
    if simulation:
        illustrate_illumination_from_simulation(lens=lens, spherical=True, Fresnel=False, arraysize=5,
                                                calibration_parameters=calibration_parameters)
    if real:
        illustrate_illumination_from_setup(datadirpath=datadirpath, lens=lens, Fresnel=False,
                                        array_size=5, calibration_parameters=calibration_parameters)
    
def compact_2x(simulation, real):
    lens = COMPACT_2X
    datadirpath = main_folder / "compact_2x_illumination"
    calibration_parameters = LED_calibration_parameters(200e-3,0e-6,0e-6,0)
    if simulation:
        illustrate_illumination_from_simulation(lens=lens, spherical=True, Fresnel=True, arraysize=5,
                                                calibration_parameters=calibration_parameters)
    if real:
        illustrate_illumination_from_setup(datadirpath=datadirpath, lens=lens, Fresnel=True,
                                        array_size=5, calibration_parameters=calibration_parameters)
    
def telecentric_3x(simulation, real):
    lens = TELECENTRIC_3X
    datadirpath = main_folder / "telecentric_3x_illumination_2"
    calibration_parameters = LED_calibration_parameters(200e-3,0e-6,0e-6,0)
    if simulation:
        illustrate_illumination_from_simulation(lens=lens, spherical=True, Fresnel=False, arraysize=7,
                                                calibration_parameters=calibration_parameters)
    if real:
        illustrate_illumination_from_setup(datadirpath=datadirpath, lens=lens, Fresnel=False,
                                        array_size=7, calibration_parameters=calibration_parameters)
    
def double_convex(simulation, real):
    lens = DOUBLE_CONVEX
    datadirpath = main_folder / "double_convex_illumination"
    calibration_parameters = LED_calibration_parameters(200e-3,0e-6,0e-6,0)
    if simulation:
        illustrate_illumination_from_simulation(lens=lens, spherical=True, Fresnel=True, arraysize=5,
                                                calibration_parameters=calibration_parameters)
    if real:
        illustrate_illumination_from_setup(datadirpath=datadirpath, lens=lens, Fresnel=True,
                                        array_size=5, calibration_parameters=calibration_parameters)


def illustrate_illumination_from_simulation(lens, spherical, Fresnel, arraysize, calibration_parameters):
    setup_parameters, data_patch, imaging_system, illumination_pattern, applied_pupil, high_res_complex_object\
       = simulate_illumination(lens = lens, 
                               correct_spherical_wave_illumination = spherical, 
                               correct_Fresnel_propagation = Fresnel,
                               arraysize=arraysize,
                               calibration_parameters=calibration_parameters,
                               patch_offset=[0,0])

    fig = plot_bright_field_images_with_BF_edge(data_patch=data_patch, setup_parameters=setup_parameters, 
                                                calibration_parameters=calibration_parameters,
                                                array_size=arraysize, Fresnel=Fresnel)

    return fig

def illustrate_illumination_from_setup(datadirpath, lens, Fresnel, array_size, calibration_parameters):
    patch_offset = [0, 0] # [x, y]
    patch_size = [2048, 2048] # [x, y]

    camera = HAMAMATSU_C11440_42U30
    LED_array = MAIN_LED_ARRAY 

    setup_parameters: Setup_parameters = setup_parameters_from_file(
        datadirpath = datadirpath,
        lens = lens,
        camera = camera,
        LED_array = LED_array
        )

    rawdata: Rawdata = get_rawdata_from_files(
        datadirpath = datadirpath,
        image_format = setup_parameters.image_format,
        center_indices = setup_parameters.LED_info.center_indices,
        max_array_size = array_size,
        float_type = setup_parameters.camera.float_type
        )

    preprocessed_data = Preprocessed_data(
        rawdata = rawdata,
        setup_parameters = setup_parameters,
        noise_reduction_regions = None, 
        threshold_value = False
        )
    
    data_patch = Data_patch(
        data = preprocessed_data,
        raw_image_size = setup_parameters.camera.raw_image_size,
        patch_offset = patch_offset,
        patch_size = patch_size
        )

    fig = plot_bright_field_images_with_BF_edge(data_patch=data_patch, setup_parameters=setup_parameters, 
                                                calibration_parameters=calibration_parameters, 
                                                array_size=array_size, Fresnel=Fresnel)
    return fig

    
if __name__ == "__main__":
    main()
    
