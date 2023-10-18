from pyFPM.NTNU_specific.simulate_images.simulate_setup import simulate_setup_parameters                                          
from pyFPM.NTNU_specific.components import (HAMAMATSU_C11440_42U30, 
                                            INFINITYCORRECTED_2X,
                                            MAIN_LED_ARRAY)
from pyFPM.setup.Imaging_system import Imaging_system
from pyFPM.aberrations.pupils.zernike_pupil import get_zernike_pupil, decompose_zernike_pupil
from pyFPM.aberrations.zernike_polynomials.plot_zernike_coefficients import plot_zernike_coefficients

import matplotlib.pyplot as plt
import numpy as np

def get_setup():
    lens = INFINITYCORRECTED_2X
    LED_array = MAIN_LED_ARRAY
    array_to_object_distance = 0.200 # m
    dummy_camera = HAMAMATSU_C11440_42U30
    slide = None
    setup_parameters = simulate_setup_parameters(lens=lens, camera=dummy_camera, slide=slide, LED_array=LED_array,
                                                 array_to_object_distance=array_to_object_distance)
    
    return setup_parameters

def simulate_imaging_system():
    setup_parameters = get_setup()
    imaging_system =  Imaging_system(
        setup_parameters = setup_parameters,
        pixel_scale_factor = 1,
        patch_start = [0,0],
        patch_size = setup_parameters.camera.raw_image_size,
        )
    return imaging_system


def test_zernike_decomposition():
    max_j = 25
    zernike_coefficients = (np.random.random(max_j+1)*2 - 1) * 0.01
    zernike_coefficients[0] = 0
    
    imaging_system = simulate_imaging_system()


    pupil = get_zernike_pupil(imaging_system=imaging_system, zernike_coefficients=zernike_coefficients)
    
    fig, axes = plt.subplots(nrows=2,ncols=2)
    plot_zernike_coefficients(ax=axes[0,0], zernike_coefficients=zernike_coefficients, title="Original Zernike coefficients")
    axes[1,0].imshow(np.angle(pupil)*imaging_system.low_res_CTF, vmin=-np.pi, vmax=np.pi)
    axes[1,0].set_axis_off()
    axes[1,0].set_title("Pupil phase")

    decomposed_zernike_coefficients = decompose_zernike_pupil(imaging_system, pupil, max_j)

    plot_zernike_coefficients(ax=axes[0,1], zernike_coefficients=decomposed_zernike_coefficients, title="Recovered Zernike coefficients")
    
    error = decomposed_zernike_coefficients - zernike_coefficients
    relative_error = error[2:]/np.abs(zernike_coefficients[2:])
    axes[1,1].plot(relative_error)
    axes[1,1].set_title("Relative error")
    y_max = np.max(np.abs(relative_error))*1.2
    axes[1,1].set_ylim(-y_max, y_max)
    print(error)
    fig.tight_layout()
    plt.show()



if __name__ == "__main__":
    test_zernike_decomposition()