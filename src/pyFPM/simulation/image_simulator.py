from pyFPM.setup.Imaging_system import Imaging_system
from pyFPM.recovery.utility.k_space import calculate_low_res_index_range

import numpy as np
from numpy.fft import ifft2, fftshift, ifftshift


def simulate_angled_imaging(high_res_fourier_transform,
                            pupil,
                            LED_indices,
                            imaging_system: Imaging_system,
                            use_aperture_shift = False
                            ):
    
    size_high_res_x = imaging_system.final_image_size[0]
    size_high_res_y = imaging_system.final_image_size[1]
    size_low_res_x = imaging_system.patch_size[0]
    size_low_res_y = imaging_system.patch_size[1]
    inverse_scaling_factor_squared = (1/imaging_system.pixel_scale_factor)**2

    if not use_aperture_shift:
        shifts_x = imaging_system.LED_shifts_x
        shifts_y = imaging_system.LED_shifts_y
    else: 
        shifts_x = imaging_system.LED_shifts_x_aperture
        shifts_y = imaging_system.LED_shifts_y_aperture
    
    
    low_res_CTF = imaging_system.low_res_CTF

    low_res_images = np.zeros(shape=(len(LED_indices), size_low_res_y, size_low_res_x))

    
    for image_nr in range(len(LED_indices)):
        # calculate which wavevector-values should be present in the low res image for LED_indices[image_nr]
        k_min_x, k_max_x, k_min_y, k_max_y = calculate_low_res_index_range(shifts_x, shifts_y, size_low_res_x, size_low_res_y,
                                                                          size_high_res_x, size_high_res_y, LED_indices, image_nr)

        low_res_ft = inverse_scaling_factor_squared \
                     * high_res_fourier_transform[k_min_y:k_max_y+1, k_min_x:k_max_x+1] \
                     * low_res_CTF * pupil
        
        low_res_image =  np.abs(fftshift(ifft2(ifftshift(low_res_ft))))

        low_res_images[image_nr] = low_res_image
        
        
    return low_res_images


