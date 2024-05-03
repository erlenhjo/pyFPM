from pyFPM.NTNU_specific.components import (IDS_U3_31J0CP_REV_2_2, FUJINON_MINWD_MAXNA)
from pyFPM.setup.Imaging_system import LED_calibration_parameters
from pyFPM.NTNU_specific.calibrate_BF.BFL_step import calibrate_datasets, plot_experiment_results, NBFL_parameters

from pathlib import Path
import numpy as np
from typing import List


#main_data_folder = Path.cwd() / "data" / "bright field localization" / "BFL step"
main_data_folder = Path("E:") / "BFL step"
main_result_folder = Path.cwd() / "results" / "master_thesis" / "BFL"


def main():
    calibrate=False
    plot=True

    multi_step_fujinon(calibrate=calibrate, plot=plot)

algorithm_parameters = NBFL_parameters(
    binning_factor = 1,
    otsu_exponent = 0.5,
    canny_sigma = 10,
    image_boundary_filter_distance = 10,
    downsample_edges_factor = 10,
    limited_import = [1400,1400]
)

        
def multi_step_fujinon(calibrate, plot):
    lens = FUJINON_MINWD_MAXNA
    camera = IDS_U3_31J0CP_REV_2_2
    experiment_name = "fujinon_illum_step_2mm"
    dataset_names = [
        "fujinon_illum_step_320_p2"
    ]
    array_sizes = [9]
    number_of_steps = 26
    relative_LED_distances = np.arange(number_of_steps) * 2e-3
    assumed_calibration_parameters = LED_calibration_parameters(320e-3,0,0,0)
    
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
    
