import numpy as np
import matplotlib.pyplot as plt

from pyFPM.aberrations.dot_array.plot_dot_array import (plot_dot_error,
                                                        plot_example_dots)
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
    max_j = 25
    aberration_magnitudes = [0.1, 1, 3]
    for n in range(len(aberration_magnitudes)):
        zernike_coefficients = (np.random.random(max_j+1)*2 - 1) * aberration_magnitudes[n]
        zernike_coefficients[0] = 0
        zernike_coefficients_list.append(zernike_coefficients)

    setup_parameters = aberrated_dot_array_setup()
    dot_array = EO_DOT_ARRAY
    pixel_scale_factor = 4
    sub_precision = 4

    simulated_datas, pupils, low_res_dot_blobs, \
    high_res_complex_object, high_res_dot_blobs, CTF \
        = simulate_abberated_dot_arrays(zernike_coefficients_list, dot_array=dot_array, arraysize=1, 
                                        setup_parameters=setup_parameters, pixel_scale_factor=pixel_scale_factor)

    for j, (simulated_data, pupil, zernike_coefficients) in enumerate(zip(simulated_datas, pupils, zernike_coefficients_list)):
        image = simulated_data.amplitude_images[0]
        fig, axes = plt.subplots(nrows=2,ncols=2)

        plot_zernike_coefficients(ax=axes[0,0], zernike_coefficients=zernike_coefficients)
        axes[0,1].matshow(np.angle(pupil)*CTF, vmin=-np.pi, vmax=np.pi)
        axes[0,1].set_axis_off()
        axes[1,0].matshow(image)
        axes[1,0].set_axis_off()

        object_pixel_size = setup_parameters.camera.camera_pixel_size / setup_parameters.lens.magnification
        
        located_blobs = locate_dots(image, dot_array, object_pixel_size, sub_precision)
        blobs, grid_points, grid_indices, rotation = assemble_dots_in_grid(image, located_blobs, dot_array, object_pixel_size)
        print(f"The total rotation was {rotation} degrees")       
        plot_dot_error(ax=axes[1,1], blobs=blobs, grid_points=grid_points, 
                       grid_indices=grid_indices, object_pixel_size=object_pixel_size)

        fig.tight_layout()
        fig_2 = plt.figure()
        plot_example_dots(fig_2, image, blobs, grid_points, grid_indices, dot_array, object_pixel_size)


    plt.show()



def profile_main():
    import cProfile
    import pstats

    with cProfile.Profile() as pr:
        main()
    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.dump_stats(filename=r"profiling_data\dot_locating.prof")

def main():
    plot_abberated_dot_arrays()

if __name__ == "__main__":
    profile_main()



