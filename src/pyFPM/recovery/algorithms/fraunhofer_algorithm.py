import numpy as np
from numpy.fft import fft2, ifft2, fftshift, ifftshift
from numba import njit

from pyFPM.setup.Data import Data_patch
from pyFPM.setup.Illumination_pattern import Illumination_pattern
from pyFPM.setup.Imaging_system import Imaging_system
from pyFPM.recovery.algorithms.Algorithm_result import Algorithm_result
from pyFPM.recovery.utility.k_space import calculate_k_vector_range, calculate_recovered_CTF
from pyFPM.recovery.algorithms.initialization import initialize_high_res_image, extract_variables
#from pyFPM.numba_helper.jitable_fftshifts import fftshift, ifftshift

def fraunhofer_recovery_algorithm(
        data_patch: Data_patch,
        imaging_system: Imaging_system,
        illumination_pattern: Illumination_pattern,
        pupil,
        loops,
        use_epry = False,
        use_gradient_descent = False
    ) -> Algorithm_result :

    low_res_images, update_order, size_low_res_x, size_low_res_y, size_high_res_x, size_high_res_y, \
        k_x, k_y, dk_y, dk_x, low_res_CTF, scaling_factor_squared, scaling_factor, LED_indices \
                = extract_variables(data_patch, imaging_system, illumination_pattern)
    
    recovered_object_guess = initialize_high_res_image(low_res_images, update_order, scaling_factor)
    

    recovered_object_fourier_transform, pupil, convergence_index \
        = main_algorithm_loop(recovered_object_guess, loops, use_epry, use_gradient_descent, update_order, low_res_images,  LED_indices,
                        k_x, k_y, dk_x, dk_y, size_low_res_x, size_low_res_y, size_high_res_x, size_high_res_y, scaling_factor_squared, low_res_CTF, pupil
                        )

    recovered_CTF = calculate_recovered_CTF(update_order, LED_indices, k_x, k_y, dk_x, dk_y, size_low_res_x, size_low_res_y, size_high_res_x, size_high_res_y, low_res_CTF)
    recovered_object_fourier_transform = recovered_object_fourier_transform * recovered_CTF

    algorithm_result = Algorithm_result(
        recovered_object = fftshift(ifft2(ifftshift(recovered_object_fourier_transform))),
        recovered_object_fourier_transform = recovered_object_fourier_transform,
        pupil = pupil,
        convergence_index = convergence_index
    ) 
    return algorithm_result



def main_algorithm_loop(recovered_object_guess, loops, use_epry, use_gradient_descent, update_order, low_res_images,  LED_indices,
                        k_x, k_y, dk_x, dk_y, size_low_res_x, size_low_res_y, size_high_res_x, size_high_res_y, scaling_factor_squared, low_res_CTF, pupil
                        ):
    recovered_object_fourier_transform = fftshift(fft2(ifftshift(recovered_object_guess)))  
    convergence_index = np.zeros(loops)
    low_res_images = low_res_images * scaling_factor_squared

    for loop_nr in range(loops):
        for image_nr in range(len(update_order)):
            index = update_order[image_nr]
            
            raw_low_res_image = low_res_images[index]

            k_min_x, k_max_x, k_min_y, k_max_y = calculate_k_vector_range(k_x, k_y, dk_x, dk_y, size_low_res_x, size_low_res_y,
                                                                          size_high_res_x, size_high_res_y, LED_indices, index)

            recovered_low_res_fourier_transform = recovered_object_fourier_transform[k_min_y:k_max_y+1, k_min_x:k_max_x+1] \
                                                  * low_res_CTF \
                                                  * pupil
                                                
            recovered_low_res_image = fftshift(ifft2(ifftshift(recovered_low_res_fourier_transform)))            

            convergence_index[loop_nr] += np.mean(np.abs(recovered_low_res_image)) \
                                            / np.sum(np.abs(np.abs(recovered_low_res_image) - raw_low_res_image))

            new_recovered_low_res_image = raw_low_res_image * recovered_low_res_image / np.abs(recovered_low_res_image)
            
            new_recovered_low_res_fourier_transform = fftshift(fft2(ifftshift(new_recovered_low_res_image)))

            if not use_epry:
                object_update_term = standard_step(pupil, new_recovered_low_res_fourier_transform, recovered_low_res_fourier_transform)
                
                recovered_object_fourier_transform[k_min_y:k_max_y+1, k_min_x:k_max_x+1] += object_update_term * low_res_CTF

            elif not use_gradient_descent:
                object_update_term = standard_step(pupil, new_recovered_low_res_fourier_transform, recovered_low_res_fourier_transform)
                pupil_update_term = standard_step(recovered_object_fourier_transform[k_min_y:k_max_y+1, k_min_x:k_max_x+1],
                                                  new_recovered_low_res_fourier_transform, recovered_low_res_fourier_transform)
                
                recovered_object_fourier_transform[k_min_y:k_max_y+1, k_min_x:k_max_x+1] += object_update_term * low_res_CTF
                if loop_nr > 1:
                    pupil = (pupil + pupil_update_term) * low_res_CTF

            elif use_gradient_descent:
                object_update_term = gradient_descent_step(pupil, new_recovered_low_res_fourier_transform, recovered_low_res_fourier_transform, 1.0)
                pupil_update_term = gradient_descent_step(recovered_object_fourier_transform[k_min_y:k_max_y+1, k_min_x:k_max_x+1],
                                                          new_recovered_low_res_fourier_transform, recovered_low_res_fourier_transform, 1.0)

                recovered_object_fourier_transform[k_min_y:k_max_y+1, k_min_x:k_max_x+1] += object_update_term * low_res_CTF
                if loop_nr > 1:
                    pupil = (pupil + pupil_update_term) * low_res_CTF

    return recovered_object_fourier_transform, pupil, convergence_index

@njit(cache=True)
def standard_step(phi, new_FT, old_FT):
    return np.conj(phi) / (np.max(np.abs(phi)) ** 2) * (new_FT - old_FT)


@njit(cache=True)
def gradient_descent_step(phi, new_FT, old_FT, delta):
    numerator = np.abs(phi) * np.conj(phi)
    denominator = np.max(np.abs(phi)) * (np.abs(phi)**2 + delta)
    return numerator/denominator * (new_FT - old_FT)


