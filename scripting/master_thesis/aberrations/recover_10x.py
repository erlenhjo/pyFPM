# FPM imports
from pyFPM.NTNU_specific.setup_IDS_U3 import setup_IDS_U3
from pyFPM.NTNU_specific.components import INFINITYCORRECTED_10X
from pyFPM.setup.Imaging_system import LED_calibration_parameters
from pyFPM.recovery.algorithms.run_algorithm import recover, Method
from pyFPM.aberrations.pupils.defocused_pupil import get_defocused_pupil
from pyFPM.recovery.algorithms.Step_description import get_standard_adaptive_step_description

# utility imports
from plot_results import plot_results
import os

def recover_10x(title, datadirpath, patch_start, patch_size, max_array_size, result_folder):
    pixel_scale_factor = 4
    remove_background = 1
    threshold_value = 0.005
    noise_reduction_regions = None
    method = Method.Fresnel_illumination_only

    setup_parameters, data_patch, imaging_system, illumination_pattern = setup_IDS_U3(
        lens = INFINITYCORRECTED_10X,
        datadirpath = datadirpath,
        patch_start = patch_start,
        patch_size = patch_size,
        pixel_scale_factor = pixel_scale_factor,
        remove_background = remove_background,
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


    step_description = get_standard_adaptive_step_description(illumination_pattern=illumination_pattern,
                                                            max_iterations=50,
                                                            start_EPRY_at_iteration = 0,
                                                            start_adaptive_at_iteration = 10)


    pupil_guess = get_defocused_pupil(imaging_system = imaging_system, defocus = 0)

    algorithm_result = recover(method=method, data_patch=data_patch, imaging_system=imaging_system,
                            illumination_pattern=illumination_pattern, pupil_guess=pupil_guess,
                            step_description=step_description)

    fig = plot_results(data_patch, illumination_pattern, imaging_system, algorithm_result, title)
    fig.savefig(os.path.join(result_folder,title.replace(" ","_")+".png"))
    return
