from pyFPM.NTNU_specific.setup_from_file import setup_parameters_from_file
from pyFPM.NTNU_specific.rawdata_from_files import get_rawdata_from_files
from pyFPM.NTNU_specific.components import MAIN_LED_ARRAY
from pyFPM.setup.Setup_parameters import Setup_parameters
from pyFPM.setup.Imaging_system import LED_calibration_parameters
from pyFPM.setup.Data import Rawdata
from pyFPM.calibration.non_linear_BFL.multi_step import non_linear_BFL_multi_step
from pyFPM.calibration.non_linear_BFL.shared import Calibration_parameters

import time
from typing import List
from pathlib import Path
import pickle
from scipy.optimize import OptimizeResult



def get_pickle_path(raw_result_folder: Path, filename):
    pickle_path: Path = raw_result_folder / filename
    return pickle_path.with_suffix(".obj")

def pickle_calibration_results_per_step(calibration_results_per_step: List[Calibration_parameters], 
                                       raw_result_folder: Path):
    pickle_path = get_pickle_path(raw_result_folder, filename="calibration_results_per_step")
    with open(pickle_path, "wb") as file:
        pickle.dump(calibration_results_per_step, file)

def unpickle_calibration_results_per_step(raw_result_folder) -> List[Calibration_parameters]:
    pickle_path = get_pickle_path(raw_result_folder, filename="calibration_results_per_step")
    with open(pickle_path, "rb") as file:
        calibration_results_per_step: List[Calibration_parameters] = pickle.load(file)
    return calibration_results_per_step

def pickle_optimization_results_per_step(optimization_results_per_step: List[OptimizeResult], 
                                       raw_result_folder: Path):
    pickle_path = get_pickle_path(raw_result_folder, filename="optimization_results_per_step")
    with open(pickle_path, "wb") as file:
        pickle.dump(optimization_results_per_step, file)

def unpickle_optimization_results_per_step(raw_result_folder) -> List[OptimizeResult]:
    pickle_path = get_pickle_path(raw_result_folder, filename="optimization_results_per_step")
    with open(pickle_path, "rb") as file:
        optimization_results_per_step: List[Calibration_parameters] = pickle.load(file)
    return optimization_results_per_step
    


def locate_bright_field_from_setup_multi_step(data_folder, number_of_steps, 
                                        lens, camera, array_size, 
                                        assumed_calibration_parameters: LED_calibration_parameters,
                                        raw_result_folder, NA_only = False):
    LED_array = MAIN_LED_ARRAY 
    binning_factor = 4
    otsu_exponent = 2 # 1/2 means that the otsu threshold is based on amplitude, 1 on intensity, 2 on intesity^2
    canny_sigma = 10
    image_boundary_filter_distance = canny_sigma
    downsample_edges_factor = 10

    start = time.perf_counter()
    setup_parameters: Setup_parameters = setup_parameters_from_file(
        datadirpath = data_folder,
        lens = lens,
        camera = camera,
        LED_array = LED_array,
        binning_factor = binning_factor
        )
    end = time.perf_counter()
    print("Setup parameters:", end-start)


    numerical_aperture = setup_parameters.lens.NA
    effective_object_to_aperture_distance = setup_parameters.lens.effective_object_to_aperture_distance

    assumed_calibration_parameters = \
        Calibration_parameters(
            delta_x = assumed_calibration_parameters.LED_x_offset,
            delta_y = assumed_calibration_parameters.LED_y_offset,
            rotation = assumed_calibration_parameters.LED_rotation,
            numerical_aperture_times_LED_distance = numerical_aperture*assumed_calibration_parameters.LED_distance,
            distance_ratio = assumed_calibration_parameters.LED_distance/effective_object_to_aperture_distance
        )

    calibration_results_per_step: List[Calibration_parameters] = [] 
    optimization_results_per_step: List[OptimizeResult] = []

    for step_nr in range(number_of_steps):
        start = time.perf_counter()
        rawdata: Rawdata = get_rawdata_from_files(
            datadirpath = data_folder,
            image_format = setup_parameters.image_format,
            center_indices = setup_parameters.LED_info.center_indices,
            max_array_size = array_size,
            float_type = setup_parameters.camera.float_type,
            binning_factor = binning_factor,
            desired_step_nr = step_nr 
            )
        end = time.perf_counter()
        print("Rawdata:", end-start)

        start = time.perf_counter()
        calibration_results, optimization_results = non_linear_BFL_multi_step(data = rawdata, setup_parameters = setup_parameters,
                                                    assumed_calibration_parameters = assumed_calibration_parameters,
                                                    result_folder = raw_result_folder, step_nr = step_nr,
                                                    otsu_exponent = otsu_exponent, canny_sigma = canny_sigma,
                                                    image_boundary_filter_distance = image_boundary_filter_distance,
                                                    downsample_edges_factor = downsample_edges_factor,
                                                    binning_factor = binning_factor, NA_only = NA_only)
        calibration_results_per_step.append(calibration_results)
        optimization_results_per_step.append(optimization_results)
        end = time.perf_counter()
        print("Bright field localization:", end-start)

        assumed_calibration_parameters = calibration_results

    pickle_calibration_results_per_step(calibration_results_per_step = calibration_results_per_step,      
                                        raw_result_folder = raw_result_folder)
    pickle_optimization_results_per_step(optimization_results_per_step = optimization_results_per_step,      
                                        raw_result_folder = raw_result_folder)



