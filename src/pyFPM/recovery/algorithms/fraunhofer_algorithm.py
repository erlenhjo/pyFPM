import numpy as np
from numpy.fft import fft2, ifft2, fftshift, ifftshift
from numba import njit

from pyFPM.setup.Data import Data_patch
from pyFPM.setup.Illumination_pattern import Illumination_pattern
from pyFPM.setup.Imaging_system import Imaging_system
from pyFPM.recovery.algorithms.Step_description import Step_description
from pyFPM.recovery.algorithms.Algorithm_result import Algorithm_result
from pyFPM.recovery.utility.k_space import calculate_low_res_index_range, calculate_recovered_CTF
from pyFPM.recovery.algorithms.initialization import initialize_high_res_image, extract_variables
from pyFPM.recovery.utility.real_space_error import caclulate_real_space_error_normalization_factor

def fraunhofer_recovery_algorithm(
        data_patch: Data_patch,
        imaging_system: Imaging_system,
        illumination_pattern: Illumination_pattern,
        pupil_guess,
        step_description: Step_description,
        use_epry: bool,
        correct_spherical_wave_phase: bool,
        correct_Fresnel_phase: bool,
        correct_aperture_shift: bool
        ) -> Algorithm_result :

    low_res_images, update_order, size_low_res_x, size_low_res_y, size_high_res_x, size_high_res_y, \
        shifts_x, shifts_y, low_res_CTF, scaling_factor_squared, scaling_factor, LED_indices, \
        alpha, beta, eta, start_EPRY_at_iteration, start_adaptive_steps_at_iteration, converged_alpha, max_iterations \
                = extract_variables(data_patch, imaging_system, illumination_pattern, step_description, correct_aperture_shift)
    
    object_phase_correction = get_object_phase_correction(imaging_system, correct_spherical_wave_phase, correct_Fresnel_phase)
    
    recovered_object_guess = initialize_high_res_image(low_res_images, update_order, scaling_factor, object_phase_correction)
    

    recovered_object_fourier_transform, recovered_pupil, convergence_index, real_space_error_metric \
        = main_algorithm_loop(recovered_object_guess, use_epry, update_order, low_res_images,  LED_indices,
                        shifts_x, shifts_y, size_low_res_x, size_low_res_y, size_high_res_x, size_high_res_y, scaling_factor_squared, 
                        low_res_CTF, pupil_guess, alpha, beta, eta, start_EPRY_at_iteration, start_adaptive_steps_at_iteration, converged_alpha, max_iterations
                        )

    recovered_CTF = calculate_recovered_CTF(update_order, LED_indices, shifts_x, shifts_y, size_low_res_x, size_low_res_y, size_high_res_x, size_high_res_y, low_res_CTF)
    recovered_object_fourier_transform = recovered_object_fourier_transform * recovered_CTF

    recovered_object = fftshift(ifft2(ifftshift(recovered_object_fourier_transform))) * np.conj(object_phase_correction)

    algorithm_result = Algorithm_result(
        recovered_object = recovered_object,
        recovered_object_fourier_transform = recovered_object_fourier_transform,
        pupil = recovered_pupil,
        convergence_index = convergence_index,
        real_space_error_metric = real_space_error_metric
    ) 
    return algorithm_result



