from enum import Enum

from pyFPM.recovery.algorithms.standard_algorithm import standard_recovery_algorithm

class Method(Enum):
    Fraunhofer_with_illumination = 1
    Fresnel = 2


def recover(method, data_patch, imaging_system, illumination_pattern, 
            pupil_guess, step_description):

    if method == Method.Fraunhofer_with_illumination:
        algorithm_result = standard_recovery_algorithm(
            data_patch = data_patch,
            imaging_system = imaging_system,
            illumination_pattern = illumination_pattern,
            pupil_guess = pupil_guess,
            step_description = step_description,
            correct_spherical_wave_phase = True,
            correct_Fresnel_phase = False,
            use_Fresnel_shifts = False
        )
    elif method == Method.Fresnel:
        algorithm_result = standard_recovery_algorithm(
            data_patch = data_patch,
            imaging_system = imaging_system,
            illumination_pattern = illumination_pattern,
            pupil_guess = pupil_guess,
            step_description = step_description,
            correct_spherical_wave_phase = True,
            correct_Fresnel_phase = True,
            use_Fresnel_shifts = True
        )


    else:
        raise "Recovery with specified method not implemented"

    return algorithm_result