from pyFPM.NTNU_specific.components import (IDS_U3_31J0CP_REV_2_2, COMPACT_2X_CALIBRATED)
from pyFPM.setup.Imaging_system import LED_calibration_parameters

from BFL_single import locate_bright_field_from_setup_single_step

from pathlib import Path
import numpy as np


main_data_folder = Path.cwd() / "data"/ "bright field localization" 
main_result_folder = Path.cwd() / "results"
BFL_result_folder = main_result_folder / "BFL"


def main():
    single_step_comp_2x_usaf_test()
    #single_step_comp_2x_phasetarget_test()


def single_step_comp_2x_usaf_test():
    lens = COMPACT_2X_CALIBRATED
    camera = IDS_U3_31J0CP_REV_2_2
    experiment_name = "2xcomp_single_usaf"
    dataset_name =  Path.cwd() / "data" / "Master_thesis" / "calibration_test" / "com2x_usaf_calib_test_175_illum"
    array_size = 5
    assumed_calibration_parameters = LED_calibration_parameters(175e-3,0e-6,0e-6,0)
    
    calibrate_dataset(dataset_name=dataset_name, experiment_name=experiment_name,
                        lens=lens, camera=camera, array_size=array_size,
                        assumed_calibration_parameters=assumed_calibration_parameters)
    
def single_step_comp_2x_phasetarget_test():
    lens = COMPACT_2X_CALIBRATED
    camera = IDS_U3_31J0CP_REV_2_2
    experiment_name = "2xcomp_single_phasetarget"
    dataset_name =  Path.cwd() / "data" / "Master_thesis" / "calibration_test" / "com2x_phasefocus_calib_test_175_illum"
    array_size = 5
    assumed_calibration_parameters = LED_calibration_parameters(175e-3,0e-6,0e-6,0)
    
    calibrate_dataset(dataset_name=dataset_name, experiment_name=experiment_name,
                        lens=lens, camera=camera, array_size=array_size,
                        assumed_calibration_parameters=assumed_calibration_parameters)


    
        
    

def get_folders(dataset_name, experiment_name):
    data_folder = main_data_folder / "BFL calibration" / dataset_name
    result_folder = BFL_result_folder / experiment_name
    result_folder.mkdir(parents=True, exist_ok=True)

    return data_folder, result_folder


def calibrate_dataset(dataset_name, experiment_name,
                      lens, camera, array_size, 
                      assumed_calibration_parameters):
    
    data_folder, result_folder = get_folders(dataset_name = dataset_name,
                                             experiment_name = experiment_name)

    locate_bright_field_from_setup_single_step(data_folder=data_folder, 
                                                lens=lens, camera=camera, 
                                                array_size=array_size, 
                                                assumed_calibration_parameters=assumed_calibration_parameters,
                                                raw_result_folder=result_folder
                                                )
    


    

if __name__ == "__main__":
    main()
    