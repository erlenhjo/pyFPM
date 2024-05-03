from pyFPM.NTNU_specific.components import (IDS_U3_31J0CP_REV_2_2, FUJINON_MINWD_MAXNA)
from pyFPM.setup.Imaging_system import LED_calibration_parameters

from pyFPM.NTNU_specific.calibrate_BF.BFL_single import calibrate_dataset
from pyFPM.NTNU_specific.calibrate_BF.BFL_step import NBFL_parameters

from pathlib import Path
import numpy as np


main_data_folder = Path.cwd() / "data"/ "bright field localization" 
main_result_folder = Path.cwd() / "results" / "master_thesis" /  "BFL"

def main():
    single_step_fujinon_usaf_far()

algorithm_parameters = NBFL_parameters(
    binning_factor = 1,
    otsu_exponent = 0.5,
    canny_sigma = 10,
    image_boundary_filter_distance = 10,
    downsample_edges_factor = 10,
    limited_import = [1400,1400]
)


def single_step_fujinon_usaf():
    lens = FUJINON_MINWD_MAXNA
    camera = IDS_U3_31J0CP_REV_2_2
    experiment_name = "fujinon_single_usaf_7"
    dataset_name =  Path.cwd() / "data" / "Master_thesis" / "fujinon" / "fujinon_usaf_illum_320"
    array_size = 7
    assumed_calibration_parameters = LED_calibration_parameters(320e-3, 0, 0, 0)
    
    calibrate_dataset(dataset_name=dataset_name, experiment_name=experiment_name,
                        lens=lens, camera=camera, array_size=array_size,
                        assumed_calibration_parameters=assumed_calibration_parameters,
                        main_data_folder = main_data_folder,
                        main_result_folder = main_result_folder,
                        algorithm_parameters = algorithm_parameters)

    
        
def single_step_fujinon_usaf_far():
    lens = FUJINON_MINWD_MAXNA
    camera = IDS_U3_31J0CP_REV_2_2
    experiment_name = "fujinon_single_usaf_7_far"
    dataset_name =  Path.cwd() / "data" / "Master_thesis" / "fujinon" / "fujinon_usaf_1,8_far_illum"
    array_size = 7
    assumed_calibration_parameters = LED_calibration_parameters(400e-3, 0, 0, 0)
    
    calibrate_dataset(dataset_name=dataset_name, experiment_name=experiment_name,
                        lens=lens, camera=camera, array_size=array_size,
                        assumed_calibration_parameters=assumed_calibration_parameters,
                        main_data_folder = main_data_folder,
                        main_result_folder = main_result_folder,
                        algorithm_parameters = algorithm_parameters)


    


    

if __name__ == "__main__":
    main()
    