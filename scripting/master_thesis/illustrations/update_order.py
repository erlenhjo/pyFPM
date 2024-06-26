# FPM imports
from pyFPM.NTNU_specific.simulate_images.simulate_2x import simulate_2x

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

main_result_folder = Path.cwd() / "results" / "master_thesis"
illustration_folder = main_result_folder / "illustrations"
illustration_folder.mkdir(parents=True, exist_ok=True)


def illustrate_update_order():
    
    zernike_coefficients = [0,0,0,0,0,0]

    amplitude_image = np.ones(shape=(512,512))
    phase_image = np.zeros(shape=amplitude_image.shape)
    high_res_complex_object = amplitude_image * np.exp(1j*phase_image)

    setup_parameters, data_patch, imaging_system, illumination_pattern, applied_pupil, _\
        = simulate_2x(high_res_complex_object, noise_fraction=0, zernike_coefficients=zernike_coefficients, 
                      spherical_illumination=True, patch_offset=[0, 0], use_Fresnel_shift=False, arraysize=7)
    
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(3,3), constrained_layout = True)
    cax = ax.pcolor(np.arange(-3,4), np.arange(-3,4), illumination_pattern.update_order_matrix[13:20,13:20])
    ax.set_xlabel("LED index, n")
    ax.set_ylabel("LED index, m")
    ax.xaxis.set_label_position("top")
    ax.xaxis.tick_top()
    ax.invert_yaxis()
    ax.set_aspect("equal")
    cbar = plt.colorbar(cax, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("Update index")
    
    fig.savefig(illustration_folder / "illustrate_update_order.pdf", dpi=1000)
    

if __name__ == "__main__":
    illustrate_update_order()
    plt.show()

