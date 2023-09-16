import numpy as np
from numpy.fft import ifft2, ifftshift, fft2, fftshift

from pyFPM.setup.Preprocessed_data import Preprocessed_data
from pyFPM.setup.Illumination_pattern import Illumination_pattern
from pyFPM.setup.Imaging_system import Imaging_system
from pyFPM.recovery.algorithms.Algorithm_result import Algorithm_result

def computeFPMerror(preprocessed_data: Preprocessed_data, imaging_system: Imaging_system, 
                            illumination_pattern: Illumination_pattern, algorithm_result: Algorithm_result):
    
    low_res_images = preprocessed_data.amplitude_images
    recovered_object = algorithm_result.recovered_object
    pupil = algorithm_result.pupil

    update_order = illumination_pattern.update_order  # order does not matter, but this is a list only of "active" LEDs
    size_low_res_x = imaging_system.patch_size[0]
    size_low_res_y = imaging_system.patch_size[1]
    size_high_res_x = imaging_system.final_image_size[0]
    size_high_res_y = imaging_system.final_image_size[1]
    k_x = imaging_system.wavevectors_x()
    k_y = imaging_system.wavevectors_y()
    dk_x = imaging_system.differential_wavevectors_x()
    dk_y = imaging_system.differential_wavevectors_y()
    low_res_CTF = imaging_system.low_res_CTF
    inverse_scaling_factor = 1 / imaging_system.pixel_scale_factor
    LED_indices = preprocessed_data.LED_indices

    weighted_object_ft = np.mean(low_res_images[update_order[0]])\
                    / np.mean((np.abs(recovered_object))) * recovered_object
    
    recovered_object_ft = fftshift(fft2(fftshift(weighted_object_ft)))

    error_estimate = 0
    e1=0
    e2=0
    for image_nr in range(len(update_order)):
        index = update_order[image_nr]
        LED_index_x = LED_indices[index][0]
        LED_index_y = LED_indices[index][1]

        raw_low_res_image = low_res_images[index]

        # calculate which wavevector-values are present in the current low res image
        k_center_x = round((size_high_res_x - 1)/2 - k_x[LED_index_y, LED_index_x]/dk_x)
        k_center_y = round((size_high_res_y - 1)/2 - k_y[LED_index_y, LED_index_x]/dk_y)
        k_min_x = int(np.floor(k_center_x - (size_low_res_x - 1) / 2))
        k_max_x = int(np.floor(k_center_x + (size_low_res_x - 1) / 2))
        k_min_y = int(np.floor(k_center_y - (size_low_res_y - 1) / 2))
        k_max_y = int(np.floor(k_center_y + (size_low_res_y - 1) / 2))


        recovered_low_res_ft = inverse_scaling_factor**2 * recovered_object_ft[k_min_y:k_max_y+1, k_min_x:k_max_x+1] \
                                * low_res_CTF * pupil
        recovered_low_res_image =  np.abs(ifftshift(ifft2(ifftshift(recovered_low_res_ft))))
        
        error_estimate += np.sum((raw_low_res_image - recovered_low_res_image)**2)
        
    return error_estimate

