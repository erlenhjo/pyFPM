from pyFPM.NTNU_specific.setup_from_file import setup_parameters_from_file
from pyFPM.NTNU_specific.rawdata_from_files import get_rawdata_from_files
from pyFPM.NTNU_specific.components import MAIN_LED_ARRAY
from pyFPM.setup.Setup_parameters import Setup_parameters
from pyFPM.setup.Data import Data_patch, Rawdata, Preprocessed_data
from pyFPM.calibration.non_linear_BFL.single_step import non_linear_BFL_single_step

import time

def locate_bright_field_from_setup(datadirpath, lens, camera, array_size, assumed_calibration_parameters):
    LED_array = MAIN_LED_ARRAY 

    start = time.perf_counter()
    setup_parameters: Setup_parameters = setup_parameters_from_file(
        datadirpath = datadirpath,
        lens = lens,
        camera = camera,
        LED_array = LED_array
        )
    end = time.perf_counter()
    print("Setup parameters:", end-start)

    start = time.perf_counter()
    rawdata: Rawdata = get_rawdata_from_files(
        datadirpath = datadirpath,
        image_format = setup_parameters.image_format,
        center_indices = setup_parameters.LED_info.center_indices,
        max_array_size = array_size,
        float_type = setup_parameters.camera.float_type
        )
    end = time.perf_counter()
    print("Rawdata:", end-start)


    start = time.perf_counter()
    calibration_parameters = non_linear_BFL_single_step(data = rawdata, setup_parameters = setup_parameters,
                                            assumed_calibration_parameters=assumed_calibration_parameters)
    end = time.perf_counter()
    print("Bright field localization:", end-start)
