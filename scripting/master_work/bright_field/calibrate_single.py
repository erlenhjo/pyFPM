from pyFPM.NTNU_specific.components import (IDS_U3_31J0CP_REV_2_2, COMPACT_2X_CALIBRATED)
from pyFPM.setup.Imaging_system import LED_calibration_parameters

from pyFPM.NTNU_specific.calibrate_BF.BFL_single import calibrate_dataset

from pathlib import Path
import numpy as np


main_data_folder = Path.cwd() / "data"/ "bright field localization" 
main_result_folder = Path.cwd() / "results"
BFL_result_folder = main_result_folder / "BFL"


def main():
    #single_step_comp_2x_usaf_test()
    #single_step_comp_2x_phasetarget_test()
    single_step_comp_2x_usaf_window()

def single_step_comp_2x_usaf_test():
    lens = COMPACT_2X_CALIBRATED
    camera = IDS_U3_31J0CP_REV_2_2
    experiment_name = "2xcomp_single_usaf"
    dataset_name =  Path.cwd() / "data" / "Master_thesis" / "calibration_test" / "com2x_usaf_calib_test_175_illum"
    array_size = 5
    assumed_calibration_parameters = LED_calibration_parameters(175e-3,0e-6,0e-6,0)
    
    calibrate_dataset(dataset_name=dataset_name, experiment_name=experiment_name,
                        lens=lens, camera=camera, array_size=array_size,
                        assumed_calibration_parameters=assumed_calibration_parameters,
                        main_data_folder = main_data_folder,
                        main_result_folder = main_result_folder)
    
def single_step_comp_2x_phasetarget_test():
    lens = COMPACT_2X_CALIBRATED
    camera = IDS_U3_31J0CP_REV_2_2
    experiment_name = "2xcomp_single_phasetarget"
    dataset_name =  Path.cwd() / "data" / "Master_thesis" / "calibration_test" / "com2x_phasefocus_calib_test_175_illum"
    array_size = 5
    assumed_calibration_parameters = LED_calibration_parameters(175e-3,0e-6,0e-6,0)
    
    calibrate_dataset(dataset_name=dataset_name, experiment_name=experiment_name,
                        lens=lens, camera=camera, array_size=array_size,
                        assumed_calibration_parameters=assumed_calibration_parameters,
                        main_data_folder = main_data_folder,
                        main_result_folder = main_result_folder)


def single_step_comp_2x_usaf_window():
    lens = COMPACT_2X_CALIBRATED
    camera = IDS_U3_31J0CP_REV_2_2
    experiment_name = "2xcomp_single_usaf_window"
    dataset_name =  Path.cwd() / "data" / "Master_thesis" / "saphire window" / "compact2x_usaf_200mm_illum"
    array_size = 5
    assumed_calibration_parameters = LED_calibration_parameters(200e-3,0e-6,0e-6,0)
    
    calibrate_dataset(dataset_name=dataset_name, experiment_name=experiment_name,
                        lens=lens, camera=camera, array_size=array_size,
                        assumed_calibration_parameters=assumed_calibration_parameters,
                        main_data_folder = main_data_folder,
                        main_result_folder = main_result_folder)

    
        
    


    


    

if __name__ == "__main__":
    main()
    