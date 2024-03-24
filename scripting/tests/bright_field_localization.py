from pyFPM.NTNU_specific.components import (IDS_U3_31J0CP_REV_2_2, INFINITYCORRECTED_2X,
                                            HAMAMATSU_C11440_42U30, TELECENTRIC_3X, DOUBLE_CONVEX, COMPACT_2X)
from pyFPM.setup.Imaging_system import LED_calibration_parameters

from BFL_scripts_real import locate_bright_field_from_setup, locate_bright_field_from_setup_multi
from BFL_scripts_sim import locate_bright_field_from_simulation, test_BFL

import matplotlib.pyplot as plt
from pathlib import Path


main_folder_1 = Path.cwd() / "data"/ "bright field localization" 
main_folder_2 = main_folder_1 / "defocus_illum"

def main():
    #multi_infcor_2x()
    #infcor_2x_200_hamamatsu()
    #telecentric_3x_200_hamamatsu()
    #infcor_2x_205_mis_ueye3()
    #infcor_2x_200_ueye3()
    #infcor_2x_201_ueye3()
    infcor_2x_202_ueye3()
    #infcor_2x_203_ueye3()
    #infcor_2x_204_ueye3()
    #infcor_2x_205_ueye3()
    #infcor_2x_206_ueye3()
    #infcor_2x_207_ueye3()
    #infcor_2x_208_ueye3()
    #locate_bright_field_from_simulation()
    #test_BFL()
    #compact_2x_205()

    plt.show()

def infcor_2x_200_hamamatsu():
    lens = INFINITYCORRECTED_2X
    camera = HAMAMATSU_C11440_42U30
    datadirpath = main_folder_1 / "infinity_2x_illumnation"
    assumed_calibration_parameters = LED_calibration_parameters(200e-3,0e-6,0e-6,0)
    locate_bright_field_from_setup(datadirpath=datadirpath, lens=lens, camera=camera, array_size=5, 
                                             assumed_calibration_parameters=assumed_calibration_parameters)
    
def telecentric_3x_200_hamamatsu():
    lens = TELECENTRIC_3X
    camera = HAMAMATSU_C11440_42U30
    datadirpath = main_folder_1 / "telecentric_3x_illumination_2"
    assumed_calibration_parameters = LED_calibration_parameters(200e-3,0e-6,0e-6,0)
    locate_bright_field_from_setup(datadirpath=datadirpath, lens=lens, camera=camera, array_size=7, 
                                             assumed_calibration_parameters=assumed_calibration_parameters)

def infcor_2x_200_ueye3():
    lens = INFINITYCORRECTED_2X
    camera = IDS_U3_31J0CP_REV_2_2
    datadirpath = main_folder_2 / "infcor2x_illum_200"
    assumed_calibration_parameters = LED_calibration_parameters(200e-3,0e-6,0e-6,0)
    locate_bright_field_from_setup(datadirpath=datadirpath, lens=lens, camera=camera, array_size=5, 
                                   assumed_calibration_parameters=assumed_calibration_parameters)
    
def infcor_2x_201_ueye3():
    lens = INFINITYCORRECTED_2X
    camera = IDS_U3_31J0CP_REV_2_2
    datadirpath = main_folder_2 / "infcor2x_illum_201"
    assumed_calibration_parameters = LED_calibration_parameters(200e-3,0e-6,0e-6,0)
    locate_bright_field_from_setup(datadirpath=datadirpath, lens=lens, camera=camera, array_size=5, 
                                   assumed_calibration_parameters=assumed_calibration_parameters)
    
def infcor_2x_202_ueye3():
    lens = INFINITYCORRECTED_2X
    camera = IDS_U3_31J0CP_REV_2_2
    datadirpath = main_folder_2 / "infcor2x_illum_202"
    assumed_calibration_parameters = LED_calibration_parameters(200e-3,0e-6,0e-6,0)
    locate_bright_field_from_setup(datadirpath=datadirpath, lens=lens, camera=camera, array_size=5, 
                                   assumed_calibration_parameters=assumed_calibration_parameters)
    
def infcor_2x_203_ueye3():
    lens = INFINITYCORRECTED_2X
    camera = IDS_U3_31J0CP_REV_2_2
    datadirpath = main_folder_2 / "infcor2x_illum_203"
    assumed_calibration_parameters = LED_calibration_parameters(200e-3,0e-6,0e-6,0)
    locate_bright_field_from_setup(datadirpath=datadirpath, lens=lens, camera=camera, array_size=5, 
                                   assumed_calibration_parameters=assumed_calibration_parameters)
    
