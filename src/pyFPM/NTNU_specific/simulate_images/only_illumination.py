from pyFPM.NTNU_specific.components import MAIN_LED_ARRAY, HAMAMATSU_C11440_42U30
from pyFPM.setup.Setup_parameters import Camera, Lens
from pyFPM.simulation.simulate_imaging import simulate_imaging, finalize_simulation_setup
from pyFPM.NTNU_specific.simulate_images.simulate_setup import simulate_setup_parameters

import numpy as np


def simulate_illumination(lens: Lens, camera: Camera,
                          correct_spherical_wave_illumination, correct_Fresnel_propagation, 
                          arraysize, calibration_parameters, patch_offset=[0,0], limit_LED_indices = None):
    noise_fraction = 0 
    zernike_coefficients = np.array([0,0,0])

    LED_array = MAIN_LED_ARRAY

    pixel_scale_factor = 2

    amplitude_image = np.ones(shape=(camera.raw_image_size[1]*pixel_scale_factor, camera.raw_image_size[0]*pixel_scale_factor))
    phase_image = np.zeros(shape=amplitude_image.shape)
    high_res_complex_object = amplitude_image * np.exp(1j*phase_image)
    
    
    setup_parameters = simulate_setup_parameters(
        lens = lens,
        camera = camera,
        LED_array = LED_array
        )  

    simulated_data, pupil, _ = simulate_imaging(
        high_res_complex_object = high_res_complex_object,
        zernike_coefficients = zernike_coefficients,
        noise_fraction = noise_fraction,
        setup_parameters = setup_parameters,
        arraysize = arraysize,
        pixel_scale_factor = pixel_scale_factor,
        Fresnel_correction = correct_Fresnel_propagation,
        spherical_illumination_correction = correct_spherical_wave_illumination,
        patch_offset=patch_offset,
        use_Fresnel_shift=correct_Fresnel_propagation,
        calibration_parameters=calibration_parameters,
        limit_LED_indices = limit_LED_indices
    )

    patch_size = camera.raw_image_size

    data_patch, imaging_system, illumination_pattern \
        = finalize_simulation_setup(
            setup_parameters = setup_parameters,
            simulated_data = simulated_data,
            patch_offset = patch_offset,
            patch_size = patch_size,
            pixel_scale_factor = pixel_scale_factor,
            calibration_parameters=calibration_parameters,
            arraysize=arraysize
        )
    
    return setup_parameters, data_patch, imaging_system, illumination_pattern, pupil, high_res_complex_object

