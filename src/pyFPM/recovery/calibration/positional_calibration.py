import numpy as np
from numpy.fft import fft2, ifft2, fftshift, ifftshift
from numba import njit
from scipy.optimize import minimize
import matplotlib.pyplot as plt

from pyFPM.setup.Data import Data_patch
from pyFPM.setup.Illumination_pattern import Illumination_pattern
from pyFPM.setup.Imaging_system import Imaging_system, LED_calibration_parameters
from pyFPM.setup.Setup_parameters import Setup_parameters
from pyFPM.recovery.algorithms.Algorithm_result import Algorithm_result
from pyFPM.recovery.utility.k_space import calculate_low_res_index_range_core
from pyFPM.recovery.algorithms.initialization import initialize_high_res_image, extract_variables_simulated_anealing

def positional_calibration_recovery_algorithm(
        data_patch: Data_patch,
        imaging_system: Imaging_system,
        illumination_pattern: Illumination_pattern,
        setup_parameters: Setup_parameters,
        assumed_LED_calibration_parameters: LED_calibration_parameters
        ) -> tuple[Algorithm_result, LED_calibration_parameters]:

    print("Warning: Does not work even sligthly")

    low_res_images, update_order, size_low_res_x, size_low_res_y, size_high_res_x, size_high_res_y,\
            low_res_CTF, high_res_CTF, scaling_factor, LED_indices, center_indices, LED_pitch,\
            frequency, df_x, df_y, patch_x, patch_y\
                = extract_variables_simulated_anealing(data_patch, setup_parameters, imaging_system, illumination_pattern)

    _ , object_spectrum_guess = initialize_high_res_image(low_res_images, update_order, scaling_factor, 
                                                       object_phase_correction=1, high_res_CTF=high_res_CTF)
    

    recovered_object_fourier_transform, recovered_pupil, calibration_values = \
        simulated_anealing(object_spectrum_guess, update_order, low_res_images, low_res_CTF, LED_indices,
                       size_low_res_x, size_low_res_y, size_high_res_x, size_high_res_y, scaling_factor,
                       center_indices, patch_x, patch_y, frequency, df_x, df_y, LED_pitch, assumed_LED_calibration_parameters)

    recovered_object = fftshift(ifft2(ifftshift(recovered_object_fourier_transform)))

    algorithm_result = Algorithm_result(
        recovered_object = recovered_object,
        recovered_object_fourier_transform = recovered_object_fourier_transform,
        pupil = recovered_pupil,
        convergence_index = [0,0,0,0],
        real_space_error_metric = [0,0,0,0]
    ) 
    return algorithm_result, calibration_values


def simulated_anealing(recovered_object_guess, update_order, low_res_images, low_res_CTF, LED_indices,
                       size_low_res_x, size_low_res_y, size_high_res_x, size_high_res_y, scaling_factor,
                       center_indices, patch_x, patch_y, frequency, df_x, df_y, LED_pitch, assumed_LED_calibration_parameters: LED_calibration_parameters  
                        ):
    low_res_images = low_res_images * scaling_factor**2
    z_LED, delta_x, delta_y, rotation = assumed_LED_calibration_parameters.LED_distance, assumed_LED_calibration_parameters.LED_x_offset,\
                                        assumed_LED_calibration_parameters.LED_y_offset, assumed_LED_calibration_parameters.LED_rotation
    max_iterations = 4
    random_subiterations = 100
    pupil = low_res_CTF

    for loop_nr in range(max_iterations):
        if loop_nr < 9:
            active_LEDs = 25
            pupil = low_res_CTF
            recovered_object_fourier_transform = recovered_object_guess * 1
        else:  
            active_LEDs = len(update_order)
        
        m_vals, n_vals = get_m_n_vals(LED_indices, update_order, active_LEDs, center_indices)
        shifts_x, shifts_y = calculate_shifts(m_vals, n_vals, delta_x, delta_y, z_LED, rotation, patch_x, patch_y, frequency, df_x, df_y, LED_pitch)
        delta = delta_freq(loop_nr)
        
        plt.figure()
        plt.scatter(shifts_x, shifts_y)

        recovered_object_fourier_transform, recovered_pupil, shifts_x, shifts_y =\
            simulated_anealing_single_loop(recovered_object_fourier_transform, pupil, low_res_images, low_res_CTF, update_order,
                                    shifts_x, shifts_y, size_low_res_x, size_low_res_y, size_high_res_x, size_high_res_y, 
                                    random_subiterations, active_LEDs, delta)
        
        error_function = simplified_non_linear_error_factory(shifts_x,shifts_y,m_vals,n_vals,patch_x,patch_y,frequency,df_x,df_y,LED_pitch)
        results = minimize(error_function, x0=[delta_x, delta_y, z_LED, rotation])
        delta_x, delta_y, z_LED, rotation = results.x
        print(delta_x, delta_y, z_LED, rotation)

        plt.scatter(shifts_x, shifts_y)
        plt.show()
    calibration_values = LED_calibration_parameters(LED_distance=z_LED,
                                                    LED_x_offset=delta_x, 
                                                    LED_y_offset=delta_y,
                                                    LED_rotation=rotation)

    return recovered_object_fourier_transform, recovered_pupil, calibration_values                                    


