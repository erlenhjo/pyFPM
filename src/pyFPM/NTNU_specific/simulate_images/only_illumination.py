from pyFPM.NTNU_specific.components import INFINITYCORRECTED_2X, MAIN_LED_ARRAY
from pyFPM.setup.Setup_parameters import Camera
from pyFPM.simulation.simulate_imaging import simulate_imaging, finalize_simulation_setup
from pyFPM.NTNU_specific.simulate_images.simulate_setup import simulate_setup_parameters

import numpy as np
import skimage


def simulate_illumination(lens, correct_spherical_wave_illumination, correct_non_telecentric, arraysize):
    noise_fraction = 0 
    zernike_coefficients = np.array([0,0,0])

    amplitude_image = np.ones(shape=(8192, 8192))
    phase_image = np.zeros(shape=amplitude_image.shape)
    high_res_complex_object = amplitude_image * np.exp(1j*phase_image)
    pixel_scale_factor = 4
    low_res_image_size = [amplitude_image.shape[1]//pixel_scale_factor, amplitude_image.shape[0]//pixel_scale_factor]
    
    LED_array = MAIN_LED_ARRAY
    array_to_object_distance = 0.200 # m    

    dummy_camera = Camera(
            camera_pixel_size = 6.5e-6,
            raw_image_size = low_res_image_size,
            bit_depth = int(2**8-1)
            )
     
    slide = None # for now
    
    setup_parameters = simulate_setup_parameters(
        lens = lens,
        camera = dummy_camera,
        slide = slide,
        LED_array = LED_array,
        array_to_object_distance = array_to_object_distance
        )  

    simulated_data, pupil, _ = simulate_imaging(
        high_res_complex_object = high_res_complex_object,
        zernike_coefficients = zernike_coefficients,
        noise_fraction = noise_fraction,
        setup_parameters = setup_parameters,
        arraysize = arraysize,
        pixel_scale_factor = pixel_scale_factor,
        non_telecentric_correction = correct_non_telecentric,
        spherical_illumination_correction = correct_spherical_wave_illumination
    )

    patch_start = [0, 0]
    patch_size = dummy_camera.raw_image_size

    data_patch, imaging_system, illumination_pattern \
        = finalize_simulation_setup(
            setup_parameters = setup_parameters,
            simulated_data = simulated_data,
            patch_start = patch_start,
            patch_size = patch_size,
            pixel_scale_factor = pixel_scale_factor
        )
    
    return setup_parameters, data_patch, imaging_system, illumination_pattern, pupil, high_res_complex_object

