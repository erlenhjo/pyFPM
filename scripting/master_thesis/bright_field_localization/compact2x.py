import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

from pyFPM.experimental.recover_experiment import recover_experiment, Experiment_settings
from pyFPM.experimental.pickle_results import plot_pickled_experiment
from pyFPM.experimental.plot_info import Plot_types, Plot_parameters, Zoom_location
from pyFPM.recovery.algorithms.run_algorithm import Method
from pyFPM.setup.Imaging_system import LED_calibration_parameters
from pyFPM.recovery.algorithms.Step_description import get_standard_adaptive_step_description
from pyFPM.NTNU_specific.components import COMPACT_2X_CALIBRATED, COMPACT_2X
from pyFPM.NTNU_specific.setup_IDS_U3 import setup_IDS_U3_global, setup_IDS_U3_local

patch_size = [512, 512]
max_array_size = 13

data_folder = Path.cwd() / "data"
main_result_folder = Path.cwd() / "results" / "master_thesis" / "BFL_recovery"

recover = True
plot = True

def main():
    # compact2x_usaf_uncalibrated()
    # compact2x_usaf_semicalibrated()
    # compact2x_usaf_calibrated()
    compact2x_usaf_calibrated_lens_only()

    if plot:
        plt.show()


def recover_and_plot(title, datadirpath, patch_offsets, result_folder, experiment_settings):
    if recover:
        recover_experiment(title, datadirpath, patch_offsets, patch_size, max_array_size, experiment_settings, 
                           setup_local=setup_IDS_U3_local, setup_global=setup_IDS_U3_global)
    if plot:
        plot_pickled_experiment(title, result_folder, plot_types, plot_parameters)


def compact2x_usaf_calibrated():
    patch_offsets = [np.array([-37,-72])]
    title = "Compact 2x usaf calibrated"
    datadirpath = data_folder / "Master_thesis" / "sapphire window" / "compact2x_usaf_200mm"
    recover_and_plot(title, datadirpath, patch_offsets, main_result_folder, experiment_settings=experiment_settings_calibrated)

def compact2x_usaf_semicalibrated():
    patch_offsets = [np.array([-37,-72])]
    title = "Compact 2x usaf semi calibrated"
    datadirpath = data_folder / "Master_thesis" / "sapphire window" / "compact2x_usaf_200mm"
    recover_and_plot(title, datadirpath, patch_offsets, main_result_folder, experiment_settings=experiment_settings_semicalibrated)

def compact2x_usaf_calibrated_lens_only():
    patch_offsets = [np.array([-37,-72])]
    title = "Compact 2x usaf calibrated lens only"
    datadirpath = data_folder / "Master_thesis" / "sapphire window" / "compact2x_usaf_200mm"
    recover_and_plot(title, datadirpath, patch_offsets, main_result_folder, experiment_settings=experiment_settings_calibrated_lens_only)


def compact2x_usaf_uncalibrated():
    patch_offsets = [np.array([-37,-72])]
    title = "Compact 2x usaf uncalibrated"
    datadirpath = data_folder / "Master_thesis" / "sapphire window" / "compact2x_usaf_200mm"
    recover_and_plot(title, datadirpath, patch_offsets, main_result_folder, experiment_settings=experiment_settings_uncalibrated)


experiment_settings_calibrated = Experiment_settings(lens = COMPACT_2X_CALIBRATED,
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
                                                        threshold_value = 1500,
                                                        noise_reduction_regions = [
                                                                                        [0, 0, 100, 100],
                                                                                        [1100, 1100, 100, 100]
                                                                                    ],
                                                        defocus_guess = 0,
                                                        limited_import = [1200,1200],
                                                        circular_LED_pattern = True
                                                        )

experiment_settings_semicalibrated = Experiment_settings(lens = COMPACT_2X,
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
                                                        threshold_value = 1500,
                                                        noise_reduction_regions = [
                                                                                        [0, 0, 100, 100],
                                                                                        [1100, 1100, 100, 100]
                                                                                    ],
                                                        defocus_guess = 0,
                                                        limited_import = [1200,1200],
                                                        circular_LED_pattern = True
                                                        )

experiment_settings_uncalibrated = Experiment_settings(lens = COMPACT_2X,
                                                        method = Method.Fresnel,
                                                        calibration_parameters = LED_calibration_parameters(LED_distance=0.200, 
                                                                                                            LED_x_offset=0, 
                                                                                                            LED_y_offset=0, 
                                                                                                            LED_rotation=0
                                                                                                            ),
                                                        step_description = get_standard_adaptive_step_description(max_iterations=50,
                                                                                                                    start_EPRY_at_iteration = 0,
                                                                                                                    start_adaptive_at_iteration = 10,
                                                                                                                    apply_BF_mask_from_iteration = 10),
                                                        pixel_scale_factor = 6,
                                                        binning_factor = 1, 
                                                        threshold_value = 1500,
                                                        noise_reduction_regions = [
                                                                                        [0, 0, 100, 100],
                                                                                        [1100, 1100, 100, 100]
                                                                                    ],
                                                        defocus_guess = 0,
                                                        limited_import = [1200,1200],
                                                        circular_LED_pattern = True
                                                        )

experiment_settings_calibrated_lens_only = Experiment_settings(lens = COMPACT_2X_CALIBRATED,
                                                        method = Method.Fresnel,
                                                        calibration_parameters = LED_calibration_parameters(LED_distance=0.200, 
                                                                                                            LED_x_offset=0, 
                                                                                                            LED_y_offset=0, 
                                                                                                            LED_rotation=0
                                                                                                            ),
                                                        step_description = get_standard_adaptive_step_description(max_iterations=50,
                                                                                                                    start_EPRY_at_iteration = 0,
                                                                                                                    start_adaptive_at_iteration = 10,
                                                                                                                    apply_BF_mask_from_iteration = 10),
                                                        pixel_scale_factor = 6,
                                                        binning_factor = 1, 
                                                        threshold_value = 1500,
                                                        noise_reduction_regions = [
                                                                                        [0, 0, 100, 100],
                                                                                        [1100, 1100, 100, 100]
                                                                                    ],
                                                        defocus_guess = 0,
                                                        limited_import = [1200,1200],
                                                        circular_LED_pattern = True
                                                        )


plot_types = Plot_types(overview = False, 
                        object_overview = False,
                        raw_image_with_zoom = False,
                        recovered_intensity_with_zoom = False,
                        recovered_intensity_zoom_only= True,
                        recovered_phase = False,
                        recovered_phase_with_zoom = False,
                        recovered_phase_zoom_only = False,
                        recovered_pupil_amplitude = False,
                        recovered_pupil_coefficients = False,
                        recovered_pupil_overview = False,
                        recovered_pupil_phase = False,
                        recovered_spectrum = False)
plot_parameters = Plot_parameters(format="pdf",
                                  zernike_coefficient_max=0.11,
                                  zernike_coefficient_min=-0.23,
                                  max_zernike_j = 25,
                                  low_res_intensity_zoom_location = Zoom_location.right,
                                  recovered_intensity_zoom_location = Zoom_location.right,
                                  recovered_phase_zoom_location = Zoom_location.right, 
                                  zoom_ratio = 10)

if __name__ == "__main__":
    main()
    
