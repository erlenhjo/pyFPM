from pyFPM.recovery.algorithms import Algorithm_result
from pyFPM.experimental.plot_results import *
from pyFPM.experimental.plot_info import Plot_parameters, Plot_types

import pickle
from pathlib import Path

def define_pickle_folder(experiment_name):
    cwd = Path.cwd()
    pickle_folder: Path = cwd / "results" / "pickles" / experiment_name
    pickle_folder.mkdir(parents=True, exist_ok=True)
    return pickle_folder

def define_plot_folder(experiment_name, result_folder):
    plot_folder: Path = result_folder / experiment_name
    plot_folder.mkdir(parents=True, exist_ok=True)
    return plot_folder

def define_pickle_path(pickle_folder: Path, file_name):
    pickle_path: Path = pickle_folder / file_name
    return pickle_path.with_suffix(".obj")

def define_plot_path(plot_folder: Path, file_name):
    plot_path: Path = plot_folder / file_name
    plot_path.mkdir(parents=True, exist_ok=True)
    return plot_path

def unpickle_algorithm_results(pickle_path):
    with open(pickle_path, "rb") as file:
        algorithm_result: Algorithm_result = pickle.load(file)
    return algorithm_result

def pickle_algorithm_results(algorithm_result: Algorithm_result, experiment_name, file_name):
    pickle_folder = define_pickle_folder(experiment_name = experiment_name)
    pickle_path = define_pickle_path(pickle_folder = pickle_folder,
                                     file_name = file_name)
    with open(pickle_path, "wb") as file:
        pickle.dump(algorithm_result, file)

