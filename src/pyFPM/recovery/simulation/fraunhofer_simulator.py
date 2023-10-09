from pyFPM.setup.Imaging_system import Imaging_system
from pyFPM.recovery.utility.k_space import calculate_k_vector_range

import numpy as np
from numpy.fft import fft2, ifft2, fftshift, ifftshift


def simulate_fraunhofer_imaging(high_resolution_object,
                                pupil,
                                LED_indices,
                                imaging_system: Imaging_system):
    
    size_high_res_x = imaging_system.final_image_size[0]
    size_high_res_y = imaging_system.final_image_size[1]
    size_low_res_x = imaging_system.patch_size[0]
    size_low_res_y = imaging_system.patch_size[1]
    inverse_scaling_factor_squared = (1/imaging_system.pixel_scale_factor)**2
    
    k_x = imaging_system.wavevectors_x()
    k_y = imaging_system.wavevectors_y()
    dk_x = imaging_system.differential_wavevectors_x()
    dk_y = imaging_system.differential_wavevectors_y()
    low_res_CTF = imaging_system.low_res_CTF

    high_res_fourier_transform = fftshift(fft2(ifftshift(high_resolution_object)))
    low_res_images = np.zeros(shape=(len(LED_indices), size_low_res_y, size_low_res_x))
    
    for image_nr in range(len(LED_indices)):
        # calculate which wavevector-values should be present in the low res image for LED_indices[image_nr]
        k_min_x, k_max_x, k_min_y, k_max_y = calculate_k_vector_range(k_x, k_y, dk_x, dk_y, size_low_res_x, size_low_res_y,
                                                                          size_high_res_x, size_high_res_y, LED_indices, image_nr)

        low_res_ft = inverse_scaling_factor_squared \
                     * high_res_fourier_transform[k_min_y:k_max_y+1, k_min_x:k_max_x+1] \
                     * low_res_CTF * pupil
        
        low_res_image =  np.abs(fftshift(ifft2(ifftshift(low_res_ft))))
        
        low_res_images[image_nr] = low_res_image
        
    
    return low_res_images