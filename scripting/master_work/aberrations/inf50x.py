import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

from pyFPM.experimental.recover_experiment import recover_experiment, plot_experiment, Experiment_settings
from pyFPM.recovery.algorithms.run_algorithm import Method
from pyFPM.setup.Imaging_system import LED_calibration_parameters
from pyFPM.recovery.algorithms.Step_description import get_standard_adaptive_step_description

from pyFPM.NTNU_specific.components import INFINITYCORRECTED_50X
from pyFPM.NTNU_specific.setup_IDS_U3 import setup_IDS_U3_global, setup_IDS_U3_local

patch_offsets = [[0,0]] #np.outer(np.arange(-5,6),np.array([256,0]))-np.array([0,256])
patch_size = [1024, 1024]
max_array_size = 3

cwd = Path.cwd()
data_folder = cwd / "data/Master_thesis"

recover = True
plot = True


def main():
    inf50x_usaf_window()
    inf50x_usaf_no_window()
    plt.show()

def recover_and_plot(title, datadirpath):
    if recover:
        recover_experiment(title, datadirpath, patch_offsets, patch_size, max_array_size, experiment_settings, 
                           setup_local=setup_IDS_U3_local, setup_global=setup_IDS_U3_global)
    if plot:
        plot_experiment(title)


def inf50x_usaf_window():
    title = "Infinity 50x USAF Window"
    datadirpath = data_folder / "window" / "usaf_50x_inf_window_best_focus"
    recover_and_plot(title, datadirpath)

def inf50x_usaf_no_window():
    title = "Infinity 50x USAF no Window"
    datadirpath = data_folder / "window" / "usaf_50x_inf_no_window"
    recover_and_plot(title, datadirpath)



experiment_settings = Experiment_settings(lens = INFINITYCORRECTED_50X,
                                          method = Method.Fresnel_illumination_only,
                                          calibration_parameters = LED_calibration_parameters(
                                                                        LED_distance=40e-3,
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
    
