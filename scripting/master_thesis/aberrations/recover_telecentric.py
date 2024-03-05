# FPM imports
from pyFPM.NTNU_specific.setup_IDS_U3 import setup_IDS_U3
from pyFPM.NTNU_specific.components import TELECENTRIC_3X
from pyFPM.setup.Imaging_system import LED_calibration_parameters
from pyFPM.recovery.algorithms.run_algorithm import recover, Method
from pyFPM.aberrations.pupils.defocused_pupil import get_defocused_pupil
from pyFPM.recovery.algorithms.Step_description import get_standard_adaptive_step_description

# utility imports
from plot_results import plot_results
import os
import numpy as np

def recover_telecentric(title, datadirpath, patch_start, patch_size, max_array_size, result_folder):
    pixel_scale_factor = 6
    threshold_value = 1000
    noise_reduction_regions = [
        [1100, 1100, 100, 100],
        [1600, 1600, 100, 100]
    ]
    method = Method.Fresnel_illumination_only

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


    step_description = get_standard_adaptive_step_description(illumination_pattern=illumination_pattern,
                                                            max_iterations=2,
                                                            start_EPRY_at_iteration = 0,
                                                            start_adaptive_at_iteration = 10)

    pupil_guess = get_defocused_pupil(imaging_system = imaging_system, defocus = 0)

    algorithm_result = recover(method=method, data_patch=data_patch, imaging_system=imaging_system,
                            illumination_pattern=illumination_pattern, pupil_guess=pupil_guess,
                            step_description=step_description)

    fig = plot_results(data_patch, illumination_pattern, imaging_system, algorithm_result, title)
    fig.savefig(os.path.join(result_folder,title.replace(" ","_")+".png"))
    return
