from pyFPM.NTNU_specific.setup_2x_hamamatsu import setup_2x_hamamatsu
from pyFPM.NTNU_specific.setup_3x_telecentric_hamamatsu import setup_3x_telecentric_hamamatsu
from pyFPM.recovery.algorithms.run_algorithm import recover, Method
from pyFPM.aberrations.pupils.defocused_pupil import get_defocused_pupil
from pyFPM.NTNU_specific.components import EO_DOT_ARRAY
from pyFPM.aberrations.dot_array.plot_dot_array import (plot_dot_error,
                                                        plot_example_dots)
from pyFPM.aberrations.zernike_polynomials.plot_zernike_coefficients import plot_zernike_coefficients
from pyFPM.aberrations.pupils.zernike_pupil import decompose_zernike_pupil
from pyFPM.aberrations.dot_array.locate_dot_array import (locate_dots,
                                                          assemble_dots_in_grid) 
from pyFPM.recovery.algorithms.Algorithm_result import Algorithm_result
from pyFPM.recovery.algorithms.Step_description import get_standard_adaptive_step_description
from plotting.plot_experimental_results import plot_experimental_results

import numpy as np
import matplotlib.pyplot as plt

def locate_recovered_dots():

    #datadirpath = r"c:\Users\erlen\Documents\GitHub\pyFPM\data\dotarray_2x_dark_object"
    datadirpath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\dotarray_telecentric3x_dark"


    pixel_scale_factor = 4
    patch_start = [767,767]
    patch_size = [512, 512] # [x, y]

    method = Method.Fraunhofer_Epry

    setup_parameters, data_patch, imaging_system, illumination_pattern = setup_3x_telecentric_hamamatsu(
        datadirpath = datadirpath,
        patch_start = patch_start,
        patch_size = patch_size,
        pixel_scale_factor = pixel_scale_factor
    )

    # define step description
    step_description = get_standard_adaptive_step_description(illumination_pattern, max_iterations=200)
    step_description.beta = 1

    # define pupil guess
    defocus_guess = 0
    pupil_guess = get_defocused_pupil(imaging_system = imaging_system, defocus = defocus_guess)

    algorithm_result: Algorithm_result = recover(method=method, data_patch=data_patch, imaging_system=imaging_system,
                                                illumination_pattern=illumination_pattern, pupil_guess=pupil_guess,
                                                step_description=step_description)

    max_j = 25
    dot_array = EO_DOT_ARRAY
    sub_precision = 4

    CTF = imaging_system.low_res_CTF
    image = np.abs(algorithm_result.recovered_object)
    pupil = algorithm_result.pupil

    fig, axes = plt.subplots(nrows=2,ncols=2)

    zernike_coefficients = decompose_zernike_pupil(imaging_system, pupil, max_j)

    plot_zernike_coefficients(ax=axes[0,0], zernike_coefficients=zernike_coefficients)
    axes[0,1].matshow(np.angle(pupil)*CTF, vmin=-np.pi, vmax=np.pi)
    axes[0,1].set_axis_off()
    axes[0,1].set_title("Pupil phase")
    axes[1,0].matshow(image)
    axes[1,0].set_axis_off()
    axes[1,0].set_title("Recovered image")

    object_pixel_size = setup_parameters.camera.camera_pixel_size / (setup_parameters.lens.magnification * pixel_scale_factor)

    located_blobs = locate_dots(image, dot_array, object_pixel_size, sub_precision)
    blobs, grid_points, grid_indices, rotation = assemble_dots_in_grid(image, located_blobs, dot_array, object_pixel_size)
    print(f"The total rotation was {rotation} degrees")       
    plot_dot_error(ax=axes[1,1], blobs=blobs, grid_points=grid_points, 
                    grid_indices=grid_indices, object_pixel_size=object_pixel_size)

    fig.tight_layout()
    fig_2 = plt.figure()
    plot_example_dots(fig_2, image, blobs, grid_points, grid_indices, dot_array, object_pixel_size)

    plot_experimental_results(data_patch,illumination_pattern,imaging_system,algorithm_result,max_j)

    plt.show()


def profile_main():
    import cProfile
    import pstats

    with cProfile.Profile() as pr:
        main()
    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.dump_stats(filename=r"profiling_data\dot_array_recovered_real.prof")

def main():
    locate_recovered_dots()

if __name__ == "__main__":
    profile_main()