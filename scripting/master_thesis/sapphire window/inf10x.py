import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

from pyFPM.experimental.recover_experiment import recover_experiment, plot_experiment, Experiment_settings
from pyFPM.recovery.algorithms.run_algorithm import Method
from pyFPM.setup.Imaging_system import LED_calibration_parameters
from pyFPM.recovery.algorithms.Step_description import get_standard_adaptive_step_description

from pyFPM.NTNU_specific.components import INFINITYCORRECTED_10X
from pyFPM.NTNU_specific.setup_IDS_U3 import setup_IDS_U3_global, setup_IDS_U3_local

patch_size = [512, 512]
max_array_size = 11

data_folder = Path.cwd() / "data"
main_result_folder = Path.cwd() / "results" / "master_thesis" / "window"

recover = True
plot = True


def main():
    inf10x_usaf_window()
    inf10x_usaf_windowless()

    if plot:
        plt.show()

def recover_and_plot(title, datadirpath, patch_offsets, result_folder):
    if recover:
        recover_experiment(title, datadirpath, patch_offsets, patch_size, max_array_size, experiment_settings, 
                           setup_local=setup_IDS_U3_local, setup_global=setup_IDS_U3_global)
    if plot:
        plot_experiment(title, result_folder)


def inf10x_usaf_window():
    patch_offsets = [np.array([-316,-26])]
    title = "Infinity 10x USAF window"
    datadirpath = data_folder / "Master_thesis" / "sapphire window" / "inf10x_usaf_window_200mm"
    result_folder = main_result_folder / "inf10x_recover_window"
    recover_and_plot(title, datadirpath, patch_offsets, result_folder)

def inf10x_usaf_windowless():
    patch_offsets = [np.array([-271,-216])]
    title = "Infinity 10x usaf windowless"
    datadirpath = data_folder / "Master_thesis" / "sapphire window" / "inf10x_usaf_200mm"
    result_folder = main_result_folder / "inf10x_recover"
    recover_and_plot(title, datadirpath, patch_offsets, result_folder)


experiment_settings = Experiment_settings(lens = INFINITYCORRECTED_10X,
                                          method = Method.Fresnel,
                                          calibration_parameters = LED_calibration_parameters(LED_distance=0.20153892853221111, 
                                                                                              LED_x_offset=-0.00012446193565815314, 
                                                                                              LED_y_offset=-0.00012741088856773426, 
                                                                                              LED_rotation=-0.0010187545121927496
                                                                                              ),
                                          step_description = get_standard_adaptive_step_description(max_iterations=50,
                                                                                                    start_EPRY_at_iteration = 0,
                                                                                                    start_adaptive_at_iteration = 10,
                                                                                                    apply_BF_mask_from_iteration = 10),
                                          pixel_scale_factor = 6,
                                          binning_factor = 1, 
                                          threshold_value = 1000,
                                          noise_reduction_regions = [
                                                                        [0, 0, 100, 100],
                                                                        [1100, 1100, 100, 100]
                                                                    ],
                                          defocus_guess = 0,
                                          limited_import = [1200,1200]
                                          )

if __name__ == "__main__":
    main()
    
