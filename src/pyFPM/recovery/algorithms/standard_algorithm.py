import numpy as np
from numpy.fft import fft2, ifft2, fftshift, ifftshift
from numba import njit, vectorize, jit
import matplotlib.pyplot as plt
from rocket_fft import scipy_like
scipy_like()

from pyFPM.setup.Data import Data_patch
from pyFPM.setup.Illumination_pattern import Illumination_pattern
from pyFPM.setup.Imaging_system import Imaging_system
from pyFPM.recovery.algorithms.Step_description import Step_description
from pyFPM.recovery.algorithms.Algorithm_result import Algorithm_result
from pyFPM.recovery.utility.k_space import calculate_low_res_index_ranges, calculate_recovered_CTF
from pyFPM.recovery.algorithms.initialization import initialize_high_res_image, extract_variables, unpack_mask_indices
from pyFPM.recovery.utility.real_space_error import caclulate_real_space_error_normalization_factor

def standard_recovery_algorithm(
        data_patch: Data_patch,
        imaging_system: Imaging_system,
        illumination_pattern: Illumination_pattern,
        pupil_guess,
        step_description: Step_description,
        correct_spherical_wave_phase: bool,
        correct_Fresnel_phase: bool,
        use_Fresnel_shifts: bool
        ) -> Algorithm_result :

    low_res_images, update_order, complex_type, size_low_res_x, size_low_res_y, size_high_res_x, size_high_res_y, \
        shifts_x, shifts_y, low_res_CTF, high_res_CTF, scaling_factor_squared, scaling_factor, LED_indices, \
        alpha, beta, eta, start_EPRY_at_iteration, start_adaptive_steps_at_iteration, converged_alpha, \
             apply_BF_mask_from_iteration, max_iterations \
                = extract_variables(data_patch, imaging_system, illumination_pattern, step_description, use_Fresnel_shifts)
    
    object_phase_correction = get_object_phase_correction(imaging_system, correct_spherical_wave_phase, 
                                                          correct_Fresnel_phase, complex_type)
    
    recovered_object_guess, recovered_object_spectrum_guess\
          = initialize_high_res_image(low_res_images, update_order, scaling_factor, 
                                      object_phase_correction, high_res_CTF, complex_type)
    pupil_guess = pupil_guess.astype(complex_type)

    LED_shifts = calculate_low_res_index_ranges(shifts_x, shifts_y, size_low_res_x, size_low_res_y,
                                                size_high_res_x, size_high_res_y, LED_indices)
    BF_edge_masks = imaging_system.BF_edge_masks
    mask_indices = unpack_mask_indices(mask_indices = imaging_system.mask_index_per_LED,
                                       LED_indices = LED_indices)
    

    recovered_object_spectrum, recovered_pupil, convergence_index, \
        real_space_error_metric, amplitude_error, masked_amplitude_error\
            = main_algorithm_loop(recovered_object_spectrum_guess, update_order, low_res_images,  
                                scaling_factor_squared, low_res_CTF, pupil_guess, LED_shifts,
                                alpha, beta, eta, converged_alpha, max_iterations,
                                start_EPRY_at_iteration, start_adaptive_steps_at_iteration,
                                BF_edge_masks, mask_indices, apply_BF_mask_from_iteration
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
        real_space_error_metric = real_space_error_metric,
        low_res_image = data_patch.amplitude_images[illumination_pattern.update_order[0]],
        recovered_CTF = recovered_CTF,
        imaging_system = imaging_system,
        amplitude_error = amplitude_error,
        masked_amplitude_error = masked_amplitude_error
    ) 
    return algorithm_result

