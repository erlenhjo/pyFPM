import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

from pyFPM.experimental.recover_experiment import recover_experiment, plot_experiment, Experiment_settings
from pyFPM.recovery.algorithms.run_algorithm import Method
from pyFPM.setup.Imaging_system import LED_calibration_parameters
from pyFPM.recovery.algorithms.Step_description import get_standard_adaptive_step_description

from pyFPM.NTNU_specific.components import COMPACT_2X
from pyFPM.NTNU_specific.setup_IDS_U3 import setup_IDS_U3_global, setup_IDS_U3_local

patch_offsets = [[0,0]]  #np.outer(np.arange(-5,6),np.array([256,0]))-np.array([0,256])
patch_size = [256, 256]
max_array_size = 3

cwd = Path.cwd()
data_folder = cwd / "data"

recover = True
plot = True


def main():
    compact2x_phase_target_test()
    compact2x_usaf_test()

    plt.show()

def recover_and_plot(title, datadirpath):
    if recover:
        recover_experiment(title, datadirpath, patch_offsets, patch_size, max_array_size, experiment_settings, 
                           setup_local=setup_IDS_U3_local, setup_global=setup_IDS_U3_global)
    if plot:
        plot_experiment(title)


def compact2x_usaf_test():
    title = "Compact 2x USAF test uncalibrated with mask"
    datadirpath = data_folder / "Master_thesis" / "calibration_test" / "com2x_usaf_calib_test_175"
    recover_and_plot(title, datadirpath)

def compact2x_phase_target_test():
    title = "Compact 2x phase target test uncalibrated with mask"
    datadirpath = data_folder / "Master_thesis" / "calibration_test" / "com2x_phasefocus_calib_test_175"
    recover_and_plot(title, datadirpath)


experiment_settings = Experiment_settings(lens = COMPACT_2X,
                                          method = Method.Fresnel,
                                          calibration_parameters = LED_calibration_parameters(
                                                                        LED_distance=175e-3,
                                                                        LED_x_offset=0,
                                                                        LED_y_offset=0,
                                                                        LED_rotation=0
                                                                    ),
                                          step_description = get_standard_adaptive_step_description(max_iterations=50,
                                                                                                    start_EPRY_at_iteration = 0,
                                                                                                    start_adaptive_at_iteration = 0),
                                          pixel_scale_factor = 6,
                                          binning_factor = 3, 
                                          threshold_value = 1000,
                                          noise_reduction_regions = [
                                                                        [500, 500, 100, 100],
                                                                        [800, 800, 100, 100]
                                                                    ],
                                          defocus_guess = 0,
                                          mask_BF_edge = True
                                          )

if __name__ == "__main__":
    main()
    
