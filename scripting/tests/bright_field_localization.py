from pyFPM.experimental.plot_illumination import plot_bright_field_images_with_BF_edge
from pyFPM.NTNU_specific.simulate_images.only_illumination import simulate_illumination
from pyFPM.NTNU_specific.setup_from_file import setup_parameters_from_file
from pyFPM.NTNU_specific.rawdata_from_files import get_rawdata_from_files
from pyFPM.NTNU_specific.components import (IDS_U3_31J0CP_REV_2_2, MAIN_LED_ARRAY, INFINITYCORRECTED_2X,
                                            HAMAMATSU_C11440_42U30, TELECENTRIC_3X, DOUBLE_CONVEX, COMPACT_2X)
from pyFPM.setup.Imaging_system import LED_calibration_parameters
from pyFPM.setup.Setup_parameters import Setup_parameters
from pyFPM.setup.Data import Data_patch, Rawdata, Preprocessed_data
from pyFPM.recovery.calibration.basic_BFL import basic_BFL
from pyFPM.recovery.calibration.non_linear_BFL import non_linear_BFL


import matplotlib.pyplot as plt
from pathlib import Path
import time

main_folder_1 = Path.cwd() / "data"/ "bright field localization" 
main_folder_2 = main_folder_1 / "defocus_illum"

def main():

    #infcor_2x_200_hamamatsu()
    #telecentric_3x_200_hamamatsu()
    #infcor_2x_205_mis_ueye3()
    #infcor_2x_200_ueye3()
    #infcor_2x_201_ueye3()
    #infcor_2x_202_ueye3()
    #infcor_2x_203_ueye3()
    #infcor_2x_204_ueye3()
    #infcor_2x_205_ueye3()
    #infcor_2x_206_ueye3()
    #infcor_2x_207_ueye3()
    #infcor_2x_208_ueye3()
    #infcor_2x_205_ueye3()
    locate_bright_field_from_simulation()
    compact_2x_205()

    plt.show()

def infcor_2x_200_hamamatsu():
    lens = INFINITYCORRECTED_2X
    datadirpath = main_folder_1 / "infinity_2x_illumnation"
    assumed_calibration_parameters = LED_calibration_parameters(200e-3,0e-6,0e-6,0)
    locate_bright_field_from_setup_hamamatsu(datadirpath=datadirpath, lens=lens, Fresnel=False, array_size=5, 
                                             assumed_calibration_parameters=assumed_calibration_parameters)
    
def telecentric_3x_200_hamamatsu():
    lens = TELECENTRIC_3X
    datadirpath = main_folder_1 / "telecentric_3x_illumination_2"
    assumed_calibration_parameters = LED_calibration_parameters(200e-3,0e-6,0e-6,0)
    locate_bright_field_from_setup_hamamatsu(datadirpath=datadirpath, lens=lens, Fresnel=False, array_size=7, 
                                             assumed_calibration_parameters=assumed_calibration_parameters)

def infcor_2x_200_ueye3():
    lens = INFINITYCORRECTED_2X
    datadirpath = main_folder_2 / "infcor2x_illum_200"
    assumed_calibration_parameters = LED_calibration_parameters(200e-3,0e-6,0e-6,0)
    locate_bright_field_from_setup(datadirpath=datadirpath, lens=lens, Fresnel=False, array_size=5, 
                                   assumed_calibration_parameters=assumed_calibration_parameters)
    
def infcor_2x_201_ueye3():
    lens = INFINITYCORRECTED_2X
    datadirpath = main_folder_2 / "infcor2x_illum_201"
    assumed_calibration_parameters = LED_calibration_parameters(200e-3,0e-6,0e-6,0)
    locate_bright_field_from_setup(datadirpath=datadirpath, lens=lens, Fresnel=False, array_size=5, 
                                   assumed_calibration_parameters=assumed_calibration_parameters)
    
