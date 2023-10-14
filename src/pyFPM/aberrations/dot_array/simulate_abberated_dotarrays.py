from pyFPM.simulation.simulate_imaging import simulate_imaging
from pyFPM.aberrations.dot_array.Dot_array import get_dot_array_image, Dot_array
from pyFPM.setup.Setup_parameters import Setup_parameters

import numpy as np


def simulate_dot_array(dot_array: Dot_array, image_size, pixel_size, magnification):
    dot_radius = dot_array.diameter / 2 # m
    dot_spacing = dot_array.spacing # m

    dot_array_image, dot_blobs = get_dot_array_image(
                                        dot_radius=dot_radius, 
                                        dot_spacing=dot_spacing, 
                                        image_size=image_size,
                                        object_pixel_size=pixel_size/magnification
                                        )

    return dot_array_image, dot_blobs

def simulate_abberated_dot_arrays(zernike_coefficients_list, dot_array: Dot_array, arraysize, 
                                  setup_parameters: Setup_parameters, pixel_scale_factor):

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

    for zernike_coefficients in zernike_coefficients_list:
        simulated_data, pupil, CTF = simulate_imaging(
            high_res_complex_object = high_res_complex_object,
            zernike_coefficients = zernike_coefficients,
            noise_fraction = 0,
            setup_parameters = setup_parameters,
            arraysize = arraysize,
            pixel_scale_factor = pixel_scale_factor
        )

        simulated_datas.append(simulated_data)
        pupils.append(pupil)

    
    return simulated_datas, pupils, low_res_dot_blobs, high_res_complex_object, high_res_dot_blobs, CTF



