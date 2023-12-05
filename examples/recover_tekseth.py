import matplotlib.pyplot as plt

# FPM imports
from pyFPM.NTNU_specific.setup_2x_hamamatsu import setup_2x_hamamatsu
from pyFPM.setup.Imaging_system import LED_calibration_parameters
from pyFPM.recovery.algorithms.run_algorithm import recover, Method
from pyFPM.aberrations.pupils.defocused_pupil import get_defocused_pupil
from pyFPM.recovery.algorithms.Step_description import get_standard_adaptive_step_description, get_constant_step_description


# utility imports
from plotting.plot_experimental_results import plot_experimental_results



datadirpath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\Fourier_Ptychography\KRT20220805_phaseTarget"


pixel_scale_factor = 6
patch_start = [399, 949]
patch_size = [256, 256]
remove_background = True
threshold_value = 0.05
noise_reduction_regions = None #[[1151,562], [1238,1203]]

method = Method.Fraunhofer_Epry

setup_parameters, data_patch, imaging_system, illumination_pattern = setup_2x_hamamatsu(
    datadirpath = datadirpath,
    patch_start = patch_start,
    patch_size = patch_size,
    pixel_scale_factor = pixel_scale_factor,
    remove_background = remove_background,
    threshold_value = threshold_value,
    noise_reduction_regions = noise_reduction_regions,
    calibration_parameters=LED_calibration_parameters(
        LED_distance=193e-3,
        LED_x_offset=0,
        LED_y_offset=0,
        LED_rotation=0
    )
)

# plot_bright_field_images(data_patch=data_patch, setup_parameters=setup_parameters, array_size=5)
# plt.show()
# define step size method
step_description = get_standard_adaptive_step_description(illumination_pattern=illumination_pattern,
                                                          max_iterations=100,
                                                          start_EPRY_at_iteration = 2,
                                                          start_adaptive_at_iteration = 2)
# step_description = get_constant_step_description(max_iterations=20, start_EPRY_at_iteration=21)
# define pupil

defocus_guess = 6e-5
pupil_guess = get_defocused_pupil(imaging_system = imaging_system, defocus = defocus_guess)


algorithm_result = recover(method=method, data_patch=data_patch, imaging_system=imaging_system,
                           illumination_pattern=illumination_pattern, pupil_guess=pupil_guess,
                           step_description=step_description)

plot_experimental_results(data_patch, illumination_pattern, imaging_system, algorithm_result)


plt.show()


