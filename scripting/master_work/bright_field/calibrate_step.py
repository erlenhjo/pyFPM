from pyFPM.NTNU_specific.components import (IDS_U3_31J0CP_REV_2_2, INFINITYCORRECTED_2X,
                                            TELECENTRIC_3X, COMPACT_2X, FUJINON_MINWD_MAXNA)
from pyFPM.setup.Imaging_system import LED_calibration_parameters

from pyFPM.NTNU_specific.calibrate_BF.BFL_step import calibrate_datasets, plot_experiment_results


from pathlib import Path
import numpy as np
from typing import List


#main_data_folder = Path.cwd() / "data" / "bright field localization" / "BFL step"
main_data_folder = Path("E:") / "BFL step"
main_result_folder = Path.cwd() / "results" / "BFL"



def main():
    calibrate=False
    plot=True


    #multi_step_comp_2x(calibrate=calibrate, plot=plot)
    #multi_step_comp_2x_old(calibrate=calibrate, plot=plot)
    multi_step_tele_3x(calibrate=calibrate, plot=plot)
    #multi_step_inf_2x_not_converging(calibrate=calibrate, plot=plot)
    multi_step_tele_3x_not_converging(calibrate=calibrate, plot=plot)


def multi_step_comp_2x(calibrate, plot):
    lens = COMPACT_2X
    camera = IDS_U3_31J0CP_REV_2_2
    experiment_name = "2xcomp_illum_step_2mm"
    dataset_names = [
        "2xcomp_illum_step_60_p2",
        "2xcomp_illum_step_85_p2",
        "2xcomp_illum_step_110_p2",
        "2xcomp_illum_step_135_p2",
        "2xcomp_illum_step_160_p2",
        "2xcomp_illum_step_185_p2"
    ]
    array_sizes = [3,5,5,5,7,7]
    number_of_steps = 26
    relative_LED_distances = np.arange(number_of_steps) * 2e-3
    assumed_calibration_parameters = LED_calibration_parameters(60e-3,0,0,0)
    
    if calibrate:
        calibrate_datasets(dataset_names=dataset_names, experiment_name=experiment_name,
                           number_of_steps=number_of_steps,
                           lens=lens, camera=camera, array_sizes=array_sizes,
                           assumed_calibration_parameters=assumed_calibration_parameters,
                           main_data_folder = main_data_folder,
                           main_result_folder = main_result_folder)
    if plot:
        plot_experiment_results(dataset_names=dataset_names,
                                experiment_name=experiment_name,
                                relative_LED_distances=relative_LED_distances,
                                main_data_folder = main_data_folder,
                                main_result_folder = main_result_folder)
                

def multi_step_tele_3x(calibrate, plot):
    lens = TELECENTRIC_3X
    camera = IDS_U3_31J0CP_REV_2_2
    experiment_name = "3xtele_illum_step_2mm"
    dataset_names = [
        "3xtele_illum_step_135_p2",
        "3xtele_illum_step_185_p2"
    ]
    array_sizes = [5,7]
    number_of_steps = 26
    relative_LED_distances = np.arange(number_of_steps) * 2e-3
    assumed_calibration_parameters = LED_calibration_parameters(135e-3,0,0,0)
    
    if calibrate:
        calibrate_datasets(dataset_names=dataset_names, experiment_name=experiment_name,
                           number_of_steps=number_of_steps,
                           lens=lens, camera=camera, array_sizes=array_sizes,
                           assumed_calibration_parameters=assumed_calibration_parameters,
                           main_data_folder = main_data_folder,
                           main_result_folder = main_result_folder)
    if plot:
        plot_experiment_results(dataset_names=dataset_names,
                                experiment_name=experiment_name,
                                relative_LED_distances=relative_LED_distances,
                                main_data_folder = main_data_folder,
                                main_result_folder = main_result_folder)


def multi_step_comp_2x_old(calibrate, plot):
    lens = COMPACT_2X
    camera = IDS_U3_31J0CP_REV_2_2
    experiment_name = "2xcomp_illum_step"
    dataset_names = [
        "2xcomp_illum_step_150_p4",
        "2xcomp_illum_step_175_p4",
        "2xcomp_illum_step_200_p4"
    ]
    array_sizes = [5,5,7]
    number_of_steps = 11
    relative_LED_distances = np.arange(number_of_steps) * 4e-3
    assumed_calibration_parameters = LED_calibration_parameters(200e-3,0,0,0)
    
    if calibrate:
        calibrate_datasets(dataset_names=dataset_names, experiment_name=experiment_name,
                           number_of_steps=number_of_steps,
                           lens=lens, camera=camera, array_sizes=array_sizes,
                           assumed_calibration_parameters=assumed_calibration_parameters,
                           main_data_folder = main_data_folder,
                           main_result_folder = main_result_folder)
    if plot:
        plot_experiment_results(dataset_names=dataset_names,
                                experiment_name=experiment_name,
                                relative_LED_distances=relative_LED_distances,
                                main_data_folder = main_data_folder,
                                main_result_folder = main_result_folder)
    
def multi_step_tele_3x_not_converging(calibrate, plot):
    lens = TELECENTRIC_3X
    camera = IDS_U3_31J0CP_REV_2_2
    experiment_name = "3xtele_illum_step_not_converging"
    dataset_names = [
        "3xtele_illum_step_150_p4",
        "3xtele_illum_step_175_p4",
        "3xtele_illum_step_200_p4"
    ]
    array_sizes = [7,7,7]
    number_of_steps = 11
    relative_LED_distances = np.arange(number_of_steps) * 4e-3
    assumed_calibration_parameters = LED_calibration_parameters(200e-3,0,0,0)

    if calibrate:
        calibrate_datasets(dataset_names=dataset_names, experiment_name=experiment_name,
                           number_of_steps=number_of_steps,
                           lens=lens, camera=camera, array_sizes=array_sizes,
                           assumed_calibration_parameters=assumed_calibration_parameters,
                           main_data_folder = main_data_folder,
                           main_result_folder = main_result_folder)
    if plot:
        plot_experiment_results(dataset_names=dataset_names,
                                experiment_name=experiment_name,
                                relative_LED_distances=relative_LED_distances,
                                main_data_folder = main_data_folder,
                                main_result_folder = main_result_folder)
    

def multi_step_inf_2x_not_converging(calibrate, plot):
    lens = INFINITYCORRECTED_2X
    camera = IDS_U3_31J0CP_REV_2_2
    experiment_name = "2xinf_illum_step_not_converging"
    dataset_names = [
        "2xinf_illum_step_150_p4",
        "2xinf_illum_step_175_p4",
        "2xinf_illum_step_200_p4"
    ]
    array_sizes = [5,5,5]
    number_of_steps = 11
    relative_LED_distances = np.arange(number_of_steps) * 4e-3
    assumed_calibration_parameters = LED_calibration_parameters(200e-3,0,0,0)

    if calibrate:
        calibrate_datasets(dataset_names=dataset_names, experiment_name=experiment_name,
                           number_of_steps=number_of_steps,
                           lens=lens, camera=camera, array_sizes=array_sizes,
                           assumed_calibration_parameters=assumed_calibration_parameters,
                                main_data_folder = main_data_folder,
                                main_result_folder = main_result_folder)
    if plot:
        plot_experiment_results(dataset_names=dataset_names,
                                experiment_name=experiment_name,
                                relative_LED_distances=relative_LED_distances,
                                main_data_folder = main_data_folder,
                                main_result_folder = main_result_folder)


        
    
    

if __name__ == "__main__":
    main()
    
