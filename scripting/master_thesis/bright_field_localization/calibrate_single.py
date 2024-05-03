from pyFPM.NTNU_specific.components import (IDS_U3_31J0CP_REV_2_2, COMPACT_2X_CALIBRATED)
from pyFPM.setup.Imaging_system import LED_calibration_parameters

from pyFPM.NTNU_specific.calibrate_BF.BFL_single import calibrate_dataset
from pyFPM.NTNU_specific.calibrate_BF.BFL_step import NBFL_parameters

from pathlib import Path
import numpy as np


main_data_folder = Path.cwd() / "data"/ "bright field localization" 
main_result_folder = Path.cwd() / "results" / "master_thesis" / "BFL"

def main():
    single_step_comp_2x_usaf_window()
    single_step_comp_2x_usaf_corner()


algorithm_parameters = NBFL_parameters(
    binning_factor = 4,
    otsu_exponent = 2,
    canny_sigma = 10,
    image_boundary_filter_distance = 10,
    downsample_edges_factor = 10,
    limited_import = None
)


def single_step_comp_2x_usaf_window():
    lens = COMPACT_2X_CALIBRATED
    camera = IDS_U3_31J0CP_REV_2_2
    experiment_name = "2xcomp_single_usaf_window"
    dataset_name =  Path.cwd() / "data" / "Master_thesis" / "sapphire window" / "compact2x_usaf_200mm_illum"
    array_size = 5
    assumed_calibration_parameters = LED_calibration_parameters(200e-3,0e-6,0e-6,0)
    
    calibrate_dataset(dataset_name=dataset_name, experiment_name=experiment_name,
                        lens=lens, camera=camera, array_size=array_size,
                        assumed_calibration_parameters=assumed_calibration_parameters,
                        main_data_folder = main_data_folder,
                        main_result_folder = main_result_folder,
                        algorithm_parameters = algorithm_parameters)


def single_step_comp_2x_usaf_corner():
    lens = COMPACT_2X_CALIBRATED
    camera = IDS_U3_31J0CP_REV_2_2
    experiment_name = "2xcomp_single_usaf_corner"
    dataset_name =  Path.cwd() / "data" / "Master_thesis" / "calibration_test" / "comp2x_usaf_corner_illum"
    array_size = 5
    assumed_calibration_parameters = LED_calibration_parameters(200e-3,0e-6,0e-6,0)
    
    calibrate_dataset(dataset_name=dataset_name, experiment_name=experiment_name,
                        lens=lens, camera=camera, array_size=array_size,
                        assumed_calibration_parameters=assumed_calibration_parameters,
                        main_data_folder = main_data_folder,
                        main_result_folder = main_result_folder,
                        algorithm_parameters = algorithm_parameters)
    
    


    


    

if __name__ == "__main__":
    main()
    