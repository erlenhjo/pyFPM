from pyFPM.setup.Data import Data_patch
from pyFPM.setup.Illumination_pattern import Illumination_pattern
from pyFPM.setup.Imaging_system import Imaging_system
from pyFPM.recovery.algorithms.Step_description import Step_description

import numpy as np
from scipy.ndimage import zoom


def extract_variables(data_patch: Data_patch, 
                      imaging_system: Imaging_system, 
                      illumination_pattern: Illumination_pattern,
                      step_description: Step_description):
    low_res_images = data_patch.amplitude_images
    update_order = illumination_pattern.update_order
    size_low_res_x = imaging_system.patch_size[0]
    size_low_res_y = imaging_system.patch_size[1]
    size_high_res_x = imaging_system.final_image_size[0]
    size_high_res_y = imaging_system.final_image_size[1]
    k_x = imaging_system.wavevectors_x()
    k_y = imaging_system.wavevectors_y()
    dk_x = imaging_system.differential_wavevectors_x()
    dk_y = imaging_system.differential_wavevectors_y()
    low_res_CTF = imaging_system.low_res_CTF
    scaling_factor_squared = (imaging_system.pixel_scale_factor)**2
    scaling_factor = imaging_system.pixel_scale_factor
    LED_indices = data_patch.LED_indices
    alpha = step_description.alpha
    beta = step_description.beta
    eta = step_description.eta
    use_adaptive_step_size = step_description.use_adaptive_step_size
    converged_alpha = step_description.converged_alpha
    max_iterations = step_description.max_iterations

    return low_res_images, update_order, size_low_res_x, size_low_res_y, size_high_res_x, size_high_res_y, k_x, k_y, dk_y, dk_x,\
            low_res_CTF, scaling_factor_squared, scaling_factor, LED_indices, alpha, beta, eta, use_adaptive_step_size, \
            converged_alpha, max_iterations


def initialize_high_res_image(low_res_images, update_order, scaling_factor):
    first_image = low_res_images[update_order[0]]
    
    recovered_object_guess = zoom(input=first_image, zoom=scaling_factor)
    #recovered_object_guess = np.ones(shape = [size*scaling_factor for size in first_image.shape])   
    
    return recovered_object_guess