def infcor_2x_202_ueye3():
    lens = INFINITYCORRECTED_2X
    datadirpath = main_folder_2 / "infcor2x_illum_202"
    assumed_calibration_parameters = LED_calibration_parameters(200e-3,0e-6,0e-6,0)
    locate_bright_field_from_setup(datadirpath=datadirpath, lens=lens, Fresnel=False, array_size=5, 
                                   assumed_calibration_parameters=assumed_calibration_parameters)
    
def infcor_2x_203_ueye3():
    lens = INFINITYCORRECTED_2X
    datadirpath = main_folder_2 / "infcor2x_illum_203"
    assumed_calibration_parameters = LED_calibration_parameters(200e-3,0e-6,0e-6,0)
    locate_bright_field_from_setup(datadirpath=datadirpath, lens=lens, Fresnel=False, array_size=5, 
                                   assumed_calibration_parameters=assumed_calibration_parameters)
    
def infcor_2x_204_ueye3():
    lens = INFINITYCORRECTED_2X
    datadirpath = main_folder_2 / "infcor2x_illum_204"
    assumed_calibration_parameters = LED_calibration_parameters(200e-3,0e-6,0e-6,0)
    locate_bright_field_from_setup(datadirpath=datadirpath, lens=lens, Fresnel=False, array_size=5, 
                                   assumed_calibration_parameters=assumed_calibration_parameters)
    
def infcor_2x_205_ueye3():
    lens = INFINITYCORRECTED_2X
    datadirpath = main_folder_2 / "infcor2x_illum_205"
    assumed_calibration_parameters = LED_calibration_parameters(200e-3,0e-6,0e-6,0)
    locate_bright_field_from_setup(datadirpath=datadirpath, lens=lens, Fresnel=False, array_size=5, 
                                   assumed_calibration_parameters=assumed_calibration_parameters)
    

def infcor_2x_206_ueye3():
    lens = INFINITYCORRECTED_2X
    datadirpath = main_folder_2 / "infcor2x_illum_206"
    assumed_calibration_parameters = LED_calibration_parameters(200e-3,0e-6,0e-6,0)
    locate_bright_field_from_setup(datadirpath=datadirpath, lens=lens, Fresnel=False, array_size=5, 
                                   assumed_calibration_parameters=assumed_calibration_parameters)
    

def infcor_2x_207_ueye3():
    lens = INFINITYCORRECTED_2X
    datadirpath = main_folder_2 / "infcor2x_illum_207"
    assumed_calibration_parameters = LED_calibration_parameters(200e-3,0e-6,0e-6,0)
    locate_bright_field_from_setup(datadirpath=datadirpath, lens=lens, Fresnel=False, array_size=5, 
                                   assumed_calibration_parameters=assumed_calibration_parameters)
    
def infcor_2x_208_ueye3():
    lens = INFINITYCORRECTED_2X
    datadirpath = main_folder_2 / "infcor2x_illum_208"
    assumed_calibration_parameters = LED_calibration_parameters(208e-3,0e-6,0e-6,0)
    locate_bright_field_from_setup(datadirpath=datadirpath, lens=lens, Fresnel=False, array_size=5, 
                                   assumed_calibration_parameters=assumed_calibration_parameters)
    

def infcor_2x_205_mis_ueye3():
    lens = INFINITYCORRECTED_2X
    datadirpath = main_folder_1 / "infcor2x_illum_205_misalign"
    assumed_calibration_parameters = LED_calibration_parameters(205e-3,0e-6,0e-6,0)
    locate_bright_field_from_setup(datadirpath=datadirpath, lens=lens, Fresnel=False, array_size=5, 
                                   assumed_calibration_parameters=assumed_calibration_parameters)
    
def compact_2x_200():
    lens = COMPACT_2X
    datadirpath = main_folder_2 / "compact2x_illum_200" 
    assumed_calibration_parameters = LED_calibration_parameters(200e-3,0e-6,0e-6,0)
    locate_bright_field_from_setup(datadirpath=datadirpath, lens=lens, Fresnel=True, array_size=5, 
                                   assumed_calibration_parameters=assumed_calibration_parameters)
    