def infcor_2x_204_ueye3():
    lens = INFINITYCORRECTED_2X
    camera = IDS_U3_31J0CP_REV_2_2
    datadirpath = main_folder_2 / "infcor2x_illum_204"
    assumed_calibration_parameters = LED_calibration_parameters(200e-3,0e-6,0e-6,0)
    locate_bright_field_from_setup(datadirpath=datadirpath, lens=lens, camera=camera, array_size=5, 
                                   assumed_calibration_parameters=assumed_calibration_parameters)
    
def infcor_2x_205_ueye3():
    lens = INFINITYCORRECTED_2X
    camera = IDS_U3_31J0CP_REV_2_2
    datadirpath = main_folder_2 / "infcor2x_illum_205"
    assumed_calibration_parameters = LED_calibration_parameters(200e-3,0e-6,0e-6,0)
    locate_bright_field_from_setup(datadirpath=datadirpath, lens=lens, camera=camera, array_size=5, 
                                   assumed_calibration_parameters=assumed_calibration_parameters)
    

def infcor_2x_206_ueye3():
    lens = INFINITYCORRECTED_2X
    camera = IDS_U3_31J0CP_REV_2_2
    datadirpath = main_folder_2 / "infcor2x_illum_206"
    assumed_calibration_parameters = LED_calibration_parameters(200e-3,0e-6,0e-6,0)
    locate_bright_field_from_setup(datadirpath=datadirpath, lens=lens, camera=camera, array_size=5, 
                                   assumed_calibration_parameters=assumed_calibration_parameters)
    

def infcor_2x_207_ueye3():
    lens = INFINITYCORRECTED_2X
    camera = IDS_U3_31J0CP_REV_2_2
    datadirpath = main_folder_2 / "infcor2x_illum_207"
    assumed_calibration_parameters = LED_calibration_parameters(200e-3,0e-6,0e-6,0)
    locate_bright_field_from_setup(datadirpath=datadirpath, lens=lens, camera=camera, array_size=5, 
                                   assumed_calibration_parameters=assumed_calibration_parameters)
    
def infcor_2x_208_ueye3():
    lens = INFINITYCORRECTED_2X
    camera = IDS_U3_31J0CP_REV_2_2
    datadirpath = main_folder_2 / "infcor2x_illum_208"
    assumed_calibration_parameters = LED_calibration_parameters(208e-3,0e-6,0e-6,0)
    locate_bright_field_from_setup(datadirpath=datadirpath, lens=lens, camera=camera, array_size=5, 
                                   assumed_calibration_parameters=assumed_calibration_parameters)
    

def infcor_2x_205_mis_ueye3():
    lens = INFINITYCORRECTED_2X
    camera = IDS_U3_31J0CP_REV_2_2
    datadirpath = main_folder_1 / "infcor2x_illum_205_misalign"
    assumed_calibration_parameters = LED_calibration_parameters(205e-3,0e-6,0e-6,0)
    locate_bright_field_from_setup(datadirpath=datadirpath, lens=lens, camera=camera, array_size=5, 
                                   assumed_calibration_parameters=assumed_calibration_parameters)
    
def compact_2x_200():
    lens = COMPACT_2X
    camera = IDS_U3_31J0CP_REV_2_2
    datadirpath = main_folder_2 / "compact2x_illum_200" 
    assumed_calibration_parameters = LED_calibration_parameters(200e-3,0e-6,0e-6,0)
    locate_bright_field_from_setup(datadirpath=datadirpath, lens=lens, camera=camera, array_size=5, 
                                   assumed_calibration_parameters=assumed_calibration_parameters)
    
def compact_2x_205():
    lens = COMPACT_2X
    camera = IDS_U3_31J0CP_REV_2_2
    datadirpath = main_folder_2 / "compact2x_illum_205" 
    assumed_calibration_parameters = LED_calibration_parameters(205e-3,0e-6,0e-6,0)
    locate_bright_field_from_setup(datadirpath=datadirpath, lens=lens, camera=camera, array_size=5, 
                                   assumed_calibration_parameters=assumed_calibration_parameters)
    
def multi_infcor_2x():
    lens = INFINITYCORRECTED_2X
    camera = IDS_U3_31J0CP_REV_2_2
    datadirpaths = [
        main_folder_2 / "infcor2x_illum_200",
        main_folder_2 / "infcor2x_illum_204",
        main_folder_2 / "infcor2x_illum_208",
        main_folder_2 / "infcor2x_illum_212"
    ]
    relative_LED_distances = [0, 4e-3, 8e-3, 12e-3]

    assumed_calibration_parameters = LED_calibration_parameters(200e-3,0e-6,0e-6,0)
    locate_bright_field_from_setup_multi(datadirpaths=datadirpaths, 
                                         relative_LED_distances=relative_LED_distances, 
                                         lens=lens, camera=camera, array_size=5, 
                                         assumed_calibration_parameters=assumed_calibration_parameters)
    
    

    
if __name__ == "__main__":
    main()
    
