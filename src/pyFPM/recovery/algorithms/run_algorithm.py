from enum import Enum

from pyFPM.recovery.algorithms.primitive_algorithm import primitive_fourier_ptychography_algorithm

class Method(Enum):
    Primitive = 1
    Epry = 2
    Epry_Gradient_Descent = 3
    Fresnel = 4
    Fresnel_Epry = 5

def recover(method, data_patch, imaging_system, illumination_pattern, pupil_guess, loops):

    if method == Method.Primitive:
        algorithm_result = primitive_fourier_ptychography_algorithm(
            data_patch = data_patch,
            imaging_system = imaging_system,
            illumination_pattern = illumination_pattern,
            pupil = pupil_guess,
            loops = loops
        )
    elif method == Method.Epry:
        algorithm_result = primitive_fourier_ptychography_algorithm(
            data_patch = data_patch,
            imaging_system = imaging_system,
            illumination_pattern = illumination_pattern,
            pupil = pupil_guess,
            loops = loops,
            use_epry = True,
            use_gradient_descent = False
        )
    elif method == Method.Epry_Gradient_Descent:
        algorithm_result = primitive_fourier_ptychography_algorithm(
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