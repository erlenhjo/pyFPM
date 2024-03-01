import numpy as np
from numpy.fft import fft2, ifft2, fftshift, ifftshift
from numba import njit
import matplotlib.pyplot as plt

from pyFPM.setup.Data import Data_patch
from pyFPM.setup.Illumination_pattern import Illumination_pattern
from pyFPM.setup.Imaging_system import Imaging_system
from pyFPM.recovery.algorithms.Step_description import Step_description
from pyFPM.recovery.algorithms.Algorithm_result import Algorithm_result
from pyFPM.recovery.utility.k_space import calculate_low_res_index_ranges, calculate_recovered_CTF
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
        shifts_x, shifts_y, low_res_CTF, high_res_CTF, scaling_factor_squared, scaling_factor, LED_indices, \
        alpha, beta, eta, start_EPRY_at_iteration, start_adaptive_steps_at_iteration, converged_alpha, max_iterations \
                = extract_variables(data_patch, imaging_system, illumination_pattern, step_description, correct_aperture_shift)
    
    object_phase_correction = get_object_phase_correction(imaging_system, correct_spherical_wave_phase, correct_Fresnel_phase)
    
    recovered_object_guess, recoverd_object_spectrum_guess\
          = initialize_high_res_image(low_res_images, update_order, scaling_factor, 
                                      object_phase_correction, high_res_CTF)
    
    LED_shifts = calculate_low_res_index_ranges(shifts_x, shifts_y, size_low_res_x, size_low_res_y,
                                                size_high_res_x, size_high_res_y, LED_indices)

    recovered_object_spectrum, recovered_pupil, convergence_index, real_space_error_metric \
        = main_algorithm_loop(recoverd_object_spectrum_guess, update_order, low_res_images,  
                              scaling_factor_squared, low_res_CTF, pupil_guess, LED_shifts,
                              alpha, beta, eta, converged_alpha, max_iterations,
                              start_EPRY_at_iteration, start_adaptive_steps_at_iteration 
                              )

    recovered_CTF = calculate_recovered_CTF(update_order, LED_shifts, low_res_CTF, size_high_res_x, size_high_res_y)
    recovered_object_spectrum = recovered_object_spectrum * recovered_CTF

    recovered_object = fftshift(ifft2(ifftshift(recovered_object_spectrum))) * np.conj(object_phase_correction)
    recovered_object_fourier_transform = fftshift(fft2(ifftshift(recovered_object))) * recovered_CTF

    algorithm_result = Algorithm_result(
        recovered_object = recovered_object,
        recovered_object_fourier_transform = recovered_object_fourier_transform,
        pupil = recovered_pupil,
        convergence_index = convergence_index,
        real_space_error_metric = real_space_error_metric
    ) 
    return algorithm_result

#@njit(cache=True)
def main_algorithm_loop(recovered_object_spectrum_guess, update_order, low_res_images,
                        scaling_factor_squared, low_res_CTF, pupil, LED_shifts, 
                        alpha, beta, eta, converged_alpha, max_iterations,
                        start_EPRY_at_iteration, start_adaptive_steps_at_iteration
                        ):
    recovered_object_spectrum = recovered_object_spectrum_guess
    low_res_images = low_res_images * scaling_factor_squared
    pupil = pupil * low_res_CTF

    convergence_index = np.zeros(max_iterations)
    normalized_real_space_error_metric = np.zeros(max_iterations)
    real_space_error_metric_normalization_factor = caclulate_real_space_error_normalization_factor(low_res_images,update_order)

    for loop_nr in range(max_iterations):
        real_space_error_metric = 0
        for image_nr in range(len(update_order)):
            index = update_order[image_nr]
            raw_image = low_res_images[index]
            min_x, max_x, min_y, max_y = LED_shifts[index]
            
            # project current spectrum to detector
            current_spectrum = recovered_object_spectrum[min_y:max_y+1, min_x:max_x+1]
            current_lens_spectrum = pupil * low_res_CTF * current_spectrum                                    
            projected_image = fftshift(ifft2(ifftshift(current_lens_spectrum)))            

            # calculate error measures
            convergence_index[loop_nr] += np.mean(np.abs(projected_image)) \
                                            / np.sum(np.abs(np.abs(projected_image) - raw_image))
            real_space_error_metric += np.linalg.norm(raw_image - np.abs(projected_image))**2

            # calculated updated spectrum at lens
            updated_image = raw_image * projected_image / np.abs(projected_image)
            updated_lens_spectrum = fftshift(fft2(ifftshift(updated_image)))

            # calculate update terms
            if loop_nr<start_EPRY_at_iteration:
                object_update_term = gradient_descent_step(pupil, updated_lens_spectrum, current_lens_spectrum, 1)
                pupil_update_term = 0
            else:
                object_update_term = gradient_descent_step(pupil, updated_lens_spectrum, current_lens_spectrum, 1)
                pupil_update_term = gradient_descent_step(current_spectrum, updated_lens_spectrum, current_lens_spectrum, 1000)
                
            # update spectrum and pupil
            recovered_object_spectrum[min_y:max_y+1, min_x:max_x+1] += alpha * object_update_term * low_res_CTF
            pupil += beta * pupil_update_term * low_res_CTF
            
        # update error and step size    
        normalized_real_space_error_metric[loop_nr] = real_space_error_metric/real_space_error_metric_normalization_factor

        if loop_nr > start_adaptive_steps_at_iteration:
            alpha, beta = update_step_sizes(alpha, beta, eta, loop_nr,
                                            error=normalized_real_space_error_metric[loop_nr],
                                            prev_error=normalized_real_space_error_metric[loop_nr-1])

            if alpha<converged_alpha:
                normalized_real_space_error_metric=normalized_real_space_error_metric[:loop_nr]
                convergence_index=convergence_index[:loop_nr]
                break


    return recovered_object_spectrum, pupil, convergence_index, normalized_real_space_error_metric


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