def plot_pickled_experiment(experiment_name, result_folder,
                            plot_types: Plot_types, plot_parameters: Plot_parameters):
    pickle_folder: Path = define_pickle_folder(experiment_name=experiment_name)
    plot_folder: Path = define_plot_folder(experiment_name=experiment_name, result_folder=result_folder)
    nr_of_pickles = 0
    for pickle_path in pickle_folder.iterdir():
        nr_of_pickles += 1
    for pickle_path in pickle_folder.iterdir():
        file_name = pickle_path.stem
        algorithm_result = unpickle_algorithm_results(pickle_path)
        
        if nr_of_pickles == 1:
            main_plot_path = plot_folder
        else:
            main_plot_path = plot_folder / file_name
            main_plot_path.mkdir(parents=True, exist_ok=True)

        if plot_types.overview:
            fig = plot_overview(algorithm_result=algorithm_result, title=file_name,
                                max_j=plot_parameters.max_zernike_j)
            plot_path = main_plot_path / "overview"
            fig.savefig(plot_path.with_suffix(f".{plot_parameters.format}"), format = plot_parameters.format, bbox_inches="tight", dpi=1000)

        if plot_types.object_overview:
            fig = plot_object_overview(algorithm_result=algorithm_result)
            plot_path = main_plot_path / "recovered object overview"
            fig.savefig(plot_path.with_suffix(f".{plot_parameters.format}"), format = plot_parameters.format, bbox_inches="tight", dpi=1000)

        if plot_types.recovered_phase:
            fig = plot_object_phase(algorithm_result=algorithm_result)
            plot_path = main_plot_path / "recovered phase"
            fig.savefig(plot_path.with_suffix(f".{plot_parameters.format}"), format = plot_parameters.format, bbox_inches="tight", dpi=1000)

        if plot_types.recovered_phase_with_zoom:
            fig = plot_object_phase_with_zoom(algorithm_result=algorithm_result,
                                              zoom_location=plot_parameters.recovered_phase_zoom_location,
                                              zoom_ratio=plot_parameters.zoom_ratio)
            plot_path = main_plot_path / "recovered phase with zoom"
            fig.savefig(plot_path.with_suffix(f".{plot_parameters.format}"), format = plot_parameters.format, bbox_inches="tight", dpi=1000)

        if plot_types.recovered_phase_zoom_only:
            fig = plot_object_phase_zoom_only(algorithm_result=algorithm_result,
                                              zoom_ratio=plot_parameters.zoom_ratio)
            plot_path = main_plot_path / "recovered phase zoom only"
            fig.savefig(plot_path.with_suffix(f".{plot_parameters.format}"), format = plot_parameters.format, bbox_inches="tight", dpi=1000)

        if plot_types.raw_image_with_zoom:
            fig = plot_low_res_intensity_with_zoom(algorithm_result=algorithm_result,
                                                  zoom_location=plot_parameters.low_res_intensity_zoom_location,
                                              zoom_ratio=plot_parameters.zoom_ratio)
            plot_path = main_plot_path / "raw image with zoom"
            fig.savefig(plot_path.with_suffix(f".{plot_parameters.format}"), format = plot_parameters.format, bbox_inches="tight", dpi=1000)

        if plot_types.recovered_intensity_with_zoom:
            fig = plot_object_intensity_with_zoom(algorithm_result=algorithm_result,
                                                  zoom_location=plot_parameters.recovered_intensity_zoom_location,
                                                  zoom_ratio=plot_parameters.zoom_ratio)
            plot_path = main_plot_path / "recovered intensity with zoom"
            fig.savefig(plot_path.with_suffix(f".{plot_parameters.format}"), format = plot_parameters.format, bbox_inches="tight", dpi=1000)

        if plot_types.recovered_intensity_zoom_only:
            fig = plot_object_intensity_zoom_only(algorithm_result=algorithm_result,
                                              zoom_ratio=plot_parameters.zoom_ratio)
            plot_path = main_plot_path / "recovered intensity zoom only"
            fig.savefig(plot_path.with_suffix(f".{plot_parameters.format}"), format = plot_parameters.format, bbox_inches="tight", dpi=1000)


        if plot_types.recovered_spectrum:
            fig = plot_spectrum(algorithm_result=algorithm_result)
            plot_path = main_plot_path / "recovered spectrum"
            fig.savefig(plot_path.with_suffix(f".{plot_parameters.format}"), format = plot_parameters.format, bbox_inches="tight", dpi=1000)

        if plot_types.recovered_pupil_overview:
            fig = plot_pupil_overview(algorithm_result=algorithm_result,
                                max_j=plot_parameters.max_zernike_j,
                                zernike_coefficient_max=plot_parameters.zernike_coefficient_max)
            plot_path = main_plot_path / "pupil_overview"
            fig.savefig(plot_path.with_suffix(f".{plot_parameters.format}"), format = plot_parameters.format, bbox_inches="tight", dpi=1000)

        if plot_types.recovered_pupil_amplitude:
            fig = plot_pupil_amplitude(algorithm_result=algorithm_result)
            plot_path = main_plot_path / "pupil_amplitude"
            fig.savefig(plot_path.with_suffix(f".{plot_parameters.format}"), format = plot_parameters.format, bbox_inches="tight", dpi=1000)

        if plot_types.recovered_pupil_phase:
            fig = plot_pupil_phase(algorithm_result=algorithm_result)
            plot_path = main_plot_path / "pupil_phase"
            fig.savefig(plot_path.with_suffix(f".{plot_parameters.format}"), format = plot_parameters.format, bbox_inches="tight", dpi=1000)

        if plot_types.recovered_pupil_coefficients:
            fig = plot_pupil_coefficients(algorithm_result=algorithm_result,
                                    max_j=plot_parameters.max_zernike_j,
                                    zernike_coefficient_max=plot_parameters.zernike_coefficient_max)
            plot_path = main_plot_path / "pupil_coefficients"
            fig.savefig(plot_path.with_suffix(f".{plot_parameters.format}"), format = plot_parameters.format, bbox_inches="tight", dpi=1000)





def compare_experiment_pupils(experiment_names, result_folder,
                                plot_parameters: Plot_parameters,
                                pupil_amplitude_limits, 
                                pupil_phase_limits,
                                labels, lens_name):
    algorithm_results = []
    for experiment_name in experiment_names:
        pickle_folder: Path = define_pickle_folder(experiment_name=experiment_name)
        for pickle_path in pickle_folder.iterdir():
            file_name = pickle_path.stem
            algorithm_result = unpickle_algorithm_results(pickle_path)
            algorithm_results.append(algorithm_result)
        

    fig = plot_pupil_amp_and_coefficients_comparative(algorithm_results=algorithm_results, 
                                                      max_j=plot_parameters.max_zernike_j, 
                                                      zernike_coefficient_limits=[plot_parameters.zernike_coefficient_min, plot_parameters.zernike_coefficient_max],
                                                      pupil_amplitude_limits=pupil_amplitude_limits,
                                                      pupil_phase_limits=pupil_phase_limits, 
                                                      labels=labels)
    
    file_name = "pupils_comparative_"+lens_name
    plot_path = result_folder / file_name
    fig.savefig(plot_path.with_suffix(f".{plot_parameters.format}"), format = plot_parameters.format, bbox_inches="tight", dpi=1000)
