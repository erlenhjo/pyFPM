from pyFPM.recovery.algorithms import Algorithm_result

import pickle
from pathlib import Path


def define_pickle_path(experiment_name, file_name):
    cwd = Path.cwd()
    pickle_folder = cwd / "results" / "pickles" / experiment_name
    pickle_path = pickle_folder / file_name
    return pickle_path

def pickle_algorithm_results(pickle_path, algorithm_result: Algorithm_result):
    with open(pickle_path, "wb") as file:
        pickle.dump(algorithm_result, file)

def unpickle_algorithm_results(pickle_path):
    with open(pickle_path, "rb") as file:
        algorithm_result: Algorithm_result = pickle.load(file)
    return algorithm_result
