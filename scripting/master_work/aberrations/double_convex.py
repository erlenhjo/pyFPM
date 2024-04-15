import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

from pyFPM.experimental.recover_experiment import recover_experiment, plot_experiment, Experiment_settings

from pyFPM.recovery.algorithms.run_algorithm import Method
from pyFPM.setup.Imaging_system import LED_calibration_parameters
from pyFPM.recovery.algorithms.Step_description import get_standard_adaptive_step_description

from pyFPM.NTNU_specific.components import DOUBLE_CONVEX
from pyFPM.NTNU_specific.setup_hamamatsu import setup_hamamatsu_global, setup_hamamatsu_local




patch_offsets = np.outer(np.arange(-3,4),np.array([256,0]))
patch_size = [256, 256]
max_array_size = 7

cwd = Path.cwd()

data_folder = cwd / "data/Fourier_Ptychography"

recover = True
plot = True


def main():
    double_convex_usaf()
    plt.show()


def recover_and_plot(title, datadirpath):
    if recover:
        recover_experiment(title, datadirpath, patch_offsets, patch_size, max_array_size, experiment_settings, 
                           setup_local=setup_hamamatsu_local, setup_global=setup_hamamatsu_global)
    if plot:
        plot_experiment(title)

def double_convex_usaf():
    title = "Double convex usaf"
    datadirpath = data_folder / "double_convex_usaf"
    recover_and_plot(title, datadirpath)




experiment_settings = Experiment_settings(lens = DOUBLE_CONVEX,
                                          method = Method.Fresnel_aperture,
                                          calibration_parameters = LED_calibration_parameters(
                                                                        LED_distance=200e-3,
                                                                        LED_x_offset=0,
                                                                        LED_y_offset=0,
                                                                        LED_rotation=0
                                                                    ),
                                          step_description = get_standard_adaptive_step_description(max_iterations=50,
                                                                                                    start_EPRY_at_iteration = 0,
                                                                                                    start_adaptive_at_iteration = 10),
                                          pixel_scale_factor = 6,
                                          threshold_value = 1000,
                                          noise_reduction_regions = [
                                                                        [1100, 1100, 100, 100],
                                                                        [1600, 1600, 100, 100]
                                                                    ],
                                          defocus_guess = 0
                                          )

if __name__ == "__main__":
    main()
    
