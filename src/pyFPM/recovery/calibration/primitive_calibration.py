import numpy as np
import matplotlib.pyplot as plt
from enum import Enum
 
from pyFPM.setup.Data import Data_patch
from pyFPM.setup.Illumination_pattern import Illumination_pattern
from pyFPM.setup.Imaging_system import Imaging_system, LED_calibration_parameters
from pyFPM.setup.Setup_parameters import Setup_parameters
from pyFPM.recovery.utility.real_space_error import compute_sum_square_error
from pyFPM.aberrations.pupils.defocused_pupil import get_defocused_pupil
from pyFPM.recovery.algorithms.Step_description import get_standard_adaptive_step_description

from pyFPM.recovery.algorithms.run_algorithm import recover


class Parameter(Enum):
    Defocus = 0
    LED_x = 1
    LED_y = 2
    LED_z = 3
    LED_rotation = 4

def primitive_calibration(
        data_patch: Data_patch,
        setup_parameters: Setup_parameters,
        illumination_pattern: Illumination_pattern,
        defocus_guess,
        rotation_guess,
        distance_offset_guess,
        LED_x_offset_guess,
        LED_y_offset_guess,
        patch_start,
        patch_size,
        pixel_scale_factor,
        parameter_to_calibrate,
        number_of_steps,
        method
    ):
    max_iterations = 30
    step_description = get_standard_adaptive_step_description(max_iterations=max_iterations, 
                                                              start_EPRY_at_iteration=max_iterations+1,
                                                              start_adaptive_at_iteration=max_iterations+1)

    best_image = None
    best_image_defocus = None
    best_image_LED_calibration_parameters = None
    errors = []

    defocus_range, LED_calibration_parameter_range, calibration_parameter_range = get_calibration_parameters(defocus_guess,
                                                                                                             rotation_guess,
                                                                                                             distance_offset_guess,
                                                                                                             LED_x_offset_guess,
                                                                                                             LED_y_offset_guess,
                                                                                                             parameter_to_calibrate,
                                                                                                             number_of_steps
                                                                                                            )

    for defocus, calibration_parameters in zip(defocus_range, LED_calibration_parameter_range):

        imaging_system = Imaging_system(setup_parameters=setup_parameters,
                                        pixel_scale_factor=pixel_scale_factor,
                                        patch_start=patch_start,
                                        patch_size=patch_size,
                                        LED_calibration_parameters = calibration_parameters)
        pupil_guess = get_defocused_pupil(imaging_system=imaging_system, defocus=defocus)

        algorithm_results = recover(
            method = method,
            data_patch = data_patch,
            imaging_system = imaging_system,
            illumination_pattern = illumination_pattern,
            pupil_guess = pupil_guess,
            step_description=step_description
            )
        
        sum_square_error = compute_sum_square_error(
            data_patch = data_patch,
            imaging_system=imaging_system,
            illumination_pattern=illumination_pattern,
            algorithm_result=algorithm_results
        )

        if best_image is None:
            best_image = np.abs(algorithm_results.recovered_object)**2
            best_image_defocus = defocus
            best_image_LED_calibration_parameters = calibration_parameters
        elif sum_square_error < min(errors):
            best_image = np.abs(algorithm_results.recovered_object)**2
            best_image_defocus = defocus
            best_image_LED_calibration_parameters = calibration_parameters
        
        errors.append(sum_square_error)

    plt.figure()
    plt.title(f"Best image")
    plt.imshow(best_image)
    plt.axis("off")

    plt.figure()
    plt.scatter(calibration_parameter_range, errors)
    plt.title("Sum square error")
    plt.ylabel("SSE [a.u.]")

    print(best_image_defocus)
    print(best_image_LED_calibration_parameters)

    plt.show()


def get_calibration_parameters(
        defocus_guess,
        LED_rotation_guess,
        LED_distance_offset_guess,
        LED_x_offset_guess,
        LED_y_offset_guess,
        parameter_to_calibrate: Parameter,
        number_of_steps
        ):

    if parameter_to_calibrate == Parameter.Defocus:
        defocus_range = np.linspace(-1,1,number_of_steps) * 20e-6 + defocus_guess
        calibration_parameters =  [LED_calibration_parameters(LED_distance_offset_guess,
                                                              LED_x_offset_guess,
                                                              LED_y_offset_guess,
                                                              LED_rotation_guess)] * number_of_steps
        calibration_parameter_range = defocus_range
        
    elif parameter_to_calibrate == Parameter.LED_rotation:
        defocus_range = [defocus_guess] * number_of_steps
        calibration_parameters = [] 
        rotation_range = np.linspace(-1,1,number_of_steps) * 0.5 + LED_rotation_guess
        for current_guess in rotation_range:
            calibration_parameters.append(LED_calibration_parameters(LED_distance_offset_guess,
                                                              LED_x_offset_guess,
                                                              LED_y_offset_guess,
                                                              current_guess))
        calibration_parameter_range = calibration_parameter_range
            
    elif parameter_to_calibrate == Parameter.LED_x:
        defocus_range = [defocus_guess] * number_of_steps
        calibration_parameters = [] 
        x_range = np.linspace(-1,1,number_of_steps) * 50e-6 + LED_x_offset_guess
        for current_guess in x_range:
            calibration_parameters.append(LED_calibration_parameters(LED_distance_offset_guess,
                                                              current_guess,
                                                              LED_y_offset_guess,
                                                              LED_rotation_guess))
        calibration_parameter_range = x_range
            
    elif parameter_to_calibrate == Parameter.LED_y:
        defocus_range = [defocus_guess] * number_of_steps
        calibration_parameters = [] 
        y_range = np.linspace(-1,1,number_of_steps) * 50e-6 + LED_y_offset_guess
        for current_guess in y_range:
            calibration_parameters.append(LED_calibration_parameters(LED_distance_offset_guess,
                                                              LED_x_offset_guess,
                                                              current_guess,
                                                              LED_rotation_guess))
        calibration_parameter_range = y_range
            
    elif parameter_to_calibrate == Parameter.LED_z:
        defocus_range = [defocus_guess] * number_of_steps
        calibration_parameters = [] 
        z_range = np.linspace(-1,1,number_of_steps) * 10e-3 + LED_distance_offset_guess
        for current_guess in z_range:
            calibration_parameters.append(LED_calibration_parameters(current_guess,
                                                              LED_x_offset_guess,
                                                              LED_y_offset_guess,
                                                              LED_rotation_guess))
        calibration_parameter_range = z_range
            
    return defocus_range, calibration_parameters, calibration_parameter_range