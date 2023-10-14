from pyFPM.NTNU_specific.components import INFINITYCORRECTED_2X, MAIN_LED_ARRAY, HAMAMATSU_C11440_42U30, EO_DOT_ARRAY
from pyFPM.NTNU_specific.simulations.simulate_imaging import simulate_imaging
from pyFPM.aberrations.dot_array.Dot_array import get_dot_array_image
from pyFPM.setup.Setup_parameters import Camera

import numpy as np
import matplotlib.pyplot as plt
from numpy.fft import fft2, ifftshift, fftshift

def simulate_dot_array(image_size, pixel_size, magnification):
    dot_radius = EO_DOT_ARRAY.diameter / 2 # m
    dot_spacing = EO_DOT_ARRAY.spacing # m

    dot_array_image, _ = get_dot_array_image(
                                        dot_radius=dot_radius, 
                                        dot_spacing=dot_spacing, 
                                        image_size=image_size,
                                        object_pixel_size=pixel_size/magnification
                                        )

    return dot_array_image

def simulate_abberated_dot_arrays(zernike_coefficients_list, arraysize):
    
    lens = INFINITYCORRECTED_2X
    LED_array = MAIN_LED_ARRAY
    array_to_object_distance = 0.200 # m
    dummy_camera = HAMAMATSU_C11440_42U30
    dummy_camera = Camera(
            camera_pixel_size = 6.5e-6,
            raw_image_size = [512, 512],
            bit_depth = int(2**8-1)
            )

    low_res_image_size = dummy_camera.raw_image_size
    pixel_scale_factor = 2
    high_res_image_size = [size * pixel_scale_factor for size in low_res_image_size]
    high_res_pixel_size = dummy_camera.camera_pixel_size / pixel_scale_factor

    amplitude_image = simulate_dot_array(image_size = high_res_image_size, pixel_size=high_res_pixel_size, magnification=INFINITYCORRECTED_2X.magnification)
    phase_image = np.zeros(shape = amplitude_image.shape)
    high_res_complex_object = amplitude_image * np.exp(1j*phase_image)
    
    simulated_datas = []
    pupils = []

    for zernike_coefficients in zernike_coefficients_list:
        setup_parameters, simulated_data, pupil, CTF = simulate_imaging(
            high_res_complex_object = high_res_complex_object,
            zernike_coefficients = zernike_coefficients,
            noise_fraction = 0,
            camera = dummy_camera,
            lens = lens,
            LED_array = LED_array,
            array_to_object_distance = array_to_object_distance,
            arraysize = arraysize,
            pixel_scale_factor = pixel_scale_factor
        )

        simulated_datas.append(simulated_data)
        pupils.append(pupil)

    
    return simulated_datas, pupils, CTF

def plot_abberated_dot_arrays():
    zernike_coefficients_list = []
    N = 10
    magnitude = 0.1
    for j in range(1, 10):
        zernike_coefficients = np.zeros(N+1)
        zernike_coefficients[j] = magnitude
        zernike_coefficients_list.append(zernike_coefficients)

    simulated_datas, pupils, CTF = simulate_abberated_dot_arrays(zernike_coefficients_list, arraysize=1)

    for j, (simulated_data, pupil) in enumerate(zip(simulated_datas, pupils)):
        image = simulated_data.amplitude_images[0]
        fig, axes = plt.subplots(nrows=1,ncols=3)
        axes[0].matshow(image)
        axes[1].matshow(np.log(np.abs(fftshift(fft2(ifftshift(image))))**2*CTF))
        axes[2].matshow(np.angle(pupil)*CTF)

    plt.show()

