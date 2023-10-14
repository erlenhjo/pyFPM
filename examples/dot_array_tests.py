import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from numpy.fft import fft2, ifftshift, fftshift

from pyFPM.aberrations.dot_array.plot_dot_array import (plot_located_dots,
                                                        plot_located_dots_vs_grid,
                                                        plot_located_dot_error)
from pyFPM.aberrations.dot_array.locate_dot_array import (locate_dots,
                                                          assemble_dots_in_grid) 
from pyFPM.NTNU_specific.simulate_images.simulate_setup import simulate_setup_parameters                                          
from pyFPM.NTNU_specific.components import (HAMAMATSU_C11440_42U30, 
                                            INFINITYCORRECTED_2X,
                                            EO_DOT_ARRAY,
                                            MAIN_LED_ARRAY)
from pyFPM.aberrations.dot_array.simulate_abberated_dotarrays import simulate_abberated_dot_arrays

def locate_and_plot_dots():
    filepath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\EHJ20230915_dotarray_2x_inf\0_10-16_16.tiff"

    image = np.array(Image.open(filepath))

    dot_radius = EO_DOT_ARRAY.diameter/2
    dot_spacing = EO_DOT_ARRAY.spacing
    pixel_size = HAMAMATSU_C11440_42U30.camera_pixel_size
    magnification = INFINITYCORRECTED_2X.magnification

    object_pixel_size = pixel_size / magnification

    filtered_blobs, blobs_LoG, blobs_DoG = locate_dots(image, dot_radius, object_pixel_size)

    plot_located_dots(image, [filtered_blobs, blobs_LoG, blobs_DoG])
    blobs, grid_points, grid_indices, rotation = assemble_dots_in_grid(image.shape, filtered_blobs, dot_spacing, object_pixel_size)
    print(f"The total rotation was {rotation} degrees")
    plot_located_dots_vs_grid(image, blobs, grid_points)
    plot_located_dot_error(blobs, grid_points, grid_indices, object_pixel_size)
    plt.show()


def aberrated_dot_array_setup():
    lens = INFINITYCORRECTED_2X
    LED_array = MAIN_LED_ARRAY
    array_to_object_distance = 0.200 # m
    dummy_camera = HAMAMATSU_C11440_42U30
    slide = None
    setup_parameters = simulate_setup_parameters(lens=lens, camera=dummy_camera, slide=slide, LED_array=LED_array,
                                                 array_to_object_distance=array_to_object_distance)
    
    return setup_parameters

def plot_abberated_dot_arrays():
    zernike_coefficients_list = []
    N = 10
    magnitude = 0.1
    for j in range(1, 10):
        zernike_coefficients = np.zeros(N+1)
        zernike_coefficients[j] = magnitude
        zernike_coefficients_list.append(zernike_coefficients)

    setup_parameters = aberrated_dot_array_setup()
    dot_array = EO_DOT_ARRAY
    pixel_scale_factor = 4

    simulated_datas, pupils, low_res_dot_blobs, \
    high_res_complex_object, high_res_dot_blobs, CTF \
        = simulate_abberated_dot_arrays(zernike_coefficients_list, dot_array=dot_array, arraysize=1, 
                                        setup_parameters=setup_parameters, pixel_scale_factor=pixel_scale_factor)

    for j, (simulated_data, pupil) in enumerate(zip(simulated_datas, pupils)):
        image = simulated_data.amplitude_images[0]
        #locate_and_plot_dots()
        fig, axes = plt.subplots(nrows=1,ncols=3)
        axes[0].matshow(image)
        axes[1].matshow(np.log(np.abs(fftshift(fft2(ifftshift(image))))**2*CTF))
        axes[2].matshow(np.angle(pupil)*CTF)

    plt.show()


def profile_main():
    import cProfile
    import pstats

    with cProfile.Profile() as pr:
        main()
    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.dump_stats(filename=r"profiling_data\dot_array_profile_all.prof")

def main():
    locate_and_plot_dots()
    plot_abberated_dot_arrays()

if __name__ == "__main__":
    profile_main()
