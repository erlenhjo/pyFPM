from pyFPM.experimental.plot_illumination import plot_bright_field_images_with_BF_edge
from pyFPM.NTNU_specific.simulate_images.only_illumination import simulate_illumination
from pyFPM.NTNU_specific.setup_from_file import setup_parameters_from_file
from pyFPM.NTNU_specific.rawdata_from_files import get_rawdata_from_files
from pyFPM.NTNU_specific.components import IDS_U3_31J0CP_REV_2_2, MAIN_LED_ARRAY, INFINITYCORRECTED_2X, HAMAMATSU_C11440_42U30
from pyFPM.setup.Imaging_system import LED_calibration_parameters
from pyFPM.setup.Setup_parameters import Setup_parameters
from pyFPM.setup.Data import Data_patch, Rawdata, Preprocessed_data
from pyFPM.recovery.calibration.bright_field_localization import bright_field_localization

import matplotlib.pyplot as plt
from pathlib import Path
import time

main_folder = Path.cwd() / "data"/ "bright field localization" 

def main():

    infcor_2x_200_hamamatsu()
    #infcor_2x_200_misaligned()
    #infcor_2x_205_misaligned()
    #infcor_2x_210_misaligned()

    plt.show()

def infcor_2x_200_hamamatsu():
    lens = INFINITYCORRECTED_2X
    datadirpath = main_folder / "infinity_2x_illumnation"
    calibration_parameters = LED_calibration_parameters(200e-3,0e-6,0e-6,0)
    locate_bright_field_from_setup_hamamatsu(datadirpath=datadirpath, lens=lens, Fresnel=False,
                                             array_size=5, calibration_parameters=calibration_parameters)

    
def infcor_2x_200_misaligned():
    lens = INFINITYCORRECTED_2X
    datadirpath = main_folder / "infcor2x_illum_200_misalign"
    calibration_parameters = LED_calibration_parameters(200e-3,0e-6,0e-6,0)
    locate_bright_field_from_setup(datadirpath=datadirpath, lens=lens, Fresnel=False,
                                   array_size=5, calibration_parameters=calibration_parameters)
    
def infcor_2x_205_misaligned():
    lens = INFINITYCORRECTED_2X
    datadirpath = main_folder / "infcor2x_illum_205_misalign"
    calibration_parameters = LED_calibration_parameters(205e-3,0e-6,0e-6,0)
    locate_bright_field_from_setup(datadirpath=datadirpath, lens=lens, Fresnel=False,
                                   array_size=5, calibration_parameters=calibration_parameters)
    
def infcor_2x_210_misaligned():
    lens = INFINITYCORRECTED_2X
    datadirpath = main_folder / "infcor2x_illum_210_misalign"
    calibration_parameters = LED_calibration_parameters(210e-3,0e-6,0e-6,0)
    locate_bright_field_from_setup(datadirpath=datadirpath, lens=lens, Fresnel=False,
                                   array_size=5, calibration_parameters=calibration_parameters)
    

def locate_bright_field_from_setup_hamamatsu(datadirpath, lens, Fresnel, array_size, calibration_parameters):
    patch_offset = [0, 0] # [x, y]
    patch_size = [2048, 2048] # [x, y]

    camera = HAMAMATSU_C11440_42U30
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
        patch_offset = patch_offset,
        patch_size = patch_size
        )
    end = time.perf_counter()
    print("Data patch:", end-start)
    
    calibration_parameters = bright_field_localization(data=data_patch, setup_parameters=setup_parameters)

    # fig = plot_bright_field_images_with_BF_edge(data_patch=data_patch, setup_parameters=setup_parameters, 
    #                                             calibration_parameters=calibration_parameters, 
    #                                             array_size=array_size, Fresnel=Fresnel)
    # return fig


def locate_bright_field_from_setup(datadirpath, lens, Fresnel, array_size, calibration_parameters):
    patch_offset = [0, 0] # [x, y]
    patch_size = [2800, 2800] # [x, y]

    camera = IDS_U3_31J0CP_REV_2_2
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
        patch_offset = patch_offset,
        patch_size = patch_size
        )
    end = time.perf_counter()
    print("Data patch:", end-start)

    calibration_parameters = bright_field_localization(data=data_patch, setup_parameters=setup_parameters)

    # fig = plot_bright_field_images_with_BF_edge(data_patch=data_patch, setup_parameters=setup_parameters, 
    #                                             calibration_parameters=calibration_parameters, 
    #                                             array_size=array_size, Fresnel=Fresnel)
    # return fig

    
if __name__ == "__main__":
    main()
    
