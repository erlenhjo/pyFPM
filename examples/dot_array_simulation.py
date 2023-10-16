import numpy as np
import matplotlib.pyplot as plt

from pyFPM.aberrations.dot_array.plot_dot_array import (plot_located_dots,
                                                        plot_located_dots_vs_grid,
                                                        plot_located_dot_error,
                                                        plot_dot_error)
from pyFPM.aberrations.dot_array.locate_dot_array import (locate_dots,
                                                          assemble_dots_in_grid) 
from pyFPM.NTNU_specific.simulate_images.simulate_setup import simulate_setup_parameters                                          
from pyFPM.NTNU_specific.components import (HAMAMATSU_C11440_42U30, 
                                            INFINITYCORRECTED_2X,
                                            EO_DOT_ARRAY,
                                            MAIN_LED_ARRAY)
from pyFPM.aberrations.dot_array.simulate_abberated_dotarrays import simulate_abberated_dot_arrays
from pyFPM.aberrations.zernike_polynomials.plot_zernike_coefficients import plot_zernike_coefficients


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
    N = 25
    magnitude = 1
    for j in range(4, 5):
        zernike_coefficients = np.zeros(N+1)
        zernike_coefficients[j] = magnitude
        zernike_coefficients_list.append(zernike_coefficients)

    setup_parameters = aberrated_dot_array_setup()
    dot_array = EO_DOT_ARRAY
    pixel_scale_factor = 1

    simulated_datas, pupils, low_res_dot_blobs, \
    high_res_complex_object, high_res_dot_blobs, CTF \
        = simulate_abberated_dot_arrays(zernike_coefficients_list, dot_array=dot_array, arraysize=1, 
                                        setup_parameters=setup_parameters, pixel_scale_factor=pixel_scale_factor)

    for j, (simulated_data, pupil, zernike_coefficients) in enumerate(zip(simulated_datas, pupils, zernike_coefficients_list)):
        image = simulated_data.amplitude_images[0]
        #locate_and_plot_dots()
        fig, axes = plt.subplots(nrows=2,ncols=2)
        axes: list[plt.Axes] = axes.flatten()
        axes[0].matshow(image)
        plot_zernike_coefficients(ax=axes[1], zernike_coefficients=zernike_coefficients)
        axes[2].matshow(np.angle(pupil)*CTF)

        object_pixel_size = setup_parameters.camera.camera_pixel_size / setup_parameters.lens.magnification
        
        a=4
        image_with_more_pixels = increase_pixel_count(image=image, scaling_factor=a)
        filtered_blobs, blobs_LoG, blobs_DoG = locate_dots(image_with_more_pixels, dot_array.diameter/2, object_pixel_size/a)
        filtered_blobs, blobs_LoG, blobs_DoG = filtered_blobs/a, blobs_LoG/a, blobs_DoG/a
        #filtered_blobs, blobs_LoG, blobs_DoG = locate_dots(image, dot_array.diameter/2, object_pixel_size)

        #plot_located_dots(image, [filtered_blobs, blobs_LoG, blobs_DoG])
        blobs, grid_points, grid_indices, rotation = assemble_dots_in_grid(image.shape, filtered_blobs, dot_array.spacing, object_pixel_size)
        print(f"The total rotation was {rotation} degrees")
        plot_located_dots_vs_grid(image, blobs, grid_points)

        plot_dot_error(ax=axes[3], blobs=blobs, grid_points=grid_points, 
                       grid_indices=grid_indices, object_pixel_size=object_pixel_size)
        fig.tight_layout()

    plt.show()

def increase_pixel_count(image, scaling_factor):
    ones = np.ones(shape = (scaling_factor, scaling_factor))
    return np.kron(image, ones)

def profile_main():
    import cProfile
    import pstats

    with cProfile.Profile() as pr:
        main()
    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.dump_stats(filename=r"profiling_data\dot_array_profile_all.prof")

def main():
    #locate_and_plot_dots()
    plot_abberated_dot_arrays()

if __name__ == "__main__":
    profile_main()



