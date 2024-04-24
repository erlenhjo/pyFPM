import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

from pyFPM.experimental.plot_illumination import plot_bright_field_images_with_BF_edge
from pyFPM.NTNU_specific.simulate_images.only_illumination import simulate_illumination
from pyFPM.setup.Setup_parameters import Lens, Lens_type
from pyFPM.setup.Imaging_system import LED_calibration_parameters
from pyFPM.NTNU_specific.components import IDS_U3_31J0CP_REV_2_2


lens = Lens(
    NA = 0.05,
    magnification = 2,
    focal_length = 60e-3,
    working_distance = None,
    depth_of_field = None,
    max_FoV_sensor = None,
    lens_type = Lens_type.SINGLE_LENS
)
camera = IDS_U3_31J0CP_REV_2_2
array_size = 5

main_result_folder = Path.cwd() / "results" / "master_thesis"
illustration_folder = main_result_folder / "illustrations"
illustration_folder.mkdir(parents=True, exist_ok=True)

def illustrate_illumination_from_simulation(lens, camera,
                                            spherical, Fresnel, 
                                            z_LED, arraysize, 
                                            patch_offset=[0,0]):
    setup_parameters, data_patch, imaging_system, illumination_pattern, applied_pupil, high_res_complex_object\
       = simulate_illumination(lens = lens, 
                               camera = camera,
                               correct_spherical_wave_illumination = spherical, 
                               correct_Fresnel_propagation = Fresnel,
                               arraysize=arraysize,
                               calibration_parameters=LED_calibration_parameters(z_LED,0,0,0),
                               patch_offset=patch_offset)
    fig = plot_bright_field_images_with_BF_edge(data_patch=data_patch, 
                                                setup_parameters=setup_parameters, 
                                                calibration_parameters=LED_calibration_parameters(z_LED,0,0,0),
                                                array_size=arraysize,
                                                Fresnel = Fresnel)

    return fig


def illustrate_BF_edge():
    fig = illustrate_illumination_from_simulation(lens=lens, camera=camera,
                                                  spherical=True, Fresnel=True, 
                                                  z_LED=200e-3, arraysize=array_size)
    fig.savefig(illustration_folder / "illustrate_BF_edge.pdf")
    fig.savefig(illustration_folder / "illustrate_BF_edge.png")


if __name__ == "__main__": 
    illustrate_BF_edge()
    plt.show()