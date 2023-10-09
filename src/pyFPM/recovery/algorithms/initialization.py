from pyFPM.setup.Data import Data_patch
from pyFPM.setup.Illumination_pattern import Illumination_pattern
from pyFPM.setup.Imaging_system import Imaging_system

import numpy as np


def extract_variables(data_patch: Data_patch, imaging_system: Imaging_system, illumination_pattern: Illumination_pattern):
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

    return low_res_images, update_order, size_low_res_x, size_low_res_y, size_high_res_x, size_high_res_y, k_x, k_y, dk_y, dk_x,\
            low_res_CTF, scaling_factor_squared, scaling_factor, LED_indices


def initialize_high_res_image(low_res_images, update_order, scaling_factor):
    ones = np.ones(shape = (scaling_factor, scaling_factor))
    first_image = low_res_images[update_order[0]]
    recovered_object_guess = np.kron(first_image, ones)
    return recovered_object_guess