def simulated_anealing_single_loop(recovered_object_fourier_transform, pupil, low_res_images, low_res_CTF, update_order,
                                    shifts_x, shifts_y, size_low_res_x, size_low_res_y, size_high_res_x, size_high_res_y, 
                                    random_subiterations, active_LEDs, delta
                                    ):
    for image_nr in range(active_LEDs):
        index = update_order[image_nr]
        raw_low_res_image = low_res_images[index]
        shift_x = shifts_x[image_nr]
        shift_y = shifts_y[image_nr]
        org_min_x, org_max_x, org_min_y, org_max_y = calculate_low_res_index_range_core(shift_x, shift_y, 
                                                                                        size_low_res_x, size_low_res_y,
                                                                                        size_high_res_x, size_high_res_y)

        #print(org_min_x, org_max_x, org_min_y, org_max_y)
        random_shifts_x = np.random.randint(low=-delta, high=delta+1, size=random_subiterations)
        random_shifts_y = np.random.randint(low=-delta, high=delta+1, size=random_subiterations)
        if image_nr == 0:
            random_shifts_x = [0]
            random_shifts_y = [0]

        for r, (delta_x, delta_y) in enumerate(zip(random_shifts_x, random_shifts_y)):
            min_x, max_x = org_min_x + delta_x, org_max_x + delta_x
            min_y, max_y = org_min_y + delta_y, org_max_y + delta_y
            
            recovered_low_res_fourier_transform = pupil *low_res_CTF * recovered_object_fourier_transform[min_y:max_y+1, min_x:max_x+1]                               
            recovered_low_res_image = fftshift(ifft2(ifftshift(recovered_low_res_fourier_transform)))            

            current_error = error(recovered_low_res_image, raw_low_res_image)
            print(delta_x, delta_y, current_error)
            print(np.mean(np.abs(recovered_low_res_image)), np.mean(raw_low_res_image))
            input()
            if r==0:
                lowest_error = current_error
                s=r
            else:
                if current_error < lowest_error:
                    lowest_error = current_error
                    s=r
                    print("New best")


            
            
        best_delta_x, best_delta_y = random_shifts_x[s], random_shifts_y[s]
        print("best:",best_delta_x,best_delta_y)
        min_x, max_x = org_min_x + best_delta_x, org_max_x + best_delta_x
        min_y, max_y = org_min_y + best_delta_y, org_max_y + best_delta_y 

        best_recovered_low_res_fourier_transform = pupil * low_res_CTF * recovered_object_fourier_transform[min_y:max_y+1, min_x:max_x+1]                               
        best_recovered_low_res_image = fftshift(ifft2(ifftshift(best_recovered_low_res_fourier_transform)))

        new_recovered_low_res_image = raw_low_res_image * best_recovered_low_res_image / np.abs(best_recovered_low_res_image)
        
        new_recovered_low_res_fourier_transform = fftshift(fft2(ifftshift(new_recovered_low_res_image)))

        object_update_term = gradient_descent_step(pupil, new_recovered_low_res_fourier_transform, recovered_low_res_fourier_transform, delta = 1)
        # pupil_update_term = gradient_descent_step(recovered_object_fourier_transform[min_y:max_y+1, min_x:max_x+1],
        #                                     new_recovered_low_res_fourier_transform, recovered_low_res_fourier_transform, delta = 1000)
            
        recovered_object_fourier_transform[min_y:max_y+1, min_x:max_x+1] += object_update_term * low_res_CTF
        #pupil = pupil + pupil_update_term * low_res_CTF


        #plt.matshow(np.log(np.abs(recovered_low_res_fourier_transform)))
        #plt.matshow(np.log(np.abs(fftshift(fft2(ifftshift(raw_low_res_image * recovered_low_res_image / np.abs(recovered_low_res_image)))))))
        #plt.show()
        
        shifts_x[image_nr] += best_delta_x
        shifts_y[image_nr] += best_delta_y
        

    return recovered_object_fourier_transform, pupil, shifts_x, shifts_y


