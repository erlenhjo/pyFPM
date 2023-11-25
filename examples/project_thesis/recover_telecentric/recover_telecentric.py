# FPM imports
from pyFPM.NTNU_specific.setup_3x_telecentric_hamamatsu import setup_3x_telecentric_hamamatsu
from pyFPM.setup.Imaging_system import LED_calibration_parameters
from pyFPM.recovery.algorithms.run_algorithm import recover, Method
from pyFPM.aberrations.pupils.defocused_pupil import get_defocused_pupil
from pyFPM.recovery.algorithms.Step_description import get_standard_adaptive_step_description, get_constant_step_description

# utility imports
from plot_results import plot_results




def recover_telecentric(noise_reduction: bool, adaptive: bool, epry: bool, aperture):
    datadirpath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\telecentric_3x_usaf"
    pixel_scale_factor = 8
    patch_start = [896, 896] # [x, y]
    patch_size = [256, 256] # [x, y]
    defocus_guess = 0

    if noise_reduction:
        remove_background = 1
        threshold_value = 0.005
        noise_reduction_regions = None
    else:
        remove_background = 0
        threshold_value = 0
        noise_reduction_regions = None

    if not epry:
        if not aperture:
            method = Method.Fraunhofer
        else:
            method = Method.Fraunhofer_aperture
    else: 
        if not aperture:
            method = Method.Fraunhofer_Epry
        else:
            method = Method.Fraunhofer_Epry_aperture

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


    if adaptive: 
        step_description = get_standard_adaptive_step_description(illumination_pattern=illumination_pattern,
                                                                max_iterations=50,
                                                                start_EPRY_at_iteration = 2,
                                                                start_adaptive_at_iteration = 2)
    else:
        step_description = get_constant_step_description(max_iterations=50, start_EPRY_at_iteration=2)


    pupil_guess = get_defocused_pupil(imaging_system = imaging_system, defocus = defocus_guess)


    algorithm_result = recover(method=method, data_patch=data_patch, imaging_system=imaging_system,
                            illumination_pattern=illumination_pattern, pupil_guess=pupil_guess,
                            step_description=step_description)

    plot_results(data_patch, illumination_pattern, imaging_system, algorithm_result)