#@njit(cache=True, fastmath=True)
def main_algorithm_loop(recovered_object_spectrum_guess, update_order, low_res_images,
                        scaling_factor_squared, low_res_CTF, pupil, LED_shifts, 
                        alpha, beta, eta, converged_alpha, max_iterations,
                        start_EPRY_at_iteration, start_adaptive_steps_at_iteration,
                        BF_edge_masks, mask_indices, apply_BF_mask_from_iteration
                        ):
    recovered_object_spectrum = recovered_object_spectrum_guess
    low_res_images = low_res_images * scaling_factor_squared
    pupil = pupil * low_res_CTF

    convergence_index = np.zeros(max_iterations)
    normalized_real_space_error_metric = np.zeros(max_iterations)
    real_space_error_metric_normalization_factor = caclulate_real_space_error_normalization_factor(low_res_images,update_order)
    amplitude_error_per_image_per_loop = np.zeros((max_iterations, len(update_order)))
    masked_amplitude_error_per_image_per_loop = np.zeros((max_iterations, len(update_order)))

    for loop_nr in range(max_iterations):
        real_space_error_metric = 0
        for image_nr in range(len(update_order)):
            index = update_order[image_nr]
            raw_image = low_res_images[index]
            min_x, max_x, min_y, max_y = LED_shifts[index]
            mask_index = mask_indices[index]
            if mask_index == -1 or loop_nr < apply_BF_mask_from_iteration:
                retain_mask = 0
                update_mask = 1
            else:
                retain_mask = BF_edge_masks[mask_index]
                update_mask = np.invert(retain_mask)
                # plt.matshow(mask)
                # plt.matshow(raw_image)
                # plt.matshow(raw_image*mask)
                # plt.matshow(raw_image*inverse_mask)
                #plt.show()

            # project current spectrum to detector
            current_spectrum = recovered_object_spectrum[min_y:max_y+1, min_x:max_x+1]
            current_lens_spectrum = pupil * low_res_CTF * current_spectrum                                    
            projected_image = fftshift(ifft2(ifftshift(current_lens_spectrum)))

            # calculated updated spectrum at lens
            updated_image = projected_image * retain_mask + raw_image * projected_image / np.abs(projected_image) * update_mask
            updated_lens_spectrum = fftshift(fft2(ifftshift(updated_image)))


            # calculate error measures
            if np.sum(np.abs(np.abs(projected_image) - np.abs(updated_image))) != 0:
                convergence_index[loop_nr] += np.mean(np.abs(projected_image)) \
                                                / np.sum(np.abs(np.abs(projected_image) - np.abs(updated_image)))
            
            amplitude_error = np.abs(np.abs(projected_image) - np.abs(raw_image))
            masked_amplitude_error =  np.abs(np.abs(projected_image) - np.abs(updated_image))
            amplitude_error_per_image_per_loop[loop_nr,image_nr] = np.mean(amplitude_error)
            masked_amplitude_error_per_image_per_loop[loop_nr,image_nr] = np.mean(masked_amplitude_error)
            real_space_error_metric += np.linalg.norm(masked_amplitude_error)**2

            # if loop_nr == 28:
            #     fig, axes = plt.subplots(2,3)
            #     axes[0,0].matshow(raw_image)
            #     axes[0,1].matshow(masked_error)
            #     axes[0,2].matshow(error)
            #     axes[1,0].matshow(np.log(np.abs(current_spectrum)))
            #     axes[1,1].matshow(np.log(np.abs(current_lens_spectrum)))
            #     if type(retain_mask) == int:
            #         axes[1,2].matshow(error)
            #     else:
            #         axes[1,2].matshow(retain_mask)

            #     fig.suptitle(f"{np.mean(amplitude_error)} {np.mean(masked_amplitude_error)}")
            #     plt.show()

            # calculate update terms
            if loop_nr<start_EPRY_at_iteration:
                object_update_term = np.abs(pupil) * np.conj(pupil)/\
                                    (np.max(np.abs(pupil)) * (np.abs(pupil)**2 + 1))\
                                    * (updated_lens_spectrum - current_lens_spectrum)
                pupil_update_term = 0 * object_update_term # just zero but of right type and shape
            else:
                object_update_term = np.abs(pupil) * np.conj(pupil)/\
                                    (np.max(np.abs(pupil)) * (np.abs(pupil)**2 + 1))\
                                    * (updated_lens_spectrum - current_lens_spectrum)
                pupil_update_term = np.abs(current_spectrum) * np.conj(current_spectrum)/\
                                    (np.max(np.abs(current_spectrum)) * (np.abs(current_spectrum)**2 + 1000))\
                                    * (updated_lens_spectrum - current_lens_spectrum)

            # update spectrum and pupil
            recovered_object_spectrum[min_y:max_y+1, min_x:max_x+1] += alpha * object_update_term * low_res_CTF
            pupil += beta * pupil_update_term * low_res_CTF
            
        # update error and step size    
        normalized_real_space_error_metric[loop_nr] = real_space_error_metric/real_space_error_metric_normalization_factor
        # if loop_nr == 27:
        #     fig, axes = plt.subplots(1,1)
        #     axes.plot(amplitude_error_per_image_per_loop[loop_nr])
        #     axes.plot(masked_amplitude_error_per_image_per_loop[loop_nr])
        #     fig.suptitle(f"{loop_nr}, {alpha}")
        #     plt.show()

        if loop_nr > start_adaptive_steps_at_iteration:
            alpha, beta = update_step_sizes(alpha, beta, eta,
                                            error=normalized_real_space_error_metric[loop_nr],
                                            prev_error=normalized_real_space_error_metric[loop_nr-1])

            if alpha<converged_alpha:
                normalized_real_space_error_metric=normalized_real_space_error_metric[:loop_nr]
                convergence_index=convergence_index[:loop_nr]
                amplitude_error_per_image_per_loop=amplitude_error_per_image_per_loop[:loop_nr]
                masked_amplitude_error_per_image_per_loop=masked_amplitude_error_per_image_per_loop[:loop_nr]
                break


    return recovered_object_spectrum, pupil, convergence_index, normalized_real_space_error_metric, amplitude_error_per_image_per_loop, masked_amplitude_error_per_image_per_loop


def get_object_phase_correction(imaging_system: Imaging_system, correct_spherical_wave_phase, correct_Fresnel_phase, complex_type):
    object_plane_phase_shift_correction = np.complex128(1)
    if correct_Fresnel_phase:
        object_plane_phase_shift_correction *= imaging_system.high_res_Fresnel_correction
    if correct_spherical_wave_phase: 
        object_plane_phase_shift_correction *= imaging_system.high_res_spherical_illumination_correction
    return object_plane_phase_shift_correction.astype(complex_type)

@njit(cache=True)
def update_step_sizes(alpha, beta, eta, error, prev_error):
    if (prev_error - error) > eta * prev_error:
        return alpha, beta
    else:
        alpha, beta = alpha/2, beta/2
        return alpha, beta
