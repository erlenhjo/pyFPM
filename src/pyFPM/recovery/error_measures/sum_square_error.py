import numpy as np

from pyFPM.setup.Data import Data_patch
from pyFPM.setup.Illumination_pattern import Illumination_pattern
from pyFPM.setup.Imaging_system import Imaging_system
from pyFPM.recovery.algorithms.Algorithm_result import Algorithm_result
from pyFPM.recovery.simulation.fraunhofer_simulator import simulate_fraunhofer_imaging

def compute_sum_square_error(data_patch: Data_patch, imaging_system: Imaging_system, 
                            illumination_pattern: Illumination_pattern, algorithm_result: Algorithm_result):
    
    low_res_images = data_patch.amplitude_images
    recovered_object = algorithm_result.recovered_object
    pupil = algorithm_result.pupil
    update_order = illumination_pattern.update_order  # order does not matter, but this is a list only of "active" LEDs
    LED_indices = data_patch.LED_indices

    recovered_low_res_images \
        = simulate_fraunhofer_imaging(
            high_resolution_object = recovered_object,
            pupil = pupil,
            LED_indices = LED_indices,
            imaging_system = imaging_system
        )

    error_estimate = 0
    for image_nr in range(len(update_order)):
        index = update_order[image_nr]

        raw_low_res_image = low_res_images[index]
        recovered_low_res_image = recovered_low_res_images[index]

        error_estimate += np.mean((raw_low_res_image - recovered_low_res_image)**2)

    error_estimate = error_estimate/len(update_order)
        
    return error_estimate

