from pyFPM.NTNU_specific.setup_from_file import setup_parameters_from_file
from pyFPM.NTNU_specific.rawdata_from_files import get_rawdata_from_files
from pyFPM.NTNU_specific.components import MAIN_LED_ARRAY
from pyFPM.setup.Setup_parameters import Setup_parameters
from pyFPM.setup.Data import Data_patch, Rawdata, Preprocessed_data
from pyFPM.recovery.calibration.parallell_non_linear_BFL import parallell_non_linear_BFL
from pyFPM.recovery.calibration.series_non_linear_BFL import series_non_linear_BFL
from pyFPM.recovery.calibration.non_linear_BFL import non_linear_BFL

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
        max_array_size = array_size
        )
    end = time.perf_counter()
    print("Rawdata:", end-start)

    start = time.perf_counter()
    preprocessed_data = Preprocessed_data(
        rawdata = rawdata,
        setup_parameters = setup_parameters,
        noise_reduction_regions = None, 
        threshold_value = False
        )
    end = time.perf_counter()
    print("Preprocessed data:", end-start)
    
    start = time.perf_counter()
    data_patch = Data_patch(
        data = preprocessed_data,
        raw_image_size = setup_parameters.camera.raw_image_size,
        patch_offset = [0,0],
        patch_size = setup_parameters.camera.raw_image_size
        )
    end = time.perf_counter()
    print("Data patch:", end-start)

    start = time.perf_counter()
    calibration_parameters = non_linear_BFL(data = data_patch, setup_parameters = setup_parameters,
                                            assumed_calibration_parameters=assumed_calibration_parameters)
    end = time.perf_counter()
    print("Bright field localization:", end-start)

def locate_bright_field_from_setup_parallell(datadirpaths, relative_LED_distances, 
                                         lens, camera, array_size, assumed_calibration_parameters):
    LED_array = MAIN_LED_ARRAY 

    start = time.perf_counter()
    setup_parameters: Setup_parameters = setup_parameters_from_file(
        datadirpath = datadirpaths[0],
        lens = lens,
        camera = camera,
        LED_array = LED_array
        )
    end = time.perf_counter()
    print("Setup parameters:", end-start)

    data_patches = []
    for datadirpath in datadirpaths:
        start = time.perf_counter()
        rawdata: Rawdata = get_rawdata_from_files(
            datadirpath = datadirpath,
            image_format = setup_parameters.image_format,
            center_indices = setup_parameters.LED_info.center_indices,
            max_array_size = array_size
            )
        end = time.perf_counter()
        print("Rawdata:", end-start)

        start = time.perf_counter()
        preprocessed_data = Preprocessed_data(
            rawdata = rawdata,
            setup_parameters = setup_parameters,
            noise_reduction_regions = None, 
            threshold_value = False
            )
        end = time.perf_counter()
        print("Preprocessed data:", end-start)
        
        start = time.perf_counter()
        data_patch = Data_patch(
            data = preprocessed_data,
            raw_image_size = setup_parameters.camera.raw_image_size,
            patch_offset = [0,0],
            patch_size = setup_parameters.camera.raw_image_size
            )
        end = time.perf_counter()
        print("Data patch:", end-start)

        data_patches.append(data_patch)

    start = time.perf_counter()
    calibration_parameters = parallell_non_linear_BFL(data_patches = data_patches, setup_parameters = setup_parameters,
                                                  assumed_calibration_parameters = assumed_calibration_parameters,
                                                  relative_LED_distances = relative_LED_distances)
    end = time.perf_counter()
    print("Bright field localization:", end-start)



def locate_bright_field_from_setup_series(datadirpaths, relative_LED_distances, 
                                         lens, camera, array_size, assumed_calibration_parameters):
    LED_array = MAIN_LED_ARRAY 

    start = time.perf_counter()
    setup_parameters: Setup_parameters = setup_parameters_from_file(
        datadirpath = datadirpaths[0],
        lens = lens,
        camera = camera,
        LED_array = LED_array
        )
    end = time.perf_counter()
    print("Setup parameters:", end-start)

    data_patches = []
    for datadirpath in datadirpaths:
        start = time.perf_counter()
        rawdata: Rawdata = get_rawdata_from_files(
            datadirpath = datadirpath,
            image_format = setup_parameters.image_format,
            center_indices = setup_parameters.LED_info.center_indices,
            max_array_size = array_size
            )
        end = time.perf_counter()
        print("Rawdata:", end-start)

        start = time.perf_counter()
        preprocessed_data = Preprocessed_data(
            rawdata = rawdata,
            setup_parameters = setup_parameters,
            noise_reduction_regions = None, 
            threshold_value = False
            )
        end = time.perf_counter()
        print("Preprocessed data:", end-start)
        
        start = time.perf_counter()
        data_patch = Data_patch(
            data = preprocessed_data,
            raw_image_size = setup_parameters.camera.raw_image_size,
            patch_offset = [0,0],
            patch_size = setup_parameters.camera.raw_image_size
            )
        end = time.perf_counter()
        print("Data patch:", end-start)

        data_patches.append(data_patch)

    start = time.perf_counter()
    calibration_parameters = series_non_linear_BFL(data_patches = data_patches, setup_parameters = setup_parameters,
                                                   assumed_calibration_parameters = assumed_calibration_parameters,
                                                   relative_LED_distances = relative_LED_distances)
    end = time.perf_counter()
    print("Bright field localization:", end-start)