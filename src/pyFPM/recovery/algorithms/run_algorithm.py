from enum import Enum

from pyFPM.recovery.algorithms.fraunhofer_algorithm import fraunhofer_recovery_algorithm

class Method(Enum):
    Fraunhofer = 1
    Fraunhofer_Epry = 2
    Pseudo_Fresnel = 3
    Pseudo_Fresnel_4f = 4
    Fresnel = 5
    Fresnel_4f = 6


def recover(method, data_patch, imaging_system, illumination_pattern, pupil_guess, step_description):

    if method == Method.Fraunhofer:
        algorithm_result = fraunhofer_recovery_algorithm(
            data_patch = data_patch,
            imaging_system = imaging_system,
            illumination_pattern = illumination_pattern,
            pupil_guess = pupil_guess,
            step_description = step_description,
            use_epry = False,
            correct_spherical_wave_phase = False,
            correct_Fresnel_phase = False,
            correct_aperture_shift = False 
        )
    elif method == Method.Fraunhofer_Epry:
        algorithm_result = fraunhofer_recovery_algorithm(
            data_patch = data_patch,
            imaging_system = imaging_system,
            illumination_pattern = illumination_pattern,
            pupil_guess = pupil_guess,
            step_description = step_description,
            use_epry = True,
            correct_spherical_wave_phase = False,
            correct_Fresnel_phase = False,
            correct_aperture_shift = False 
        )
    elif method == Method.Pseudo_Fresnel:
        algorithm_result = fraunhofer_recovery_algorithm(
            data_patch = data_patch,
            imaging_system = imaging_system,
            illumination_pattern = illumination_pattern,
            pupil_guess = pupil_guess,
            step_description = step_description,
            use_epry = True,
            correct_spherical_wave_phase = True,
            correct_Fresnel_phase = True,
            correct_aperture_shift = False 
        )
    elif method == Method.Pseudo_Fresnel_4f:
        algorithm_result = fraunhofer_recovery_algorithm(
            data_patch = data_patch,
            imaging_system = imaging_system,
            illumination_pattern = illumination_pattern,
            pupil_guess = pupil_guess,
            step_description = step_description,
            use_epry = True,
            correct_spherical_wave_phase = True,
            correct_Fresnel_phase = False,
            correct_aperture_shift = False 
        )
    elif method == Method.Fresnel:
        algorithm_result = fraunhofer_recovery_algorithm(
            data_patch = data_patch,
            imaging_system = imaging_system,
            illumination_pattern = illumination_pattern,
            pupil_guess = pupil_guess,
            step_description = step_description,
            use_epry = True,
            correct_spherical_wave_phase = True,
            correct_Fresnel_phase = True,
            correct_aperture_shift = True 
        )
    elif method == Method.Fresnel_4f:
        algorithm_result = fraunhofer_recovery_algorithm(
            data_patch = data_patch,
            imaging_system = imaging_system,
            illumination_pattern = illumination_pattern,
            pupil_guess = pupil_guess,
            step_description = step_description,
            use_epry = True,
            correct_spherical_wave_phase = True,
            correct_Fresnel_phase = False,
            correct_aperture_shift = True 
        )
    else:
        raise "Recovery with specified method not implemented"

    return algorithm_result