def gradient_descent_step(phi, new_FT, old_FT, delta):
    numerator = np.abs(phi) * np.conj(phi)
    denominator = np.max(np.abs(phi)) * (np.abs(phi)**2 + delta)
    return numerator/denominator * (new_FT - old_FT)

def error(image_1, image_2):
    return np.sum((np.abs(image_1)**2 - np.abs(image_2)**2)**2)

def delta_freq(loop_nr):
    if loop_nr == 0:
        return 2
    elif loop_nr == 1 or loop_nr == 2:
        return 2
    elif loop_nr > 10:
        return 1
    else: 
        return 2
    
def get_m_n(LED_indices, index, center_indices):
    LED_index_x = LED_indices[index][0]
    LED_index_y = LED_indices[index][1]

    center_index_x = center_indices[0]
    center_index_y = center_indices[1]

    m = LED_index_x - center_index_x
    n = LED_index_y - center_index_y

    return m, n

def get_m_n_vals(LED_indices, update_order, active_LEDs, center_indices):
    m_vals = np.empty(active_LEDs)
    n_vals = np.empty(active_LEDs)
    for image_nr in range(active_LEDs):
        index = update_order[image_nr]
        m, n = get_m_n(LED_indices, index, center_indices)
        m_vals[image_nr] = m
        n_vals[image_nr] = n
    return m_vals, n_vals

def calculate_shifts(m, n, delta_x, delta_y, z_LED, rotation, patch_x, patch_y, frequency, df_x, df_y, LED_pitch):
    sin = np.sin(3.14/180 * rotation)
    cos = np.cos(3.14/180 * rotation)

    LED_x = (cos*m + sin*n) * LED_pitch + delta_x
    LED_y = (-sin*m + cos*n) * LED_pitch + delta_y

    x = patch_x - LED_x
    y = patch_y - LED_y

    pixel_shifts_x = -frequency/df_x * x / np.sqrt(x**2 + y**2 + z_LED**2)
    pixel_shifts_y = -frequency/df_y * y / np.sqrt(x**2 + y**2 + z_LED**2)

    return pixel_shifts_x, pixel_shifts_y

def simplified_calculate_shifts_factory(m_vals, n_vals, patch_x, patch_y, frequency, df_x, df_y, LED_pitch):

    def simplified_shift_function(delta_x, delta_y, z_LED, rotation):
        return calculate_shifts(m_vals, n_vals, delta_x, delta_y, z_LED, rotation, patch_x, patch_y, frequency, df_x, df_y, LED_pitch)

    return simplified_shift_function


def simplified_non_linear_error_factory(shifts_x, shifts_y, m_vals, n_vals, patch_x, patch_y, frequency, df_x, df_y, LED_pitch):
    shift_function = simplified_calculate_shifts_factory(m_vals, n_vals, patch_x, patch_y, frequency, df_x, df_y, LED_pitch)
    def simplified_non_linear_error(x):
        delta_x, delta_y, z_LED, rotation = x
        simulated_shifts_x, simulated_shifts_y = shift_function(delta_x, delta_y, z_LED, rotation)
        return np.sum((simulated_shifts_x-shifts_x)**2 + (simulated_shifts_y-shifts_y)**2)
    return simplified_non_linear_error

    

