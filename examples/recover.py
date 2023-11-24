from enum import Enum
import matplotlib.pyplot as plt
import numpy as np

# FPM imports
from pyFPM.NTNU_specific.setup_2x_hamamatsu import setup_2x_hamamatsu
from pyFPM.NTNU_specific.setup_3x_telecentric_hamamatsu import setup_3x_telecentric_hamamatsu
from pyFPM.setup.Imaging_system import LED_calibration_parameters
from pyFPM.recovery.algorithms.run_algorithm import recover, Method
from pyFPM.aberrations.pupils.defocused_pupil import get_defocused_pupil
from pyFPM.recovery.algorithms.Step_description import get_standard_adaptive_step_description, get_constant_step_description

from pyFPM.simulation.simulate_imaging import simulate_angled_imaging
from pyFPM.setup.Data import Data_patch, Simulated_data

# utility imports
from plotting.plot_experimental_results import plot_experimental_results



#datadirpath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\20230825_USAFtarget"
# datadirpath = r"c:\Users\erlen\Documents\GitHub\pyFPM\data\EHJ20230915_dotarray_2x_inf"
# datadirpath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\dotarray_telecentric3x_dark"
# datadirpath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\USAF1951_centered_2x_infcorr"
# datadirpath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\USAF1951_centered_defocused_2x_infcorr"
# datadirpath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\USAF1951_corner_2x_infcorr"
# datadirpath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\USAF1951_corner_defocused_2x_infcorr"
# datadirpath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\USAF1951_plastic_2x_infcorr"
# datadirpath = r"c:\Users\erlen\Documents\GitHub\pyFPM\data\dotarray_2x_dark_no_object"

#datadirpath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\USAF_centered_infcor2x"
#datadirpath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\USAF_corner_infcor2x"

datadirpath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\telecentric_3x_usaf"

pixel_scale_factor = 8
patch_start = [300,896]#[896, 896] # [x, y]
patch_size = [256, 256] # [x, y]
remove_background = 1
threshold_value = 0.005
noise_reduction_regions = None# [[0,0], [1000,0]]

method = Method.Fraunhofer

setup_parameters, data_patch, imaging_system, illumination_pattern = setup_3x_telecentric_hamamatsu(
    datadirpath = datadirpath,
    patch_start = patch_start,
    patch_size = patch_size,
    pixel_scale_factor = pixel_scale_factor,
    remove_background = remove_background,
    threshold_value = threshold_value,
    noise_reduction_regions = noise_reduction_regions,
    calibration_parameters=LED_calibration_parameters(
        LED_distance=201e-3,
        LED_x_offset=0,
        LED_y_offset=0,
        LED_rotation=0
    )
)


# define step size method
step_description = get_standard_adaptive_step_description(illumination_pattern=illumination_pattern,
                                                          max_iterations=100,
                                                          start_EPRY_at_iteration = 2,
                                                          start_adaptive_at_iteration = 2)
# step_description = get_constant_step_description(max_iterations=20, start_EPRY_at_iteration=21)
# define pupil

defocus_guess = 0
pupil_guess = get_defocused_pupil(imaging_system = imaging_system, defocus = defocus_guess)


algorithm_result = recover(method=method, data_patch=data_patch, imaging_system=imaging_system,
                           illumination_pattern=illumination_pattern, pupil_guess=pupil_guess,
                           step_description=step_description)

plot_experimental_results(data_patch, illumination_pattern, imaging_system, algorithm_result)


plt.show()


