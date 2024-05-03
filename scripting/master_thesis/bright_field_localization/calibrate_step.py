from pyFPM.NTNU_specific.components import (IDS_U3_31J0CP_REV_2_2, COMPACT_2X,
                                            TELECENTRIC_3X, INFINITYCORRECTED_10X)
from pyFPM.setup.Imaging_system import LED_calibration_parameters

from pyFPM.NTNU_specific.calibrate_BF.BFL_step import calibrate_datasets, plot_experiment_results, NBFL_parameters


from pathlib import Path
import numpy as np
from typing import List


main_data_folder = Path("E:") / "BFL step"
main_result_folder = Path.cwd() / "results" / "master_thesis" / "BFL"

def main():
    calibrate=True
    plot=True

    #multi_step_comp_2x(calibrate=calibrate, plot=plot)
    multi_step_inf_10x(calibrate=calibrate, plot=plot)
    multi_step_tele_3x(calibrate=calibrate, plot=plot)
    #multi_step_comp_2x_corner(calibrate=calibrate, plot=plot)

algorithm_parameters = NBFL_parameters(
    binning_factor = 4,
    otsu_exponent = 2,
    canny_sigma = 10,
    image_boundary_filter_distance = 10,
    downsample_edges_factor = 10,
    limited_import = None
)

    

def multi_step_comp_2x(calibrate, plot):
    lens = COMPACT_2X
    camera = IDS_U3_31J0CP_REV_2_2
    experiment_name = "2xcomp_illum_step_2mm"
    dataset_names = [
        "2xcomp_illum_step_85_p2",
        "2xcomp_illum_step_110_p2",
        "2xcomp_illum_step_135_p2",
        "2xcomp_illum_step_160_p2",
        "2xcomp_illum_step_185_p2"
    ]
    array_sizes = [5,5,5,7,7]
    number_of_steps = 26
    relative_LED_distances = np.arange(number_of_steps) * 2e-3
    assumed_calibration_parameters = LED_calibration_parameters(85e-3,0,0,0)
    
    if calibrate:
        calibrate_datasets(dataset_names=dataset_names, experiment_name=experiment_name,
                           number_of_steps=number_of_steps,
                           lens=lens, camera=camera, array_sizes=array_sizes,
                           assumed_calibration_parameters=assumed_calibration_parameters,
                           main_data_folder = main_data_folder,
                           main_result_folder = main_result_folder,
                           algorithm_parameters = algorithm_parameters)
    if plot:
        plot_experiment_results(dataset_names=dataset_names,
                                experiment_name=experiment_name,
                                relative_LED_distances=relative_LED_distances,
                                main_data_folder = main_data_folder,
                                main_result_folder = main_result_folder)
                
def multi_step_tele_3x(calibrate, plot):
    lens = TELECENTRIC_3X
    camera = IDS_U3_31J0CP_REV_2_2
    experiment_name = "3xtele_illum_step_2mm_240"
    dataset_names = [
        "tele3x_illum_step_240_p2"
    ]
    array_sizes = [9]
    number_of_steps = 26
    relative_LED_distances = np.arange(number_of_steps) * 2e-3
    assumed_calibration_parameters = LED_calibration_parameters(240e-3,0,0,0)
    
    if calibrate:
        calibrate_datasets(dataset_names=dataset_names, experiment_name=experiment_name,
                           number_of_steps=number_of_steps,
                           lens=lens, camera=camera, array_sizes=array_sizes,
                           assumed_calibration_parameters=assumed_calibration_parameters,
                           main_data_folder = main_data_folder,
                           main_result_folder = main_result_folder,
                           algorithm_parameters = algorithm_parameters)
    if plot:
        plot_experiment_results(dataset_names=dataset_names,
                                experiment_name=experiment_name,
                                relative_LED_distances=relative_LED_distances,
                                main_data_folder = main_data_folder,
                                main_result_folder = main_result_folder)
                
def multi_step_inf_10x(calibrate, plot):
    lens = INFINITYCORRECTED_10X
    camera = IDS_U3_31J0CP_REV_2_2
    experiment_name = "10xinf_illum_step_2mm"
    dataset_names = [
        "inf10x_illum_step_40_p2"
    ]
    array_sizes = [7]
    number_of_steps = 14
    relative_LED_distances = np.arange(number_of_steps) * 2e-3
    assumed_calibration_parameters = LED_calibration_parameters(40e-3,0,0,0)
    
    if calibrate:
        calibrate_datasets(dataset_names=dataset_names, experiment_name=experiment_name,
                           number_of_steps=number_of_steps,
                           lens=lens, camera=camera, array_sizes=array_sizes,
                           assumed_calibration_parameters=assumed_calibration_parameters,
                           main_data_folder = main_data_folder,
                           main_result_folder = main_result_folder,
                           algorithm_parameters = algorithm_parameters)
    if plot:
        plot_experiment_results(dataset_names=dataset_names,
                                experiment_name=experiment_name,
                                relative_LED_distances=relative_LED_distances,
                                main_data_folder = main_data_folder,
                                main_result_folder = main_result_folder)

def multi_step_comp_2x_corner(calibrate, plot):
    lens = COMPACT_2X
    camera = IDS_U3_31J0CP_REV_2_2
    experiment_name = "2xcomp_illum_step_corner"
    dataset_names = [
        "comp2x_usaf_corner_illum_step"
    ]
    array_sizes = [7]
    number_of_steps = 6
    relative_LED_distances = np.arange(number_of_steps) * 5e-3
    assumed_calibration_parameters = LED_calibration_parameters(85e-3,0,0,0)
    
    if calibrate:
        calibrate_datasets(dataset_names=dataset_names, experiment_name=experiment_name,
                           number_of_steps=number_of_steps,
                           lens=lens, camera=camera, array_sizes=array_sizes,
                           assumed_calibration_parameters=assumed_calibration_parameters,
                           main_data_folder = main_data_folder,
                           main_result_folder = main_result_folder,
                           algorithm_parameters = algorithm_parameters)
    if plot:
        plot_experiment_results(dataset_names=dataset_names,
                                experiment_name=experiment_name,
                                relative_LED_distances=relative_LED_distances,
                                main_data_folder = main_data_folder,
                                main_result_folder = main_result_folder)


        
    
    

if __name__ == "__main__":
    main()
    
