from pyFPM.simulation.simulate_imaging import simulate_imaging
from pyFPM.aberrations.dot_array.Dot_array import Dot_array
from pyFPM.aberrations.dot_array.simulate_dot_array import simulate_dot_array
from pyFPM.setup.Setup_parameters import Setup_parameters
from pyFPM.setup.Imaging_system import LED_calibration_parameters

import numpy as np




def simulate_abberated_dot_arrays(zernike_coefficients_list, dot_array: Dot_array, arraysize, 
                                  setup_parameters: Setup_parameters, pixel_scale_factor, 
                                  simulate_quadratic_phases_list, calibration_parameters: LED_calibration_parameters):
    

    low_res_image_size = setup_parameters.camera.raw_image_size
    high_res_image_size = [size * pixel_scale_factor for size in low_res_image_size]
    high_res_pixel_size = setup_parameters.camera.camera_pixel_size / pixel_scale_factor

    amplitude_image, high_res_dot_blobs = simulate_dot_array(dot_array= dot_array, image_size=high_res_image_size, 
                                                             pixel_size=high_res_pixel_size, magnification=setup_parameters.lens.magnification)

    phase_image = np.zeros(shape = amplitude_image.shape)
    high_res_complex_object = amplitude_image * np.exp(1j*phase_image)
    
    low_res_dot_blobs = high_res_dot_blobs/pixel_scale_factor

    simulated_datas = []
    pupils = []

    for zernike_coefficients, simulate_quadratic_phases in zip(zernike_coefficients_list, simulate_quadratic_phases_list):
        simulated_data, pupil, CTF = simulate_imaging(
            high_res_complex_object = high_res_complex_object,
            zernike_coefficients = zernike_coefficients,
            noise_fraction = 0,
            setup_parameters = setup_parameters,
            arraysize = arraysize,
            pixel_scale_factor = pixel_scale_factor,
            Fresnel_correction=simulate_quadratic_phases,
            spherical_illumination_correction=simulate_quadratic_phases,
            calibration_parameters = calibration_parameters,
            use_aperture_shift = False,
            patch_offset = [0,0]
        )

        simulated_datas.append(simulated_data)
        pupils.append(pupil)

    
    return simulated_datas, pupils, low_res_dot_blobs, high_res_complex_object, high_res_dot_blobs, CTF



