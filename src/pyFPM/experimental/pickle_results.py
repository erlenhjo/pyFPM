from pyFPM.recovery.algorithms import Algorithm_result
from pyFPM.experimental.plot_results import (plot_results_all, plot_results_object, 
                                             plot_results_phase, plot_results_pupil, 
                                             plot_results_spectrum)

import pickle
from pathlib import Path


def define_pickle_folder(experiment_name):
    cwd = Path.cwd()
    pickle_folder: Path = cwd / "results" / "pickles" / experiment_name
    pickle_folder.mkdir(parents=True, exist_ok=True)
    return pickle_folder

def define_plot_folder(experiment_name):
    cwd = Path.cwd()
    plot_folder: Path = cwd / "results" / "plots" / experiment_name
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

def plot_pickled_experiment(experiment_name, alternative_result_folder):
    pickle_folder: Path = define_pickle_folder(experiment_name=experiment_name)
    plot_folder: Path = define_plot_folder(experiment_name=experiment_name)
    for pickle_path in pickle_folder.iterdir():
        file_name = pickle_path.stem
        algorithm_result = unpickle_algorithm_results(pickle_path)
        
        if alternative_result_folder is None:
            main_plot_path = define_plot_path(plot_folder=plot_folder, file_name=file_name)
        else:
            main_plot_path = alternative_result_folder
            alternative_result_folder.mkdir(parents=True, exist_ok=True)

        fig = plot_results_all(algorithm_result=algorithm_result, title=file_name)
        plot_path = main_plot_path / "all"
        fig.savefig(plot_path.with_suffix(".pdf"), format = "pdf")
        fig.savefig(plot_path.with_suffix(".png"), format = "png")

        fig = plot_results_phase(algorithm_result=algorithm_result)
        plot_path = main_plot_path / "phase"
        fig.savefig(plot_path.with_suffix(".pdf"), format = "pdf")
        fig.savefig(plot_path.with_suffix(".png"), format = "png")

        fig = plot_results_pupil(algorithm_result=algorithm_result)
        plot_path = main_plot_path / "pupil"
        fig.savefig(plot_path.with_suffix(".pdf"), format = "pdf")
        fig.savefig(plot_path.with_suffix(".png"), format = "png")

        fig = plot_results_spectrum(algorithm_result=algorithm_result)
        plot_path = main_plot_path / "spectrum"
        fig.savefig(plot_path.with_suffix(".pdf"), format = "pdf")
        fig.savefig(plot_path.with_suffix(".png"), format = "png")

        fig = plot_results_object(algorithm_result=algorithm_result)
        plot_path = main_plot_path / "object"
        fig.savefig(plot_path.with_suffix(".pdf"), format = "pdf", bbox_inches="tight")
        fig.savefig(plot_path.with_suffix(".png"), format = "png", bbox_inches="tight")
