import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

from pyFPM.experimental.recover_experiment import recover_experiment, Experiment_settings
from pyFPM.experimental.pickle_results import plot_pickled_experiment, compare_experiment_pupils
from pyFPM.experimental.plot_info import Plot_types, Plot_parameters, Zoom_location
from pyFPM.recovery.algorithms.run_algorithm import Method
from pyFPM.setup.Imaging_system import LED_calibration_parameters
from pyFPM.recovery.algorithms.Step_description import get_standard_adaptive_step_description

from pyFPM.NTNU_specific.components import TELECENTRIC_3X
from pyFPM.NTNU_specific.setup_IDS_U3 import setup_IDS_U3_global, setup_IDS_U3_local

patch_size = [512, 512]
max_array_size = 13

data_folder = Path.cwd() / "data"
main_result_folder = Path.cwd() / "results" / "master_thesis" / "window"

recover = False
plot = True


def main():
    # telecentric3x_usaf_window()
    # plt.close("all")
    # telecentric3x_usaf_windowless()
    # plt.close("all")
    compare_zernike()
    plt.close("all")

    if plot:
        plt.show()

def recover_and_plot(title, datadirpath, patch_offsets, result_folder):
    if recover:
        recover_experiment(title, datadirpath, patch_offsets, patch_size, max_array_size, experiment_settings, 
                           setup_local=setup_IDS_U3_local, setup_global=setup_IDS_U3_global)
    if plot:
        plot_pickled_experiment(title, result_folder, plot_types, plot_parameters)


def telecentric3x_usaf_window():
    patch_offsets = [[-45,39]]
    title = "Telecentric 3x usaf window"
    datadirpath = data_folder / "Master_thesis" / "sapphire window" / "tele3x_usaf_window_200mm"
    recover_and_plot(title, datadirpath, patch_offsets, main_result_folder)

def telecentric3x_usaf_windowless():
    patch_offsets = [[-35,-21]]
    title = "Telecentric 3x usaf windowless"
    datadirpath = data_folder / "Master_thesis" / "sapphire window" / "tele3x_usaf_200mm"
    recover_and_plot(title, datadirpath, patch_offsets, main_result_folder)

def compare_zernike():
    titles = ["Telecentric 3x usaf windowless", "Telecentric 3x usaf window"]
    labels = ["No window", "Window"]
    compare_experiment_pupils(experiment_names=titles,
                                          result_folder=main_result_folder,
                                          plot_parameters=plot_parameters,
                                          labels=labels, lens_name = "telecentric3x",
                                          pupil_amplitude_limits = [0.2, 1.4], 
                                          pupil_phase_limits = [-0.86, 0.86])


experiment_settings = Experiment_settings(lens = TELECENTRIC_3X,
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
                                          limited_import = [1200,1200],
                                          circular_LED_pattern = True
                                          )

plot_types = Plot_types(overview = 0, 
                        object_overview = 0,
                        raw_image_with_zoom = 1,
                        recovered_intensity_with_zoom = 0,
                        recovered_intensity_zoom_only= 1,
                        recovered_phase = 0,
                        recovered_phase_with_zoom = 0,
                        recovered_phase_zoom_only = 1,
                        recovered_pupil_amplitude = 0,
                        recovered_pupil_coefficients = 0,
                        recovered_pupil_overview = 0,
                        recovered_pupil_phase = 0,
                        recovered_spectrum = 0)
plot_parameters = Plot_parameters(format="pdf",
                                  zernike_coefficient_max=0.11,
                                  zernike_coefficient_min=-0.23,
                                  max_zernike_j = 25,
                                  low_res_intensity_zoom_location = Zoom_location.right,
                                  recovered_intensity_zoom_location = Zoom_location.right,
                                  recovered_phase_zoom_location = Zoom_location.right, 
                                  zoom_ratio = 6.67)

if __name__ == "__main__":
    main()
    
