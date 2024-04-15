from enum import Enum
import matplotlib.pyplot as plt
import numpy as np
import skimage

# FPM imports
from pyFPM.NTNU_specific.simulate_images.simulate_2x import simulate_2x
from pyFPM.recovery.calibration.positional_calibration import positional_calibration_recovery_algorithm
from pyFPM.setup.Imaging_system import LED_calibration_parameters

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


# pixel_scale_factor = 4
# patch_start = [900, 900] # [x, y]
# patch_size = [256, 256] # [x, y]
# remove_background = False
# threshold_value = 0

# setup_parameters, data_patch, imaging_system, illumination_pattern = setup_2x_hamamatsu(
#     datadirpath = datadirpath,
#     patch_start = patch_start,
#     patch_size = patch_size,
#     pixel_scale_factor = pixel_scale_factor,
#     remove_background = remove_background,
#     threshold_value = threshold_value 
# )


amplitude_image = skimage.data.camera()
phase_image = np.zeros(shape=amplitude_image.shape)
high_res_complex_object = amplitude_image * np.exp(1j*phase_image)

setup_parameters, data_patch, imaging_system, illumination_pattern, applied_pupil, _\
    = simulate_2x(high_res_complex_object, noise_fraction=0, zernike_coefficients=[0], spherical_illumination=False)

assumed_LED_calibration_parameters = LED_calibration_parameters(200e-3,0,0,0)

algorithm_result, calibration_values = positional_calibration_recovery_algorithm(data_patch=data_patch,
                                                             imaging_system=imaging_system,
                                                             illumination_pattern=illumination_pattern,
                                                             setup_parameters=setup_parameters,
                                                             assumed_LED_calibration_parameters=assumed_LED_calibration_parameters)


plot_experimental_results(data_patch, illumination_pattern, imaging_system, algorithm_result)
print(calibration_values)

plt.show()


