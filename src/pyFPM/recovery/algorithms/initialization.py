from pyFPM.setup.Data import Data_patch
from pyFPM.setup.Illumination_pattern import Illumination_pattern
from pyFPM.setup.Imaging_system import Imaging_system
from pyFPM.recovery.algorithms.Step_description import Step_description

import numpy as np
from scipy.ndimage import zoom


def extract_variables(data_patch: Data_patch, 
                      imaging_system: Imaging_system, 
                      illumination_pattern: Illumination_pattern,
                      step_description: Step_description,
                      correct_aperture_shift: bool):
    low_res_images = data_patch.amplitude_images
    update_order = illumination_pattern.update_order
    size_low_res_x = imaging_system.patch_size[0]
    size_low_res_y = imaging_system.patch_size[1]
    size_high_res_x = imaging_system.final_image_size[0]
    size_high_res_y = imaging_system.final_image_size[1]

    if not correct_aperture_shift:
        shifts_x = imaging_system.LED_shifts_x
        shifts_y = imaging_system.LED_shifts_y
    else: 
        shifts_x = imaging_system.LED_shifts_x_aperture
        shifts_y = imaging_system.LED_shifts_y_aperture

    low_res_CTF = imaging_system.low_res_CTF
    scaling_factor_squared = (imaging_system.pixel_scale_factor)**2
    scaling_factor = imaging_system.pixel_scale_factor
    LED_indices = data_patch.LED_indices
    alpha = step_description.alpha
    beta = step_description.beta
    eta = step_description.eta
    start_EPRY_at_iteration = step_description.start_EPRY_at_iteration
    start_adaptive_steps_at_iteration = step_description.start_adaptive_at_iteration
    converged_alpha = step_description.converged_alpha
    max_iterations = step_description.max_iterations



    return low_res_images, update_order, size_low_res_x, size_low_res_y, size_high_res_x, size_high_res_y, shifts_x, shifts_y,\
            low_res_CTF, scaling_factor_squared, scaling_factor, LED_indices, alpha, beta, eta, start_EPRY_at_iteration,\
            start_adaptive_steps_at_iteration, converged_alpha, max_iterations


def initialize_high_res_image(low_res_images, update_order, scaling_factor, object_phase_correction):
    first_image = low_res_images[update_order[0]]
    
    recovered_object_guess = zoom(input=first_image, zoom=scaling_factor) * object_phase_correction
    recovered_object_guess = np.ones(shape=recovered_object_guess.shape) * object_phase_correction

    return recovered_object_guess
