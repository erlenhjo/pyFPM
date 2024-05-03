from pyFPM.NTNU_specific.setup_from_file import setup_parameters_from_file
from pyFPM.NTNU_specific.rawdata_from_files import get_rawdata_from_files
from pyFPM.NTNU_specific.components import MAIN_LED_ARRAY
from pyFPM.setup.Setup_parameters import Setup_parameters
from pyFPM.setup.Data import Rawdata
from pyFPM.calibration.non_linear_BFL.single_step import non_linear_BFL_single_step
from pyFPM.NTNU_specific.calibrate_BF.BFL_step import NBFL_parameters

import time


def get_folders(dataset_name, experiment_name, main_data_folder, main_result_folder):
    data_folder = main_data_folder / dataset_name
    result_folder = main_result_folder / experiment_name
    result_folder.mkdir(parents=True, exist_ok=True)

    return data_folder, result_folder


def calibrate_dataset(dataset_name, experiment_name,
                      lens, camera, array_size, 
                      assumed_calibration_parameters,
                      main_data_folder, main_result_folder,
                      algorithm_parameters: NBFL_parameters):
    
    data_folder, result_folder = get_folders(dataset_name = dataset_name,
                                             experiment_name = experiment_name,
                                             main_data_folder = main_data_folder,
                                             main_result_folder = main_result_folder)

    locate_bright_field_from_setup_single_step(data_folder=data_folder, 
                                                lens=lens, camera=camera, 
                                                array_size=array_size, 
                                                assumed_calibration_parameters=assumed_calibration_parameters,
                                                raw_result_folder=result_folder,
                                                algorithm_parameters = algorithm_parameters
                                                )

def locate_bright_field_from_setup_single_step(data_folder, lens, camera, array_size, 
                                               assumed_calibration_parameters, raw_result_folder,
                                               algorithm_parameters: NBFL_parameters):
    LED_array = MAIN_LED_ARRAY 

    start = time.perf_counter()
    setup_parameters: Setup_parameters = setup_parameters_from_file(
        datadirpath = data_folder,
        lens = lens,
        camera = camera,
        LED_array = LED_array,
        binning_factor = algorithm_parameters.binning_factor
        )
    end = time.perf_counter()
    print("Setup parameters:", end-start)

    start = time.perf_counter()
    rawdata: Rawdata = get_rawdata_from_files(
        datadirpath = data_folder,
        image_format = setup_parameters.image_format,
        center_indices = setup_parameters.LED_info.center_indices,
        max_array_size = array_size,
        float_type = setup_parameters.camera.float_type,
        binning_factor = algorithm_parameters.binning_factor
        )
    end = time.perf_counter()
    print("Rawdata:", end-start)

    start = time.perf_counter()
    calibration_parameters = non_linear_BFL_single_step(data = rawdata, setup_parameters = setup_parameters,
                                                        assumed_calibration_parameters=assumed_calibration_parameters,
                                                        result_folder = raw_result_folder,
                                                        otsu_exponent = algorithm_parameters.otsu_exponent, 
                                                        canny_sigma = algorithm_parameters.canny_sigma,
                                                        image_boundary_filter_distance = algorithm_parameters.image_boundary_filter_distance,
                                                        downsample_edges_factor = algorithm_parameters.downsample_edges_factor,
                                                        binning_factor = algorithm_parameters.binning_factor)
    end = time.perf_counter()
    print("Bright field localization:", end-start)

    print(calibration_parameters)

