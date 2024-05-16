from pyFPM.NTNU_specific.components import (IDS_U3_31J0CP_REV_2_2, COMPACT_2X_CALIBRATED, COMPACT_2X, MAIN_LED_ARRAY)
from pyFPM.setup.Imaging_system import LED_calibration_parameters, Imaging_system
from pyFPM.NTNU_specific.rawdata_from_files import get_rawdata_from_files
from pyFPM.NTNU_specific.setup_from_file import setup_parameters_from_file

from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

calibration_parameters = LED_calibration_parameters(LED_distance=0.20153892853221111, LED_x_offset=-0.00012446193565815314, 
                                                    LED_y_offset=-0.00012741088856773426, LED_rotation=-0.0010187545121927496)
dummy_dataset = Path.cwd() / "data" / "Master_thesis" / "sapphire window" / "compact2x_usaf_200mm_illum"
result_folder = main_result_folder = Path.cwd() / "results" / "master_thesis" / "BFL_recovery"


def main():
    Q_illum, Q_fresnel_uncalibrated = get_quadratic_phases(COMPACT_2X)
    _, Q_fresnel_calibrated = get_quadratic_phases(COMPACT_2X_CALIBRATED)
    fig_calib, axes_calib = plt.subplots(1,1, figsize=(3,3))
    fig_uncalib, axes_uncalib = plt.subplots(1,1, figsize=(3,3))
    fig_diff, axes_diff = plt.subplots(1,1, figsize=(3,3))

    axes_uncalib.matshow(np.angle(Q_fresnel_uncalibrated*Q_illum), vmin=-np.pi, vmax=np.pi)
    axes_calib.matshow(np.angle(Q_fresnel_calibrated*Q_illum), vmin=-np.pi, vmax=np.pi)
    axes_diff.matshow(np.angle(Q_fresnel_uncalibrated/Q_fresnel_calibrated), vmin=-np.pi, vmax=np.pi)
    axes_uncalib.set_axis_off()
    axes_calib.set_axis_off()
    axes_diff.set_axis_off()
    
    fig_calib.savefig(result_folder / "quadratic_phase_calibrated.pdf", 
                       format = "pdf", 
                       bbox_inches="tight")
    fig_uncalib.savefig(result_folder / "quadratic_phase_uncalibrated.pdf", 
                       format = "pdf", 
                       bbox_inches="tight")
    fig_diff.savefig(result_folder / "quadratic_phase_difference.pdf", 
                       format = "pdf", 
                       bbox_inches="tight")

def get_quadratic_phases(lens):
    LED_array = MAIN_LED_ARRAY 

    setup_parameters = setup_parameters_from_file(
        datadirpath = dummy_dataset,
        lens = lens,
        camera = IDS_U3_31J0CP_REV_2_2,
        LED_array = LED_array,
        binning_factor = 1
        )

    imaging_system = Imaging_system(setup_parameters = setup_parameters,
                                    pixel_scale_factor = 6,
                                    patch_offset = [0, 0],
                                    patch_size = [512,512],
                                    calibration_parameters = calibration_parameters,
                                    binned_image_size = [512, 512])
    
    return imaging_system.high_res_spherical_illumination_correction, imaging_system.high_res_Fresnel_correction


if __name__ == "__main__":
    main()