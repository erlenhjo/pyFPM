import numpy as np
from numba import njit

from pyFPM.setup.Data import Data_patch
from pyFPM.setup.Illumination_pattern import Illumination_pattern
from pyFPM.setup.Imaging_system import Imaging_system
from pyFPM.recovery.algorithms.Algorithm_result import Algorithm_result
from pyFPM.simulation.image_simulator import simulate_angled_imaging

def compute_sum_square_error(data_patch: Data_patch, imaging_system: Imaging_system, 
                            illumination_pattern: Illumination_pattern, algorithm_result: Algorithm_result):
    
    low_res_images = data_patch.amplitude_images
    recovered_object_fourier_transform = algorithm_result.recovered_object_fourier_transform
    pupil = algorithm_result.pupil
    update_order = illumination_pattern.update_order  # order does not matter, but this is a list only of "active" LEDs
    LED_indices = data_patch.LED_indices

    recovered_low_res_images \
        = simulate_angled_imaging(
            high_res_fourier_transform = recovered_object_fourier_transform,
            pupil = pupil,
            LED_indices = LED_indices,
            imaging_system = imaging_system
        )

    numerator = caclulate_real_space_error_numerator(low_res_images=low_res_images,
                                                     recovered_low_res_images=recovered_low_res_images,
                                                     update_order=update_order)

    denominator = caclulate_real_space_error_normalization_factor(low_res_images=low_res_images,
                                                                  update_order=update_order)

    error_estimate = numerator/denominator
        
    return error_estimate

@njit(cache=True)
def caclulate_real_space_error_numerator(
    low_res_images,
    recovered_low_res_images,
    update_order
):
    real_space_error_metric_numerator = 0
    for image_nr in range(len(update_order)):
        index = update_order[image_nr]
        raw_low_res_image = low_res_images[index]
        recovered_low_res_image = recovered_low_res_images[index]
        real_space_error_metric_numerator += np.linalg.norm(raw_low_res_image - recovered_low_res_image)**2

    return real_space_error_metric_numerator



@njit(cache=True)
def caclulate_real_space_error_normalization_factor(
    low_res_images,
    update_order
):
    real_space_error_metric_normalization_factor = 0
    for image_nr in range(len(update_order)):
        index = update_order[image_nr]
        raw_low_res_image = low_res_images[index]
        real_space_error_metric_normalization_factor += np.linalg.norm(raw_low_res_image)**2

    return real_space_error_metric_normalization_factor