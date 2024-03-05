# FPM imports
from pyFPM.NTNU_specific.setup_USN import setup_USN
from pyFPM.setup.Imaging_system import LED_calibration_parameters
from pyFPM.recovery.algorithms.run_algorithm import recover, Method
from pyFPM.aberrations.pupils.defocused_pupil import get_defocused_pupil
from pyFPM.recovery.algorithms.Step_description import get_standard_adaptive_step_description

# utility imports
from plot_results import plot_results

import numpy as np
import matplotlib.pyplot as plt


def recover_USN_phase_target(patch_shift, title):
    method = Method.Fresnel_aperture
    datadirpath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\Master_thesis\USN\Basler_PhaseTarget2"

    setup_parameters, data_patch, imaging_system, illumination_pattern \
        = setup_USN(datadirpath=datadirpath,
                    patch_shift=np.array(patch_shift),
                    patch_size=np.array([512,512]),
                    calibration_parameters = LED_calibration_parameters(
                        LED_distance=83e-3,
                        LED_x_offset=0,
                        LED_y_offset=0,
                        LED_rotation=0
                        ),
                    noise_threshold = 1800
                    )

    step_description = get_standard_adaptive_step_description(illumination_pattern=illumination_pattern,
                                                            max_iterations=50,
                                                            start_EPRY_at_iteration = 0,
                                                            start_adaptive_at_iteration = 0)
    step_description.alpha=1
    step_description.beta=1

    pupil_guess = get_defocused_pupil(imaging_system = imaging_system, defocus = 0)

    algorithm_result = recover(method=method, data_patch=data_patch, imaging_system=imaging_system,
                            illumination_pattern=illumination_pattern, pupil_guess=pupil_guess,
                            step_description=step_description)

    plot_results(data_patch, illumination_pattern, imaging_system, algorithm_result, title)
    return


if __name__ == "__main__":
    recover_USN_phase_target([0,0], "USN phase target centered")
    #recover_USN_phase_target([0,-750], "USN phase target edge")
    plt.show()