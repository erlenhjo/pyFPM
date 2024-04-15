from pyFPM.NTNU_specific.simulate_images.simulate_setup import simulate_setup_parameters                                          
from pyFPM.NTNU_specific.components import (HAMAMATSU_C11440_42U30, 
                                            INFINITYCORRECTED_2X,
                                            MAIN_LED_ARRAY)
from pyFPM.setup.Imaging_system import Imaging_system, LED_calibration_parameters
from pyFPM.aberrations.pupils.zernike_pupil import get_zernike_pupil, decompose_zernike_pupil
from pyFPM.aberrations.zernike_polynomials.plot_zernike_coefficients import plot_zernike_coefficients

from arrow import add_arrow, Arrow_style, Arrow_text

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

main_result_folder = Path.cwd() / "results" / "master_thesis"
illustration_folder = main_result_folder / "illustrations"
illustration_folder.mkdir(parents=True, exist_ok=True)

def get_setup():
    lens = INFINITYCORRECTED_2X
    LED_array = MAIN_LED_ARRAY
    dummy_camera = HAMAMATSU_C11440_42U30
    setup_parameters = simulate_setup_parameters(lens=lens, camera=dummy_camera, LED_array=LED_array)
    
    return setup_parameters

def simulate_imaging_system():
    setup_parameters = get_setup()
    imaging_system =  Imaging_system(
        setup_parameters = setup_parameters,
        pixel_scale_factor = 1,
        patch_offset = [0,0],
        patch_size = setup_parameters.camera.raw_image_size,
        calibration_parameters=LED_calibration_parameters(200e-3,0,0,0)
        )
    return imaging_system


def test_zernike_decomposition():
    max_j = 25
    zernike_coefficients = (np.random.random(max_j+1)*2 - 1) * 0.5
    zernike_coefficients[0] = 0
    
    imaging_system = simulate_imaging_system()


    pupil = get_zernike_pupil(imaging_system=imaging_system, zernike_coefficients=zernike_coefficients)
    
    fig = plt.figure(figsize=(9,4), constrained_layout=True)
    gs = fig.add_gridspec(4, 8)

    axes_0 = plt.subplot(gs[0:2, 0:3])
    axes_1 = plt.subplot(gs[0:4, 3:8])
    axes_2 = plt.subplot(gs[2:4, 0:3])


    plot_zernike_coefficients(ax=axes_0, zernike_coefficients=zernike_coefficients, title="Original Zernike coefficients")
    

    nonzero_y, nonzero_x = np.nonzero(imaging_system.low_res_CTF)
    min_x, max_x = np.min(nonzero_x), np.max(nonzero_x)
    min_y, max_y = np.min(nonzero_y), np.max(nonzero_y)

    cropped_low_res_CTF = imaging_system.low_res_CTF[min_y:max_y, min_x:max_x]
    cropped_pupil = pupil[min_y:max_y, min_x:max_x]

    pupil_phase = np.ma.masked_where(cropped_low_res_CTF == 0, np.angle(cropped_pupil))


    cax = axes_1.imshow(pupil_phase, vmin=-np.pi, vmax=np.pi)
    axes_1.set_axis_off()
    cbar = plt.colorbar(cax, ax=axes_1)
    cbar.set_label("Phase")
    axes_1.set_title("Pupil phase")

    decomposed_zernike_coefficients = decompose_zernike_pupil(imaging_system, pupil, max_j)

    plot_zernike_coefficients(ax=axes_2, zernike_coefficients=decomposed_zernike_coefficients, title="Recovered Zernike coefficients")

    #add arrows
    arrow_style = Arrow_style(
        face_color = "r",
        edge_color = "k",
        connection_style = "arc3, rad=-0.3",
        arrow_style = "simple",
        alpha = 0.7,
        mutation_scale = 30
    )

    arrow_text_1 = Arrow_text(
        text = "Synthesis",
        relative_x = 0,
        relative_y = -0.04,
        font_size = "large"
    )

    arrow_text_2 = Arrow_text(
        text = "Decomposition",
        relative_x = 0,
        relative_y = 0.04,
        font_size = "large"
    )

    axes_0.set_xlim() # needed for some reason?
    axes_0.set_ylim()
    axes_1.set_xlim()
    axes_1.set_ylim()
    axes_2.set_xlim()
    axes_2.set_ylim()
    
    # y_max = 1404 aprox.

    add_arrow(fig=fig, ax_from=axes_1, ax_to=axes_1,
              coord_from=(-100,100), coord_to=(400,100),
              arrow_style=arrow_style, arrow_text=arrow_text_1)
    add_arrow(fig=fig, ax_from=axes_1, ax_to=axes_1,
              coord_from=(400,1300), coord_to=(-100,1300),
              arrow_style=arrow_style, arrow_text=arrow_text_2)

    fig.savefig(illustration_folder / "zernike_example.png")
    fig.savefig(illustration_folder / "zernike_example.pdf")


if __name__ == "__main__":
    test_zernike_decomposition()
    plt.show()