from pyFPM.recovery.algorithms import Algorithm_result
from pyFPM.experimental.plot_results import plot_results

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
    return pickle_path

def define_plot_path(plot_folder: Path, file_name):
    plot_path: Path = plot_folder / file_name
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

def plot_pickled_experiment(experiment_name):
    pickle_folder: Path = define_pickle_folder(experiment_name=experiment_name)
    plot_folder: Path = define_plot_folder(experiment_name=experiment_name)
    for pickle_path in pickle_folder.iterdir():
        file_name = pickle_path.stem
        algorithm_result = unpickle_algorithm_results(pickle_path)
        fig = plot_results(algorithm_result=algorithm_result, title=file_name)
        plot_path = define_plot_path(plot_folder=plot_folder, file_name=file_name)
        #fig.savefig(plot_path.with_suffix(".pdf"), format = "pdf")
        fig.savefig(plot_path.with_suffix(".png"), format = "png")