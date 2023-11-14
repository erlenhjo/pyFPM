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
from plotting.plot_illumination import plot_bright_field_images


#datadirpath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\20230825_USAFtarget"
# datadirpath = r"c:\Users\erlen\Documents\GitHub\pyFPM\data\EHJ20230915_dotarray_2x_inf"
# datadirpath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\dotarray_telecentric3x_dark"
# datadirpath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\USAF1951_centered_2x_infcorr"
# datadirpath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\USAF1951_centered_defocused_2x_infcorr"
# datadirpath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\USAF1951_corner_2x_infcorr"
# datadirpath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\USAF1951_corner_defocused_2x_infcorr"
# datadirpath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\USAF1951_plastic_2x_infcorr"
# datadirpath = r"c:\Users\erlen\Documents\GitHub\pyFPM\data\dotarray_2x_dark_no_object"

datadirpath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\USAF_centered_infcor2x"


pixel_scale_factor = 4
patch_start = [964, 964] # [x, y]
patch_size = [128, 128] # [x, y]
remove_background = 1
threshold_value = 0

method = Method.Fraunhofer_Epry_aperture

setup_parameters, data_patch, imaging_system, illumination_pattern = setup_2x_hamamatsu(
    datadirpath = datadirpath,
    patch_start = patch_start,
    patch_size = patch_size,
    pixel_scale_factor = pixel_scale_factor,
    remove_background = remove_background,
    threshold_value = threshold_value,
    calibration_parameters=LED_calibration_parameters(
        LED_distance=201e-3,
        LED_x_offset=0,
        LED_y_offset=0,
        LED_rotation=0
    )
)

# define step size method
step_description = get_standard_adaptive_step_description(illumination_pattern=illumination_pattern,
                                                          max_iterations=200,
                                                          start_EPRY_at_iteration = 0,
                                                          start_adaptive_at_iteration = 0)
# step_description = get_constant_step_description(max_iterations=20, start_EPRY_at_iteration=21)
# define pupil
defocus_guess = 0
pupil_guess = get_defocused_pupil(imaging_system = imaging_system, defocus = defocus_guess)

#plot_bright_field_images(data_patch=data_patch, setup_parameters=setup_parameters, array_size=7)

algorithm_result = recover(method=method, data_patch=data_patch, imaging_system=imaging_system,
                           illumination_pattern=illumination_pattern, pupil_guess=pupil_guess,
                           step_description=step_description)

# for image in data_patch.amplitude_images:
#     plt.matshow(image)

# recovered_low_res_images \
#         = simulate_angled_imaging(
#             algorithm_result.recovered_object_fourier_transform,
#             algorithm_result.pupil,
#             data_patch.LED_indices,
#             imaging_system)
    
# recovered_low_res_data = Simulated_data(LED_indices=data_patch.LED_indices, amplitude_images=recovered_low_res_images)

# recovered_data_patch = Data_patch(data = recovered_low_res_data, patch_start=[0, 0], patch_size=recovered_low_res_images[0].shape)

# plot_bright_field_images(data_patch=recovered_data_patch, setup_parameters=setup_parameters, array_size=7)

plot_experimental_results(data_patch, illumination_pattern, imaging_system, algorithm_result)
# fig, axes = plt.subplots(nrows=1, ncols=2, layout='constrained')
# axes: list[plt.Axes] = axes.flatten()
# axes[0].set_title(f"Recovered image")
# axes[0].matshow(np.abs(algorithm_result.recovered_object)**2)    
# axes[0].axis("off")
# axes[0].margins(x=0, y=0)
# axes[1].set_title(f"Recovered phase")
# axes[1].matshow(np.angle(algorithm_result.recovered_object), vmin=-np.pi, vmax=np.pi)    
# axes[1].axis("off")
# axes[1].margins(x=0, y=0)

plt.show()


