import matplotlib.pyplot as plt
import numpy as np

from pyFPM.visualization.plot_illumination import plot_bright_field_images
from pyFPM.NTNU_specific.simulate_images.only_illumination import simulate_illumination
from pyFPM.NTNU_specific.setup_from_file import setup_parameters_from_file
from pyFPM.NTNU_specific.rawdata_from_files import get_rawdata_from_files
from pyFPM.NTNU_specific.components import HAMAMATSU_C11440_42U30, MAIN_LED_ARRAY
from pyFPM.setup.Imaging_system import LED_calibration_parameters
from pyFPM.setup.Setup_parameters import Setup_parameters
from pyFPM.setup.Data import Data_patch, Rawdata, Preprocessed_data

def illustrate_illumination_from_simulation(lens, spherical, Fresnel, z_LED, arraysize, patch_offset=[0,0], use_working_distance=False):
    setup_parameters, data_patch, imaging_system, illumination_pattern, applied_pupil, high_res_complex_object\
       = simulate_illumination(lens = lens, 
                               correct_spherical_wave_illumination = spherical, 
                               correct_Fresnel_propagation = Fresnel,
                               arraysize=arraysize,
                               calibration_parameters=LED_calibration_parameters(z_LED,0,0,0),
                               patch_offset=patch_offset)
    fig = plot_bright_field_images(data_patch=data_patch, setup_parameters=setup_parameters, array_size=arraysize)

    return fig

def illustrate_illumination_from_setup(datadirpath, lens, array_size):
    patch_start = [0, 0] # [x, y]
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
        datadirpath = datadirpath
        )

    preprocessed_data = Preprocessed_data(
        rawdata = rawdata,
        setup_parameters = setup_parameters,
        remove_background = False,
        noise_reduction_regions = None, 
        threshold_value = False
        )
    
    data_patch = Data_patch(
        data = preprocessed_data,
        patch_start = patch_start,
        patch_size = patch_size
        )

    fig = plot_bright_field_images(data_patch=data_patch, setup_parameters=setup_parameters, array_size=array_size)
    return fig

    

    
