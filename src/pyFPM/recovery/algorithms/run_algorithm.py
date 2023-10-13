from enum import Enum

from pyFPM.recovery.algorithms.fraunhofer_algorithm import fraunhofer_recovery_algorithm

class Method(Enum):
    Fraunhofer = 1
    Fraunhofer_Epry = 2
    Fraunhofer_Epry_Gradient_Descent = 3
    Fresnel = 4
    Fresnel_Epry = 5

def recover(method, data_patch, imaging_system, illumination_pattern, pupil_guess, loops):

    if method == Method.Fraunhofer:
        algorithm_result = fraunhofer_recovery_algorithm(
            data_patch = data_patch,
            imaging_system = imaging_system,
            illumination_pattern = illumination_pattern,
            pupil = pupil_guess,
            loops = loops
        )
    elif method == Method.Fraunhofer_Epry:
        algorithm_result = fraunhofer_recovery_algorithm(
            data_patch = data_patch,
            imaging_system = imaging_system,
            illumination_pattern = illumination_pattern,
            pupil = pupil_guess,
            loops = loops,
            use_epry = True,
            use_gradient_descent = False
        )
    elif method == Method.Fraunhofer_Epry_Gradient_Descent:
        algorithm_result = fraunhofer_recovery_algorithm(
            data_patch = data_patch,
            imaging_system = imaging_system,
            illumination_pattern = illumination_pattern,
            pupil = pupil_guess,
            loops = loops,
            use_epry = True,
            use_gradient_descent = True
        )
    else:
        raise "Recovery with specified method not implemented"

    return algorithm_result