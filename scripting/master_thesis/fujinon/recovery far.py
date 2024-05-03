import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

from pyFPM.experimental.recover_experiment import recover_experiment, plot_experiment, Experiment_settings
from pyFPM.recovery.algorithms.run_algorithm import Method
from pyFPM.setup.Imaging_system import LED_calibration_parameters
from pyFPM.recovery.algorithms.Step_description import get_standard_adaptive_step_description

from pyFPM.NTNU_specific.components import FUJINON_MINWD_MAXNA
from pyFPM.NTNU_specific.setup_IDS_U3 import setup_IDS_U3_global, setup_IDS_U3_local

patch_size = [256, 256]
patch_offsets = [[0,-35]]
max_array_size = 7

data_folder = Path.cwd() / "data"
main_result_folder = Path.cwd() / "results" / "master_thesis" / "fujinon"

recover = True
plot = True


def main():
    fujinon_usaf_1p8()
    fujinon_usaf_4()
    fujinon_usaf_6()
    fujinon_usaf_8()


    # if plot:
    #     plt.show()

def recover_and_plot(title, datadirpath, patch_offsets, result_folder, experiment_settings):
    if recover:
        recover_experiment(title, datadirpath, patch_offsets, patch_size, max_array_size, experiment_settings, 
                           setup_local=setup_IDS_U3_local, setup_global=setup_IDS_U3_global)
    if plot:
        plot_experiment(title, result_folder)


def fujinon_usaf_1p8():
    title = "Fujinon USAF 1,8"
    datadirpath = data_folder / "Master_thesis" / "fujinon" / "fujinon_usaf_1,8_far"
    result_folder = main_result_folder / "recovery_1,8"
    experiment_settings.lens.NA = 0.044
    recover_and_plot(title, datadirpath, patch_offsets, result_folder, experiment_settings=experiment_settings)

def fujinon_usaf_4():
    title = "Fujinon USAF 4"
    datadirpath = data_folder / "Master_thesis" / "fujinon" / "fujinon_usaf_4_far"
    result_folder = main_result_folder / "recovery_4"
    experiment_settings.lens.NA = 0.044/2
    recover_and_plot(title, datadirpath, patch_offsets, result_folder, experiment_settings=experiment_settings)

def fujinon_usaf_6():
    title = "Fujinon USAF 6"
    datadirpath = data_folder / "Master_thesis" / "fujinon" / "fujinon_usaf_6_far"
    result_folder = main_result_folder / "recovery_6"
    experiment_settings.lens.NA = 0.044/3
    recover_and_plot(title, datadirpath, patch_offsets, result_folder, experiment_settings=experiment_settings)

def fujinon_usaf_8():
    title = "Fujinon USAF 8"
    datadirpath = data_folder / "Master_thesis" / "fujinon" / "fujinon_usaf_8_far"
    result_folder = main_result_folder / "recovery_8"
    experiment_settings.lens.NA = 0.044/4
    recover_and_plot(title, datadirpath, patch_offsets, result_folder, experiment_settings=experiment_settings)



experiment_settings = Experiment_settings(lens = FUJINON_MINWD_MAXNA,
                                          method = Method.Fresnel,
                                          calibration_parameters = LED_calibration_parameters(LED_distance=0.387362897785381, 
                                                                                              LED_x_offset=-0.0022187066638627503, 
                                                                                              LED_y_offset=-0.003169517388228522, 
                                                                                              LED_rotation=0.0023389768631743653),
                                          step_description = get_standard_adaptive_step_description(max_iterations=50,
                                                                                                    start_EPRY_at_iteration = 0,
                                                                                                    start_adaptive_at_iteration = 10,
                                                                                                    apply_BF_mask_from_iteration = 10),
                                          pixel_scale_factor = 8,
                                          binning_factor = 1, 
                                          threshold_value = 1000,
                                          noise_reduction_regions = [
                                                                        [0, 0, 100, 100],
                                                                        [412, 412, 100, 100]
                                                                    ],
                                          defocus_guess = 0,
                                          limited_import = [512,512]
                                          )

if __name__ == "__main__":
    main()
    