def main_algorithm_loop(recovered_object_guess, use_epry, update_order, low_res_images,  LED_indices,
                        shifts_x, shifts_y, size_low_res_x, size_low_res_y, size_high_res_x, size_high_res_y, scaling_factor_squared, 
                        low_res_CTF, pupil, alpha, beta, eta, start_EPRY_at_iteration, start_adaptive_steps_at_iteration, converged_alpha, max_iterations
                        ):
    recovered_object_fourier_transform = fftshift(fft2(ifftshift(recovered_object_guess)))  
    convergence_index = np.zeros(max_iterations)
    normalized_real_space_error_metric = np.zeros(max_iterations)
    low_res_images = low_res_images * scaling_factor_squared
    real_space_error_metric_normalization_factor = caclulate_real_space_error_normalization_factor(low_res_images,update_order)
    pupil = pupil * low_res_CTF

    for loop_nr in range(max_iterations):
        real_space_error_metric = 0
        for image_nr in range(len(update_order)):
            index = update_order[image_nr]
            
            raw_low_res_image = low_res_images[index]

            min_x, max_x, min_y, max_y = calculate_low_res_index_range(shifts_x, shifts_y, size_low_res_x, size_low_res_y,
                                                                          size_high_res_x, size_high_res_y, LED_indices, index)
            
            recovered_low_res_fourier_transform = pupil * recovered_object_fourier_transform[min_y:max_y+1, min_x:max_x+1]
                                                
            recovered_low_res_image = fftshift(ifft2(ifftshift(recovered_low_res_fourier_transform)))            

            convergence_index[loop_nr] += np.mean(np.abs(recovered_low_res_image)) \
                                            / np.sum(np.abs(np.abs(recovered_low_res_image) - raw_low_res_image))
            
            real_space_error_metric += np.linalg.norm(raw_low_res_image - np.abs(recovered_low_res_image))**2

            new_recovered_low_res_image = raw_low_res_image * recovered_low_res_image / np.abs(recovered_low_res_image)
            
            new_recovered_low_res_fourier_transform = fftshift(fft2(ifftshift(new_recovered_low_res_image)))

            # import matplotlib.pyplot as plt
            # plt.matshow(np.abs(recovered_low_res_image))
            # plt.matshow(np.abs(new_recovered_low_res_image))
            # plt.matshow(np.log(np.abs(new_recovered_low_res_fourier_transform)))
            # plt.matshow(np.log(np.abs(recovered_low_res_fourier_transform)))
            # plt.show()

            if not use_epry or loop_nr<start_EPRY_at_iteration:
                object_update_term = standard_step(pupil, new_recovered_low_res_fourier_transform, recovered_low_res_fourier_transform)
                pupil_update_term = 0

            else:
                object_update_term = standard_step(pupil, new_recovered_low_res_fourier_transform, recovered_low_res_fourier_transform)
                pupil_update_term = standard_step(recovered_object_fourier_transform[min_y:max_y+1, min_x:max_x+1],
                                                  new_recovered_low_res_fourier_transform, recovered_low_res_fourier_transform)
                
            recovered_object_fourier_transform[min_y:max_y+1, min_x:max_x+1] += alpha * object_update_term * low_res_CTF
            pupil += beta * pupil_update_term * low_res_CTF
        
        normalized_real_space_error_metric[loop_nr] = real_space_error_metric/real_space_error_metric_normalization_factor

        if loop_nr > start_adaptive_steps_at_iteration:
            alpha, beta = update_step_sizes(alpha, beta, eta, loop_nr,
                                            error=normalized_real_space_error_metric[loop_nr],
                                            prev_error=normalized_real_space_error_metric[loop_nr-1])

            if alpha<converged_alpha:
                normalized_real_space_error_metric=normalized_real_space_error_metric[:loop_nr]
                convergence_index=convergence_index[:loop_nr]
                break


    return recovered_object_fourier_transform, pupil, convergence_index, normalized_real_space_error_metric

@njit(cache=True)
def standard_step(phi, new_FT, old_FT):
    return np.conj(phi) / (np.max(np.abs(phi)) ** 2) * (new_FT - old_FT)


@njit(cache=True)
def gradient_descent_step(phi, new_FT, old_FT, delta):
    numerator = np.abs(phi) * np.conj(phi)
    denominator = np.max(np.abs(phi)) * (np.abs(phi)**2 + delta)
    return numerator/denominator * (new_FT - old_FT)


def get_object_phase_correction(imaging_system: Imaging_system, correct_spherical_wave_phase, correct_Fresnel_phase):
    object_plane_phase_shift_correction = 1
    if correct_Fresnel_phase:
        object_plane_phase_shift_correction *= imaging_system.high_res_Fresnel_correction
    if correct_spherical_wave_phase: 
        object_plane_phase_shift_correction *= imaging_system.high_res_spherical_illumination_correction
    return object_plane_phase_shift_correction





def update_step_sizes(alpha, beta, eta, loop_nr, error, prev_error):
    if (prev_error - error) > eta * prev_error:
        return alpha, beta
    else:
        alpha, beta = alpha/2, beta/2
        print(f"Loop nr {loop_nr}, alpha={alpha}, beta={beta}")
        return alpha, beta
