from pyFPM.NTNU_specific.setup_from_file import setup_parameters_from_file
from pyFPM.NTNU_specific.rawdata_from_files import get_rawdata_from_files
from pyFPM.NTNU_specific.components import MAIN_LED_ARRAY
from pyFPM.setup.Setup_parameters import Setup_parameters
from pyFPM.setup.Data import Rawdata
from pyFPM.recovery.calibration.advanced_non_linear_BFL import advanced_non_linear_BFL, Calibration_parameters_advanced

import time
from typing import List
import numpy as np
from scipy.stats import linregress
import matplotlib.pyplot as plt

def locate_bright_field_from_setup_step(data_folders, relative_LED_distances, 
                                         lens, camera, array_sizes, 
                                         assumed_calibration_parameters,
                                         result_folder, result_subfolders, result_suffix):
    LED_array = MAIN_LED_ARRAY 

    optimal_calibration_parameters_per_step_per_dataset = []

    for data_folder, result_subfolder, array_size in zip(data_folders, result_subfolders, array_sizes):
        start = time.perf_counter()
        setup_parameters: Setup_parameters = setup_parameters_from_file(
            datadirpath = data_folder,
            lens = lens,
            camera = camera,
            LED_array = LED_array
            )
        end = time.perf_counter()
        print("Setup parameters:", end-start)

        optimal_calibration_parameters_per_step: List[Calibration_parameters_advanced] = []

        for step_nr in range(len(relative_LED_distances)):
            start = time.perf_counter()
            rawdata: Rawdata = get_rawdata_from_files(
                datadirpath = data_folder,
                image_format = setup_parameters.image_format,
                center_indices = setup_parameters.LED_info.center_indices,
                max_array_size = array_size,
                float_type = setup_parameters.camera.float_type,
                desired_step_nr = step_nr 
                )
            end = time.perf_counter()
            print("Rawdata:", end-start)

            start = time.perf_counter()
            calibration_parameters = advanced_non_linear_BFL(data = rawdata, setup_parameters = setup_parameters,
                                                        assumed_calibration_parameters = assumed_calibration_parameters,
                                                        result_folder = result_subfolder, result_suffix = result_suffix,
                                                        step_nr = step_nr)
            optimal_calibration_parameters_per_step.append(calibration_parameters)
            end = time.perf_counter()
            print("Bright field localization:", end-start)

        optimal_calibration_parameters_per_step_per_dataset.append(optimal_calibration_parameters_per_step)


    delta_x_vals_per_dataset = []
    delta_y_vals_per_dataset = []
    rotation_vals_per_dataset = []
    NA_times_z_0_vals_per_dataset = []
    distance_ratio_vals_per_dataset = []
    relative_LED_distances = np.array(relative_LED_distances)


    for parameters_per_step in optimal_calibration_parameters_per_step_per_dataset:
        delta_x_vals = []
        delta_y_vals = []
        rotation_vals = []
        NA_times_z_0_vals = []
        distance_ratio_vals = []

        for parameters in parameters_per_step:
            delta_x_vals.append(parameters.delta_x)
            delta_y_vals.append(parameters.delta_y)
            rotation_vals.append(parameters.rotation * 180/np.pi)
            NA_times_z_0_vals.append(parameters.numerical_aperture_times_LED_distance)
            distance_ratio_vals.append(parameters.distance_ratio)

        delta_x_vals_per_dataset.append(delta_x_vals)
        delta_y_vals_per_dataset.append(delta_y_vals)
        rotation_vals_per_dataset.append(rotation_vals)
        NA_times_z_0_vals_per_dataset.append(NA_times_z_0_vals)
        distance_ratio_vals_per_dataset.append(distance_ratio_vals)


    fig, axes = plt.subplots(1,1)
    fig.suptitle("Delta x")
    for delta_x_vals in delta_x_vals_per_dataset:
        axes.scatter(relative_LED_distances, delta_x_vals)
    plot_path = result_folder / f"delta_x"
    fig.savefig(plot_path.with_suffix(f".{result_suffix}"), format = result_suffix)

    fig, axes = plt.subplots(1,1)
    fig.suptitle("Delta y")
    for delta_y_vals in delta_y_vals_per_dataset:
        axes.scatter(relative_LED_distances, delta_y_vals)
    plot_path = result_folder / f"delta_y"
    fig.savefig(plot_path.with_suffix(f".{result_suffix}"), format = result_suffix)

    fig, axes = plt.subplots(1,1)
    fig.suptitle("Rotation")
    for rotation_vals in rotation_vals_per_dataset:
        axes.scatter(relative_LED_distances, rotation_vals)
    plot_path = result_folder / f"rotation"
    fig.savefig(plot_path.with_suffix(f".{result_suffix}"), format = result_suffix)



    fig, axes = plt.subplots(1,1)
    fig.suptitle("NA * z_0")
    for NA_times_z_0_vals in NA_times_z_0_vals_per_dataset:
        result = linregress(relative_LED_distances, NA_times_z_0_vals)
        axes.scatter(relative_LED_distances, NA_times_z_0_vals)
        axes.plot(relative_LED_distances, result.slope*relative_LED_distances + result.intercept, 
                label = f"{result.slope:.3f} x + {result.slope:.3f}*{result.intercept/result.slope:.3f}")
    axes.legend()
    plot_path = result_folder / f"NA_times_z_0"
    fig.savefig(plot_path.with_suffix(f".{result_suffix}"), format = result_suffix)

    fig, axes = plt.subplots(1,1)
    fig.suptitle("z_0 / z_q")
    for distance_ratio_vals in distance_ratio_vals_per_dataset:
        result = linregress(relative_LED_distances, distance_ratio_vals)
        axes.scatter(relative_LED_distances, distance_ratio_vals)
        axes.plot(relative_LED_distances, result.slope*relative_LED_distances + result.intercept, 
                label = f"{result.slope:.3f} x + {result.slope:.3f}*{result.intercept/result.slope:.3f}")
    axes.legend()
    plot_path = result_folder / f"distance_ratio"
    fig.savefig(plot_path.with_suffix(f".{result_suffix}"), format = result_suffix)

    # plt.show()
    plt.close("all")