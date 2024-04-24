from pyFPM.NTNU_specific.components import (IDS_U3_31J0CP_REV_2_2, INFINITYCORRECTED_2X,
                                            HAMAMATSU_C11440_42U30, TELECENTRIC_3X, DOUBLE_CONVEX, COMPACT_2X)
from pyFPM.setup.Imaging_system import LED_calibration_parameters

from BFL_scripts_real import locate_bright_field_from_setup
from BFL_scripts_sim import locate_bright_field_from_simulation, test_BFL
from BFL_step import locate_bright_field_from_setup_step

import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np


main_data_folder = Path.cwd() / "data"/ "bright field localization" 
main_result_folder = Path.cwd() / "results" / "BFL"


def main():
    #infcor_2x_200_hamamatsu()
    #telecentric_3x_200_hamamatsu()
    step_comp_2x()
    #step_inf_2x()
    #step_tele_3x()


def infcor_2x_200_hamamatsu():
    lens = INFINITYCORRECTED_2X
    camera = HAMAMATSU_C11440_42U30
    datadirpath = main_data_folder / "infinity_2x_illumnation"
    assumed_calibration_parameters = LED_calibration_parameters(200e-3,0e-6,0e-6,0)
    locate_bright_field_from_setup(datadirpath=datadirpath, lens=lens, camera=camera, array_size=5, 
                                             assumed_calibration_parameters=assumed_calibration_parameters)
    
def telecentric_3x_200_hamamatsu():
    lens = TELECENTRIC_3X
    camera = HAMAMATSU_C11440_42U30
    datadirpath = main_data_folder / "telecentric_3x_illumination_2"
    assumed_calibration_parameters = LED_calibration_parameters(200e-3,0e-6,0e-6,0)
    locate_bright_field_from_setup(datadirpath=datadirpath, lens=lens, camera=camera, array_size=7, 
                                             assumed_calibration_parameters=assumed_calibration_parameters)

def step_comp_2x():
    lens = COMPACT_2X
    camera = IDS_U3_31J0CP_REV_2_2
    experiment_name = "2xcomp_illum_step_5"
    dataset_names = [
        "2xcomp_illum_step_150_p4",
        "2xcomp_illum_step_175_p4",
        "2xcomp_illum_step_200_p4"
    ]
    array_sizes = [5,5,7]
    relative_LED_distances = np.arange(11) * 4e-3
    result_suffix = "png"
    assumed_calibration_parameters = LED_calibration_parameters(200e-3,0e-6,0e-6,0)

    data_folders = [main_data_folder / "BFL step" / dataset_name for dataset_name in dataset_names]
    result_folder = main_result_folder / experiment_name
    result_folder.mkdir(parents=True, exist_ok=True)
    result_subfolders = [result_folder / dataset_name for dataset_name in dataset_names]
    for folder in result_subfolders:
        folder.mkdir(parents=True, exist_ok=True)

    locate_bright_field_from_setup_step(data_folders=data_folders, 
                                        relative_LED_distances=relative_LED_distances, 
                                        lens=lens, camera=camera, array_sizes=array_sizes, 
                                        assumed_calibration_parameters=assumed_calibration_parameters,
                                        result_folder = result_folder, 
                                        result_subfolders = result_subfolders, 
                                        result_suffix = result_suffix)
    
def step_tele_3x():
    lens = TELECENTRIC_3X
    camera = IDS_U3_31J0CP_REV_2_2
    experiment_name = "3xtele_illum_step"
    dataset_names = [
        "3xtele_illum_step_150_p4",
        "3xtele_illum_step_175_p4",
        "3xtele_illum_step_200_p4"
    ]
    array_sizes = [7,7,7]
    relative_LED_distances = np.arange(11) * 4e-3
    result_suffix = "png"
    assumed_calibration_parameters = LED_calibration_parameters(200e-3,0e-6,0e-6,0)

    data_folders = [main_data_folder / "BFL step" / dataset_name for dataset_name in dataset_names]
    result_folder = main_result_folder / experiment_name
    result_folder.mkdir(parents=True, exist_ok=True)
    result_subfolders = [result_folder / dataset_name for dataset_name in dataset_names]
    for folder in result_subfolders:
        folder.mkdir(parents=True, exist_ok=True)

    locate_bright_field_from_setup_step(data_folders=data_folders, 
                                        relative_LED_distances=relative_LED_distances, 
                                        lens=lens, camera=camera, array_sizes=array_sizes, 
                                        assumed_calibration_parameters=assumed_calibration_parameters,
                                        result_folder = result_folder, 
                                        result_subfolders = result_subfolders, 
                                        result_suffix = result_suffix)
    

def step_inf_2x():
    lens = INFINITYCORRECTED_2X
    camera = IDS_U3_31J0CP_REV_2_2
    experiment_name = "2xinf_illum_step"
    dataset_names = [
        "2xinf_illum_step_150_p4",
        "2xinf_illum_step_175_p4",
        "2xinf_illum_step_200_p4"
    ]
    array_sizes = [5,5,5]
    relative_LED_distances = np.arange(11) * 4e-3
    result_suffix = "png"
    assumed_calibration_parameters = LED_calibration_parameters(200e-3,0e-6,0e-6,0)

    data_folders = [main_data_folder / "BFL step" / dataset_name for dataset_name in dataset_names]
    result_folder = main_result_folder / experiment_name
    result_folder.mkdir(parents=True, exist_ok=True)
    result_subfolders = [result_folder / dataset_name for dataset_name in dataset_names]
    for folder in result_subfolders:
        folder.mkdir(parents=True, exist_ok=True)

    locate_bright_field_from_setup_step(data_folders=data_folders, 
                                        relative_LED_distances=relative_LED_distances, 
                                        lens=lens, camera=camera, array_sizes=array_sizes, 
                                        assumed_calibration_parameters=assumed_calibration_parameters,
                                        result_folder = result_folder, 
                                        result_subfolders = result_subfolders, 
                                        result_suffix = result_suffix)
    

if __name__ == "__main__":
    main()
    
