import numpy as np
import matplotlib.pyplot as plt

from pyFPM.pre_processing.Preprocessed_data import Preprocessed_data
from pyFPM.pre_processing.Illumination_pattern import Illumination_pattern
from pyFPM.setup.Setup_parameters import Setup_parameters
from pyFPM.setup.Imaging_system import Imaging_system
from pyFPM.recovery.algorithms.Algorithm_result import Algorithm_result

def primitive_fourier_ptychography_algorithm(
        preprocessed_data: Preprocessed_data,
        setup_parameters: Setup_parameters,
        imaging_system: Imaging_system,
        illumination_pattern: Illumination_pattern,
        loops
    ) -> Algorithm_result :

    low_res_images = preprocessed_data.amplitude_images
    update_order = illumination_pattern.update_order
    size_low_res_x = imaging_system.patch_size[0]
    size_low_res_y = imaging_system.patch_size[1]
    size_high_res_x = imaging_system.final_image_size[0]
    size_hig_res_y = imaging_system.final_image_size[1]
    k_x = imaging_system.wavevectors_x()
    k_y = imaging_system.wavevectors_y()
    dk_x = imaging_system.differential_wavevectors_x()
    dk_y = imaging_system.differential_wavevectors_y()
    low_res_CTF = imaging_system.low_res_CTF


    # initialize recovered image with ones
    recovered_object = np.ones(shape = (size_hig_res_y, size_high_res_x)) 
    recovered_object_fourier_transform = np.fft.fftshift(np.fft.fft2(np.fft.fftshift(recovered_object))) 

    convergence_index = np.empty(loops)

    #print(np.argwhere(recovered_object_fourier_transform > 0))
    #print(recovered_object_fourier_transform[128,128])

    for loop_nr in range(loops):
        for image_nr in range(len(update_order)):
            index = update_order[image_nr]
            current_image = low_res_images[index]
            #print(np.fft.fftshift(current_image))
            #print(np.fft.fft2(np.fft.fftshift(current_image)))
            print(np.fft.fftshift(np.fft.fft2(current_image)))
            input()
        continue
