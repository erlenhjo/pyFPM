# pyFPM imports
from pyFPM.NTNU_specific.setup_IDS_U3 import setup_IDS_U3
from pyFPM.NTNU_specific.components import TELECENTRIC_3X
from pyFPM.recovery.calibration.primitive_calibration import primitive_calibration, Parameter
from pyFPM.setup.Imaging_system import LED_calibration_parameters
from pyFPM.recovery.algorithms.run_algorithm import recover, Method

import numpy as np

#datadirpath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\USAF_centered_infcor2x"
datadirpath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\Master_thesis\aberrations_040324\usaf_3x_tele_m20"


patch_start = np.array([2848, 2844], dtype=int) // 2 - np.array([256+128,128])
patch_size = [256, 256]
max_array_size = 7
pixel_scale_factor = 6
method = Method.Fresnel_illumination_only
threshold_value = 1000
noise_reduction_regions = [
    [1100, 1100, 100, 100],
    [1600, 1600, 100, 100]
]


setup_parameters, data_patch, imaging_system, illumination_pattern = setup_IDS_U3(
    lens = TELECENTRIC_3X,
    datadirpath = datadirpath,
    patch_start = patch_start,
    patch_size = patch_size,
    pixel_scale_factor = pixel_scale_factor,
    threshold_value = threshold_value,
    noise_reduction_regions = noise_reduction_regions,
    calibration_parameters=LED_calibration_parameters(
        LED_distance=200e-3,
        LED_x_offset=0,
        LED_y_offset=0,
        LED_rotation=0
    ),
    max_array_size = max_array_size
)



defocus_guess = 0e-6
rotation_guess = 0
distance_offset_guess = 200e-3
LED_x_offset_guess = 0e-3
LED_y_offset_guess = 0e-3

parameter_to_calibrate = Parameter.Defocus
number_of_steps = 20

primitive_calibration(
    data_patch,
    setup_parameters,
    illumination_pattern,
    defocus_guess,
    rotation_guess,
    distance_offset_guess,
    LED_x_offset_guess,
    LED_y_offset_guess,
    patch_start,
    patch_size,
    pixel_scale_factor,
    parameter_to_calibrate,
    number_of_steps,
    method = method
)





