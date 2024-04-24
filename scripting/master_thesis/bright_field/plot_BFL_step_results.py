
from pyFPM.calibration.non_linear_BFL.shared import Calibration_parameters

from BFL_step import unpickle_calibration_results_per_step, unpickle_optimization_results_per_step

from typing import List
import numpy as np
from scipy.stats import linregress
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.optimize import OptimizeResult


def plot_BFL_step_experiments(raw_result_folders: List[Path],
                              result_folder: Path,
                              relative_LED_distances):

    calibration_results_per_step_per_experiment: List[List[Calibration_parameters]] = []
    optimization_results_per_step_per_experiment: List[List[OptimizeResult]] = []

    for raw_result_folder in raw_result_folders:
        calibration_results_per_step_per_experiment.append(
            unpickle_calibration_results_per_step(raw_result_folder = raw_result_folder)
        )
        optimization_results_per_step_per_experiment.append(
            unpickle_optimization_results_per_step(raw_result_folder = raw_result_folder)
        )

    delta_x_vals_per_dataset = []
    delta_y_vals_per_dataset = []
    rotation_vals_per_dataset = []
    NA_times_z_0_vals_per_dataset = []
    distance_ratio_vals_per_dataset = []
    optimization_score_vals_per_dataset = []
    relative_LED_distances = np.array(relative_LED_distances)
    
    for calibration_results_per_step, optimization_results_per_step \
        in zip(calibration_results_per_step_per_experiment, optimization_results_per_step_per_experiment):
        delta_x_vals = []
        delta_y_vals = []
        rotation_vals = []
        NA_times_z_0_vals = []
        distance_ratio_vals = []
        optimization_score_vals = []

        for parameters, optimization_result in zip(calibration_results_per_step, optimization_results_per_step):
            delta_x_vals.append(parameters.delta_x)
            delta_y_vals.append(parameters.delta_y)
            rotation_vals.append(parameters.rotation * 180/np.pi)
            NA_times_z_0_vals.append(parameters.numerical_aperture_times_LED_distance)
            distance_ratio_vals.append(parameters.distance_ratio)
            optimization_score_vals.append(optimization_result.fun)


        delta_x_vals_per_dataset.append(delta_x_vals)
        delta_y_vals_per_dataset.append(delta_y_vals)
        rotation_vals_per_dataset.append(rotation_vals)
        NA_times_z_0_vals_per_dataset.append(np.array(NA_times_z_0_vals))
        distance_ratio_vals_per_dataset.append(np.array(distance_ratio_vals))
        optimization_score_vals_per_dataset.append(np.array(optimization_score_vals))

        optimization_score_filter_value = 2 * np.median(np.array(optimization_score_vals_per_dataset))


    fig, axes = plt.subplots(1,1)
    fig.suptitle("Delta x")
    for delta_x_vals in delta_x_vals_per_dataset:
        axes.scatter(relative_LED_distances, delta_x_vals)
    plot_path = result_folder / f"delta_x"
    fig.savefig(plot_path.with_suffix(f".pdf"), format = "pdf")
    fig.savefig(plot_path.with_suffix(f".png"), format = "png")

    fig, axes = plt.subplots(1,1)
    fig.suptitle("Delta y")
    for delta_y_vals in delta_y_vals_per_dataset:
        axes.scatter(relative_LED_distances, delta_y_vals)
    plot_path = result_folder / f"delta_y"
    fig.savefig(plot_path.with_suffix(f".pdf"), format = "pdf")
    fig.savefig(plot_path.with_suffix(f".png"), format = "png")

    fig, axes = plt.subplots(1,1)
    fig.suptitle("Rotation")
    for rotation_vals in rotation_vals_per_dataset:
        axes.scatter(relative_LED_distances, rotation_vals)
    plot_path = result_folder / f"rotation"
    fig.savefig(plot_path.with_suffix(f".pdf"), format = "pdf")
    fig.savefig(plot_path.with_suffix(f".png"), format = "png")

    fig, axes = plt.subplots(1,1)
    fig.suptitle("Optimization score")
    for optimization_score_vals in optimization_score_vals_per_dataset:
        axes.scatter(relative_LED_distances, optimization_score_vals)
    axes.hlines(optimization_score_filter_value, relative_LED_distances[0], relative_LED_distances[-1])
    plot_path = result_folder / f"optimization_score"
    fig.savefig(plot_path.with_suffix(f".pdf"), format = "pdf")
    fig.savefig(plot_path.with_suffix(f".png"), format = "png")


    fig, axes = plt.subplots(1,1)
    fig.suptitle("NA * z_0")
    fig1, axes1 = plt.subplots(1,1)
    fig1.suptitle("NA * z_0 (filtered)")
    for NA_times_z_0_vals, optimization_score_vals in zip(NA_times_z_0_vals_per_dataset, optimization_score_vals_per_dataset):
        filtered_vals = NA_times_z_0_vals[np.argwhere(optimization_score_vals < optimization_score_filter_value)].flatten()
        filtered_LED_distances = relative_LED_distances[np.argwhere(optimization_score_vals < optimization_score_filter_value)].flatten()

        result = linregress(relative_LED_distances, NA_times_z_0_vals)
        axes.scatter(relative_LED_distances, NA_times_z_0_vals)
        axes.plot(relative_LED_distances, result.slope*relative_LED_distances + result.intercept, 
                label = f"{result.slope:.3f} x + {result.slope:.3f}*{result.intercept/result.slope:.3f}")
        
        if len(filtered_vals) == 0:
            continue
        result = linregress(filtered_LED_distances, filtered_vals)
        axes1.scatter(filtered_LED_distances, filtered_vals)
        axes1.plot(relative_LED_distances, result.slope*relative_LED_distances + result.intercept, 
                label = f"{result.slope:.3f} x + {result.slope:.3f}*{result.intercept/result.slope:.3f}")
    axes.legend()
    axes1.legend()
    plot_path = result_folder / f"NA_times_z_0"
    fig.savefig(plot_path.with_suffix(f".pdf"), format = "pdf")
    fig.savefig(plot_path.with_suffix(f".png"), format = "png")
    plot_path = result_folder / f"NA_times_z_0_filtered"
    fig1.savefig(plot_path.with_suffix(f".pdf"), format = "pdf")
    fig1.savefig(plot_path.with_suffix(f".png"), format = "png")


    fig, axes = plt.subplots(1,1)
    fig.suptitle("z_0 / z_q")
    fig1, axes1 = plt.subplots(1,1)
    fig1.suptitle("z_0 / z_q (filtered)")
    for distance_ratio_vals, optimization_score_vals in zip(distance_ratio_vals_per_dataset, optimization_score_vals_per_dataset):
        filtered_vals = distance_ratio_vals[np.argwhere(optimization_score_vals < optimization_score_filter_value)].flatten()
        filtered_LED_distances = relative_LED_distances[np.argwhere(optimization_score_vals < optimization_score_filter_value)].flatten()

        result = linregress(relative_LED_distances, distance_ratio_vals)
        axes.scatter(relative_LED_distances, distance_ratio_vals)
        axes.plot(relative_LED_distances, result.slope*relative_LED_distances + result.intercept, 
                label = f"{result.slope:.3f} x + {result.slope:.3f}*{result.intercept/result.slope:.3f}")
        
        if len(filtered_vals) == 0:
            continue

        result = linregress(filtered_LED_distances, filtered_vals)
        axes1.scatter(filtered_LED_distances, filtered_vals)
        axes1.plot(relative_LED_distances, result.slope*relative_LED_distances + result.intercept, 
                label = f"{result.slope:.3f} x + {result.slope:.3f}*{result.intercept/result.slope:.3f}")
    axes.legend()
    axes1.legend()
    plot_path = result_folder / f"distance_ratio"
    fig.savefig(plot_path.with_suffix(f".pdf"), format = "pdf")
    fig.savefig(plot_path.with_suffix(f".png"), format = "png")
    plot_path = result_folder / f"distance_ratio_filtered"
    fig1.savefig(plot_path.with_suffix(f".pdf"), format = "pdf")
    fig1.savefig(plot_path.with_suffix(f".png"), format = "png")

    plt.show()