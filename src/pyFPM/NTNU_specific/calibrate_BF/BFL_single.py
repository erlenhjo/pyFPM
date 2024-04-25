from pyFPM.NTNU_specific.setup_from_file import setup_parameters_from_file
from pyFPM.NTNU_specific.rawdata_from_files import get_rawdata_from_files
from pyFPM.NTNU_specific.components import MAIN_LED_ARRAY
from pyFPM.setup.Setup_parameters import Setup_parameters
from pyFPM.setup.Data import Data_patch, Rawdata, Preprocessed_data
from pyFPM.calibration.non_linear_BFL.single_step import non_linear_BFL_single_step

import time

def locate_bright_field_from_setup_single_step(data_folder, lens, camera, array_size, 
                                               assumed_calibration_parameters, raw_result_folder):
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

    start = time.perf_counter()
    rawdata: Rawdata = get_rawdata_from_files(
        datadirpath = data_folder,
        image_format = setup_parameters.image_format,
        center_indices = setup_parameters.LED_info.center_indices,
        max_array_size = array_size,
        float_type = setup_parameters.camera.float_type,
        binning_factor = binning_factor
        )
    end = time.perf_counter()
    print("Rawdata:", end-start)

    start = time.perf_counter()
    calibration_parameters = non_linear_BFL_single_step(data = rawdata, setup_parameters = setup_parameters,
                                                        assumed_calibration_parameters=assumed_calibration_parameters,
                                                        result_folder = raw_result_folder,
                                                        otsu_exponent = otsu_exponent, 
                                                        canny_sigma = canny_sigma,
                                                        image_boundary_filter_distance = image_boundary_filter_distance,
                                                        downsample_edges_factor = downsample_edges_factor,
                                                        binning_factor = binning_factor)
    end = time.perf_counter()
    print("Bright field localization:", end-start)

    print(calibration_parameters)

