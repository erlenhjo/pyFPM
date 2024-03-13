# FPM imports
from pyFPM.setup.Setup_parameters import Lens
from pyFPM.setup.Imaging_system import LED_calibration_parameters
from pyFPM.recovery.algorithms.run_algorithm import recover, Method
from pyFPM.aberrations.pupils.defocused_pupil import get_defocused_pupil
from pyFPM.recovery.algorithms.Step_description import Step_description
from pyFPM.experimental.pickle_results import pickle_algorithm_results, plot_pickled_experiment

from dataclasses import dataclass
from typing import List, Callable

@dataclass
class Experiment_settings:
    lens: Lens
    method: Method
    calibration_parameters: LED_calibration_parameters
    step_description: Step_description
    pixel_scale_factor: int
    threshold_value: int
    noise_reduction_regions: List[List[int]]
    defocus_guess: float

def recover_experiment(experiment_name, datadirpath, patch_offsets, patch_size, max_array_size, experiment_settings: Experiment_settings, setup_local: Callable, setup_global: Callable):

    setup_parameters, preprocessed_data = setup_global(experiment_settings.lens,
                                                              datadirpath,
                                                              experiment_settings.threshold_value,
                                                              experiment_settings.noise_reduction_regions,
                                                              max_array_size
                                                             )
    

    for patch_offset in patch_offsets:

        imaging_system, data_patch, illumination_pattern = setup_local(setup_parameters,
                                                                            preprocessed_data,
                                                                            patch_offset,
                                                                            patch_size,
                                                                            experiment_settings.pixel_scale_factor,
                                                                            experiment_settings.calibration_parameters,
                                                                            max_array_size
                                                                            )

        pupil_guess = get_defocused_pupil(imaging_system = imaging_system, defocus = experiment_settings.defocus_guess)

        algorithm_result = recover(method=experiment_settings.method, data_patch=data_patch, imaging_system=imaging_system,
                                illumination_pattern=illumination_pattern, pupil_guess=pupil_guess,
                                step_description=experiment_settings.step_description)

        file_name = f"LEDs_{max_array_size}x{max_array_size}_size_{patch_size[0]}x{patch_size[1]}_offset_{patch_offset[0]}_{patch_offset[1]}.obj"

        pickle_algorithm_results(algorithm_result=algorithm_result,
                                experiment_name=experiment_name, 
                                file_name=file_name)
    return


def plot_experiment(experiment_name):

    plot_pickled_experiment(experiment_name)

    
