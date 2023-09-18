import numpy as np
from numpy.fft import fft2, ifft2, fftshift, ifftshift
import matplotlib.pyplot as plt

from pyFPM.setup.Preprocessed_data import Preprocessed_data
from pyFPM.setup.Illumination_pattern import Illumination_pattern
from pyFPM.setup.Setup_parameters import Setup_parameters
from pyFPM.setup.Imaging_system import Imaging_system
from pyFPM.recovery.algorithms.Algorithm_result import Algorithm_result

def primitive_fourier_ptychography_algorithm(
        preprocessed_data: Preprocessed_data,
        imaging_system: Imaging_system,
        illumination_pattern: Illumination_pattern,
        pupil,
        loops
    ) -> Algorithm_result :

    low_res_images, update_order, size_low_res_x, size_low_res_y, size_high_res_x, size_high_res_y, \
        k_x, k_y, dk_y, dk_x, low_res_CTF, inverse_scaling_factor_squared, scaling_factor_squared, \
            scaling_factor, LED_indices = extract_variables(preprocessed_data, imaging_system, illumination_pattern)
    
    recovered_object_guess = initialize_high_res_image(low_res_images, update_order, scaling_factor)
    recovered_object_fourier_transform = fftshift(fft2(fftshift(recovered_object_guess)))  # why extra fftshift, should be ifftshift?    
    convergence_index = np.zeros(loops)

    for loop_nr in range(loops):
        for image_nr in range(len(update_order)):
            index = update_order[image_nr]
            
            raw_low_res_image = low_res_images[index]

            k_min_x, k_max_x, k_min_y, k_max_y = calculate_k_vector_range(k_x, k_y, dk_x, dk_y, size_low_res_x, size_low_res_y,
                                                                          size_high_res_x, size_high_res_y, LED_indices, index)

            recovered_low_res_fourier_transform = inverse_scaling_factor_squared \
                                                  * recovered_object_fourier_transform[k_min_y:k_max_y+1, k_min_x:k_max_x+1] \
                                                  * low_res_CTF \
                                                  * pupil
                                                
            recovered_low_res_image = ifftshift(ifft2(ifftshift(recovered_low_res_fourier_transform))) # only inner should be ifftshift?

            convergence_index[loop_nr] += np.mean(np.abs(recovered_low_res_image)) \
                                            / np.sum(abs(abs(recovered_low_res_image) - raw_low_res_image))

            new_recovered_low_res_image =  scaling_factor_squared * raw_low_res_image * recovered_low_res_image / np.abs(recovered_low_res_image)
            
            new_recovered_low_res_fourier_transform = fftshift(fft2(fftshift(new_recovered_low_res_image))) \
                                                      * low_res_CTF \
                                                      / pupil

            updated_region_of_recovered_object_fourier_transform = new_recovered_low_res_fourier_transform \
                                                     + (1-low_res_CTF) * recovered_object_fourier_transform[k_min_y:k_max_y+1, k_min_x:k_max_x+1]

            recovered_object_fourier_transform[k_min_y:k_max_y+1, k_min_x:k_max_x+1] = updated_region_of_recovered_object_fourier_transform

    algorithm_result = Algorithm_result(
        recovered_object = ifftshift(ifft2(ifftshift(recovered_object_fourier_transform))),  # only inner should be ifftshift?
        recovered_object_fourier_transform = recovered_object_fourier_transform,
        pupil = pupil,
        convergence_index = convergence_index
    ) 
    return algorithm_result




def extract_variables(preprocessed_data: Preprocessed_data, imaging_system: Imaging_system, illumination_pattern: Illumination_pattern):
    low_res_images = preprocessed_data.amplitude_images
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
    inverse_scaling_factor_squared = (1 / imaging_system.pixel_scale_factor)**2
    scaling_factor_squared = (imaging_system.pixel_scale_factor)**2
    scaling_factor = imaging_system.pixel_scale_factor
    LED_indices = preprocessed_data.LED_indices

    return low_res_images, update_order, size_low_res_x, size_low_res_y, size_high_res_x, size_high_res_y, k_x, k_y, dk_y, dk_x,\
            low_res_CTF, inverse_scaling_factor_squared, scaling_factor_squared, scaling_factor, LED_indices

def initialize_high_res_image(low_res_images, update_order, scaling_factor):
    ones = np.ones(shape = (scaling_factor, scaling_factor))
    first_image = low_res_images[update_order[0]]
    recovered_object_guess = np.kron(first_image, ones)
    return recovered_object_guess

def calculate_k_vector_range(k_x, k_y, dk_x, dk_y, 
                             size_low_res_x, size_low_res_y, size_high_res_x, size_high_res_y,
                             LED_indices, index 
                            ):
    LED_index_x = LED_indices[index][0]
    LED_index_y = LED_indices[index][1]

    # calculate which wavevector-values are present in the current low res image
    k_center_x = round((size_high_res_x - 1)/2 - k_x[LED_index_y, LED_index_x]/dk_x)
    k_center_y = round((size_high_res_y - 1)/2 - k_y[LED_index_y, LED_index_x]/dk_y)
    k_min_x = int(np.floor(k_center_x - (size_low_res_x - 1) / 2))
    k_max_x = int(np.floor(k_center_x + (size_low_res_x - 1) / 2))
    k_min_y = int(np.floor(k_center_y - (size_low_res_y - 1) / 2))
    k_max_y = int(np.floor(k_center_y + (size_low_res_y - 1) / 2))

    return k_min_x, k_max_x, k_min_y, k_max_y