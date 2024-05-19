
from pyFPM.calibration.non_linear_BFL.shared import Calibration_parameters

from typing import List
import numpy as np
from scipy.stats import linregress
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.optimize import OptimizeResult
import pickle
import latextable
import texttable
 
def get_pickle_path(raw_result_folder: Path, filename):
    pickle_path: Path = raw_result_folder / filename
    return pickle_path.with_suffix(".obj")

def unpickle_optimization_results_per_step(raw_result_folder) -> List[OptimizeResult]:
    pickle_path = get_pickle_path(raw_result_folder, filename="optimization_results_per_step")
    with open(pickle_path, "rb") as file:
        optimization_results_per_step: List[Calibration_parameters] = pickle.load(file)
    return optimization_results_per_step

def unpickle_calibration_results_per_step(raw_result_folder) -> List[Calibration_parameters]:
    pickle_path = get_pickle_path(raw_result_folder, filename="calibration_results_per_step")
    with open(pickle_path, "rb") as file:
        calibration_results_per_step: List[Calibration_parameters] = pickle.load(file)
    return calibration_results_per_step


def plot_BFL_step_experiments_combined(raw_result_folders: List[Path],
                                        result_folder: Path,
                                        relative_LED_distances,
                                        filter_factor: float):

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


        delta_x_vals_per_dataset.append(np.array(delta_x_vals))
        delta_y_vals_per_dataset.append(np.array(delta_y_vals))
        rotation_vals_per_dataset.append(np.array(rotation_vals))
        NA_times_z_0_vals_per_dataset.append(np.array(NA_times_z_0_vals))
        distance_ratio_vals_per_dataset.append(np.array(distance_ratio_vals))
        optimization_score_vals_per_dataset.append(np.array(optimization_score_vals))

        optimization_score_filter_value = filter_factor * np.median(np.array(optimization_score_vals_per_dataset))


    fig = plt.figure(figsize=(9,6), constrained_layout = True)
    gs = fig.add_gridspec(6, 5)

    axes_z_q = fig.add_subplot(gs[3:6, 0:3])
    axes_NA = fig.add_subplot(gs[0:3, 0:3], sharex=axes_z_q)
    axes_rot = fig.add_subplot(gs[4:6, 3:5])
    axes_x = fig.add_subplot(gs[0:2, 3:5], sharex=axes_rot)
    axes_y = fig.add_subplot(gs[2:4, 3:5], sharex=axes_rot)
    
    #convert to mm
    relative_LED_distances *= 1000

    max_NA_times_z_0_val = 0
    max_distance_ratio_val = 0

    result_table = texttable.Texttable()
    result_table.set_cols_align(["c", "c", "c", "c", "c"])
    result_table.set_cols_dtype(["t","t","t","t","t"])
    result_table.add_row(["Dataset nr.",r"$\textit{NA}$", "$z'_{NA}$", "$z_q$", "$z'_{z_q}$"])
    sum_NA = 0
    sum_z_q = 0

    for n, (NA_times_z_0_vals, distance_ratio_vals, delta_x_vals, delta_y_vals, rotation_vals, optimization_score_vals) in \
        enumerate(zip(NA_times_z_0_vals_per_dataset, distance_ratio_vals_per_dataset, delta_x_vals_per_dataset, 
            delta_y_vals_per_dataset, rotation_vals_per_dataset, optimization_score_vals_per_dataset)):
        
        filtered_NA_times_z_0_vals = NA_times_z_0_vals[np.argwhere(optimization_score_vals < optimization_score_filter_value)].flatten()
        filtered_distance_ratio_vals = distance_ratio_vals[np.argwhere(optimization_score_vals < optimization_score_filter_value)].flatten()
        filtered_relative_LED_distances = relative_LED_distances[np.argwhere(optimization_score_vals < optimization_score_filter_value)].flatten()
        filtered_delta_x_vals = delta_x_vals[np.argwhere(optimization_score_vals < optimization_score_filter_value)].flatten()
        filtered_delta_y_vals = delta_y_vals[np.argwhere(optimization_score_vals < optimization_score_filter_value)].flatten()
        filtered_rotation_vals = rotation_vals[np.argwhere(optimization_score_vals < optimization_score_filter_value)].flatten()

        # convert to mm
        filtered_NA_times_z_0_vals *= 1000
        # convert to um
        filtered_delta_x_vals *= 1e6
        filtered_delta_y_vals *= 1e6
        
        result_NA = linregress(filtered_relative_LED_distances, filtered_NA_times_z_0_vals)
        result_z_q = linregress(filtered_relative_LED_distances, filtered_distance_ratio_vals)
    
        NA = result_NA.slope
        z_0_from_NA = result_NA.intercept/NA
        z_q = 1 / result_z_q.slope
        z_0_from_z_q = result_z_q.intercept*z_q

        axes_NA.scatter(filtered_relative_LED_distances, filtered_NA_times_z_0_vals, marker="o", alpha = 0.7)
        axes_NA.plot(relative_LED_distances, relative_LED_distances*NA + z_0_from_NA*NA, 
                label = f"(z+{z_0_from_NA:.0f})*{NA:.3f}", linestyle = "dotted")
        
        axes_z_q.scatter(filtered_relative_LED_distances, filtered_distance_ratio_vals, marker="o", alpha = 0.7)
        axes_z_q.plot(relative_LED_distances, relative_LED_distances/z_q + z_0_from_z_q/z_q, 
                label = f"(z+{z_0_from_z_q:.0f})/{z_q:.0f}", linestyle = "dotted")

        axes_x.scatter(filtered_relative_LED_distances, filtered_delta_x_vals, marker="o", alpha = 0.7)
        axes_y.scatter(filtered_relative_LED_distances, filtered_delta_y_vals, marker="o", alpha = 0.7)
        axes_rot.scatter(filtered_relative_LED_distances, filtered_rotation_vals, marker="o", alpha = 0.7)

        max_NA_times_z_0_val = np.max([max_NA_times_z_0_val, np.max(filtered_NA_times_z_0_vals)])
        max_distance_ratio_val = np.max([max_distance_ratio_val, np.max(filtered_distance_ratio_vals)])



        #result_table.add_row(["Dataset nr.","NA", "$z'_{NA}$", "$z_q$", "z'_{z_q}"])
        result_table.add_row([n+1,f"{NA:.3f}", f"{z_0_from_NA:.0f}", f"{z_q:.0f}", f"{z_0_from_z_q:.0f}"])
        sum_NA += NA
        sum_z_q += z_q

    nr_of_datasets = len(optimization_score_vals_per_dataset)
    mean_NA = sum_NA / nr_of_datasets
    mean_z_q = sum_z_q / nr_of_datasets

    result_table.add_row(["Mean", f"{mean_NA:.3f}", "", f"{mean_z_q:.0f}", ""])

    axes_z_q.set_xlabel("Relative LED distance [mm]")
    axes_rot.set_xlabel("Relative LED distance [mm]")

    axes_rot.set_ylabel("Rotation [deg]")
    axes_NA.set_ylabel(r"$NA \cdot z$ [m]")
    axes_z_q.set_ylabel(r"$z / z_q$ [unitless]")
    axes_x.set_ylabel(r"$\Delta x$ [µm]")
    axes_y.set_ylabel(r"$\Delta y$ [µm]")

    axes_x.yaxis.set_label_position("right")
    axes_x.yaxis.tick_right()
    axes_y.yaxis.set_label_position("right")
    axes_y.yaxis.tick_right()
    axes_rot.yaxis.set_label_position("right")
    axes_rot.yaxis.tick_right()

    axes_NA.set_ylim(bottom=0, top=max_NA_times_z_0_val*1.07)
    axes_z_q.set_ylim(bottom=0, top=max_distance_ratio_val*1.07)

    axes_NA.legend(loc = "lower right")
    axes_z_q.legend(loc = "lower right")

    fig.align_ylabels([axes_z_q, axes_NA])
    fig.align_ylabels([axes_x, axes_y, axes_rot])

    plot_path = result_folder / f"combined_results"
    fig.savefig(plot_path.with_suffix(f".pdf"), format = "pdf")
    fig.savefig(plot_path.with_suffix(f".png"), format = "png")




    fig, axes = plt.subplots(1, 2, figsize=(8,3), constrained_layout = True)
    for optimization_score_vals in optimization_score_vals_per_dataset:
        axes[0].scatter(relative_LED_distances, optimization_score_vals, marker="o", alpha = 0.7)
    axes[0].hlines(optimization_score_filter_value, relative_LED_distances[0], relative_LED_distances[-1], linestyles="dashed")
    axes[0].set_ylabel("Cost function value [unitless]")
    axes[0].set_xlabel("Relative LED distance [mm]")
    axes[0].set_ylim(bottom=0, top=np.max([np.max(optimization_score_vals_per_dataset), optimization_score_filter_value])*1.07)


    for optimization_score_vals in optimization_score_vals_per_dataset:
        axes[1].scatter(relative_LED_distances[np.argwhere(optimization_score_vals < 1.5 * optimization_score_filter_value)].flatten(), 
                     optimization_score_vals[np.argwhere(optimization_score_vals < 1.5 * optimization_score_filter_value)].flatten(), 
                     marker="o", alpha = 0.7)   
    axes[1].hlines(optimization_score_filter_value, relative_LED_distances[0], relative_LED_distances[-1], linestyles="dashed")
    axes[1].set_ylabel("Cost function value [unitless]")
    axes[1].set_xlabel("Relative LED distance [mm]")
    axes[1].set_ylim(bottom=0, top=1.5 * optimization_score_filter_value * 1.07)
    axes[1].yaxis.set_label_position("right")
    axes[1].yaxis.tick_right()


    plot_path = result_folder / f"optimization_score"
    fig.savefig(plot_path.with_suffix(f".pdf"), format = "pdf")
    fig.savefig(plot_path.with_suffix(f".png"), format = "png")

    



    print('Texttable Output:')
    print(result_table.draw())
    print('\nLatextable Output:')
    print(latextable.draw_latex(result_table))


    
    plt.show()