def compact_2x_205():
    lens = COMPACT_2X
    datadirpath = main_folder_2 / "compact2x_illum_205" 
    assumed_calibration_parameters = LED_calibration_parameters(205e-3,0e-6,0e-6,0)
    locate_bright_field_from_setup(datadirpath=datadirpath, lens=lens, Fresnel=True, array_size=5, 
                                   assumed_calibration_parameters=assumed_calibration_parameters)
    
    

    

def locate_bright_field_from_simulation():
    lens = INFINITYCORRECTED_2X
    spherical = True
    Fresnel = False
    arraysize = 5
    simulation_parameters = LED_calibration_parameters(LED_distance = 201e-3,
                                                       LED_x_offset = 50e-6,
                                                       LED_y_offset = 50e-6,
                                                       LED_rotation = 0.3)
    
    assumed_parameters = LED_calibration_parameters(LED_distance = 200e-3,
                                                    LED_x_offset = 0e-6,
                                                    LED_y_offset = 0e-6,
                                                    LED_rotation = 0)

    start = time.perf_counter()
    setup_parameters, data_patch, imaging_system, illumination_pattern, applied_pupil, high_res_complex_object\
       = simulate_illumination(lens = lens, 
                               correct_spherical_wave_illumination = spherical, 
                               correct_Fresnel_propagation = Fresnel,
                               arraysize = arraysize,
                               calibration_parameters = simulation_parameters,
                               patch_offset = [0,0])
    end = time.perf_counter()
    print("Simulation:", end-start)
    
    start = time.perf_counter()
    calibration_parameters = non_linear_BFL(data = data_patch, setup_parameters = setup_parameters, 
                                            assumed_calibration_parameters=assumed_parameters)

    end = time.perf_counter()
    print("Bright field localization:", end-start)

    # fig = plot_bright_field_images_with_BF_edge(data_patch=data_patch, setup_parameters=setup_parameters, 
    #                                             calibration_parameters=calibration_parameters,
    #                                             array_size=arraysize, Fresnel=Fresnel)
    
    # fig = plot_bright_field_images_with_BF_edge(data_patch=data_patch, setup_parameters=setup_parameters, 
    #                                             calibration_parameters=simulation_parameters,
    #                                             array_size=arraysize, Fresnel=Fresnel)


def locate_bright_field_from_setup_hamamatsu(datadirpath, lens, Fresnel, array_size, assumed_calibration_parameters):
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
    
    start = time.perf_counter()
    calibration_parameters = non_linear_BFL(data = data_patch, setup_parameters = setup_parameters,
                                            assumed_calibration_parameters=assumed_calibration_parameters)
    end = time.perf_counter()
    print("Bright field localization:", end-start)


    # fig = plot_bright_field_images_with_BF_edge(data_patch=data_patch, setup_parameters=setup_parameters, 
    #                                             calibration_parameters=calibration_parameters, 
    #                                             array_size=array_size, Fresnel=Fresnel)
    
    # fig = plot_bright_field_images_with_BF_edge(data_patch=data_patch, setup_parameters=setup_parameters, 
    #                                     calibration_parameters=assumed_calibration_parameters, 
    #                                     array_size=array_size, Fresnel=Fresnel)



def locate_bright_field_from_setup(datadirpath, lens, Fresnel, array_size, assumed_calibration_parameters):
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

    start = time.perf_counter()
    calibration_parameters = non_linear_BFL(data = data_patch, setup_parameters = setup_parameters,
                                            assumed_calibration_parameters=assumed_calibration_parameters)
    end = time.perf_counter()
    print("Bright field localization:", end-start)

    # fig = plot_bright_field_images_with_BF_edge(data_patch=data_patch, setup_parameters=setup_parameters, 
    #                                             calibration_parameters=calibration_parameters, 
    #                                             array_size=array_size, Fresnel=Fresnel)
    
    # fig = plot_bright_field_images_with_BF_edge(data_patch=data_patch, setup_parameters=setup_parameters, 
    #                                         calibration_parameters=assumed_calibration_parameters, 
    #                                         array_size=array_size, Fresnel=Fresnel)


    
if __name__ == "__main__":
    main()
    
