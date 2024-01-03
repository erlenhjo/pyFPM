import numpy as np
import matplotlib.pyplot as plt

from pyFPM.aberrations.dot_array.plot_dot_array import (plot_dot_error,
                                                        plot_example_dots)
from pyFPM.aberrations.dot_array.locate_dot_array import (locate_dots,
                                                          assemble_dots_in_grid) 
from pyFPM.NTNU_specific.simulate_images.simulate_setup import simulate_setup_parameters                                          
from pyFPM.NTNU_specific.components import (HAMAMATSU_C11440_42U30, 
                                            DOUBLE_CONVEX, 
                                            INFINITYCORRECTED_2X,
                                            COMPACT_2X,
                                            EO_DOT_ARRAY,
                                            MAIN_LED_ARRAY)
from pyFPM.aberrations.dot_array.simulate_abberated_dotarrays import simulate_abberated_dot_arrays
from pyFPM.aberrations.zernike_polynomials.plot_zernike_coefficients import plot_zernike_coefficients
from pyFPM.setup.Imaging_system import LED_calibration_parameters

result_folder = r"C:\Users\erlen\Documents\GitHub\pyFPM\examples\project_thesis\results\magnification_simulation"

def aberrated_dot_array_setup():
    lens = COMPACT_2X
    LED_array = MAIN_LED_ARRAY
    dummy_camera = HAMAMATSU_C11440_42U30
    setup_parameters = simulate_setup_parameters(lens=lens, camera=dummy_camera, LED_array=LED_array)
    
    calibration_parameters = LED_calibration_parameters(200e-3, 0, 0, 0)

    return setup_parameters, calibration_parameters

def plot_abberated_dot_arrays():
    zernike_coefficients_list = []
    max_j = 25
    aberration_magnitudes = [0, 0, 1, 1]
    simulate_quadratic_phases_list = [False, True, False, True] 
    titles = ["normal", "quadratic", "defocused","defocused_quadratic"]
    for n in range(len(aberration_magnitudes)):
        zernike_coefficients = np.zeros(12)
        zernike_coefficients[4] = aberration_magnitudes[n] 
        zernike_coefficients_list.append(zernike_coefficients)

    setup_parameters, calibration_parameters = aberrated_dot_array_setup()
    dot_array = EO_DOT_ARRAY
    pixel_scale_factor = 4
    sub_precision = 8

    simulated_datas, pupils, low_res_dot_blobs, \
    high_res_complex_object, high_res_dot_blobs, CTF \
        = simulate_abberated_dot_arrays(zernike_coefficients_list, dot_array=dot_array, arraysize=1, 
                                        setup_parameters=setup_parameters, pixel_scale_factor=pixel_scale_factor,
                                        simulate_quadratic_phases_list=simulate_quadratic_phases_list, 
                                        calibration_parameters=calibration_parameters)
    

    for simulated_data, pupil, zernike_coefficients, title in zip(simulated_datas, pupils, zernike_coefficients_list, titles):
        image = simulated_data.amplitude_images[0]

        object_pixel_size = setup_parameters.camera.camera_pixel_size / setup_parameters.lens.magnification
        
        located_blobs = locate_dots(image, dot_array, object_pixel_size, sub_precision)
        blobs, grid_points, grid_indices, rotation, \
            center_dot_indices, image_center_coords = assemble_dots_in_grid(image, located_blobs, dot_array, object_pixel_size)

        fig_0, axes_0 = plt.subplots(nrows=1, ncols=1, figsize=(2.5,2.5), constrained_layout = True)
        axes_0.matshow(image)
        axes_0.set_axis_off()

        print(f"The total rotation was {rotation} degrees")       

        fig_1, axes_1 = plt.subplots(nrows=1, ncols=1, figsize=(3,2.5), constrained_layout=True)
        plot_dot_error(ax=axes_1, blobs=blobs, grid_points=grid_points, 
                       grid_indices=grid_indices, object_pixel_size=object_pixel_size)


        fig_2, axes_2 = plt.subplots(nrows=3, ncols=3, figsize=(5,5), constrained_layout=True)
        plot_example_dots(axes_2, image, blobs, grid_points, grid_indices, dot_array, object_pixel_size, center_dot_indices)
        
        fig_0.savefig(result_folder+f"\magnification_simulation_{title}_image.pdf", dpi = 1000)
        fig_1.savefig(result_folder+f"\magnification_simulation_{title}_error_matrix.pdf", dpi = 1000)
        fig_2.savefig(result_folder+f"\magnification_simulation_{title}_example_dots.pdf", dpi = 1000)
        

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



