# FPM imports
from pyFPM.setup.Setup_parameters import Lens
from pyFPM.setup.Imaging_system import LED_calibration_parameters
from pyFPM.recovery.algorithms.run_algorithm import recover, Method
from pyFPM.aberrations.pupils.defocus_and_window import get_defocused_pupil
from pyFPM.aberrations.pupils.zernike_pupil import get_zernike_pupil
from pyFPM.recovery.algorithms.Step_description import Step_description
from pyFPM.experimental.pickle_results import pickle_algorithm_results, plot_pickled_experiment

from dataclasses import dataclass
from typing import List, Callable
import numpy as np

@dataclass
class Experiment_settings:
    lens: Lens
    method: Method
    calibration_parameters: LED_calibration_parameters
    step_description: Step_description
    pixel_scale_factor: int
    binning_factor: int
    threshold_value: int
    noise_reduction_regions: List[List[int]]
    defocus_guess: float
    limited_import: List[int]
    circular_LED_pattern: bool

def recover_experiment(experiment_name, datadirpath, patch_offsets, patch_size, max_array_size, experiment_settings: Experiment_settings, 
                       setup_local: Callable, setup_global: Callable, zernike_coefficients = None):
    
    if experiment_settings.limited_import is None:
        limited_import_patch = None
        limited_import_shift = np.array([0,0])
    elif len(experiment_settings.limited_import) == 2:
        limited_import_patch = np.array(experiment_settings.limited_import)
        limited_import_shift = np.array([0,0])
    elif len(experiment_settings.limited_import) == 4:
        limited_import_patch = np.array(experiment_settings.limited_import[0:2])
        limited_import_shift = np.array(experiment_settings.limited_import[2:4])
        limited_import_shift = limited_import_shift // experiment_settings.binning_factor * experiment_settings.binning_factor

    setup_parameters, preprocessed_data = setup_global(experiment_settings.lens,
                                                        datadirpath,
                                                        experiment_settings.threshold_value,
                                                        experiment_settings.noise_reduction_regions,
                                                        max_array_size,
                                                        experiment_settings.binning_factor,
                                                        limited_import_patch,
                                                        limited_import_shift,
                                                        experiment_settings.circular_LED_pattern
                                                        )
    
    

    for patch_offset in patch_offsets:

        imaging_system, data_patch, illumination_pattern = setup_local(setup_parameters,
                                                                            preprocessed_data,
                                                                            patch_offset,
                                                                            patch_size,
                                                                            experiment_settings.pixel_scale_factor,
                                                                            experiment_settings.calibration_parameters,
                                                                            max_array_size,
                                                                            limited_import_shift // experiment_settings.binning_factor,
                                                                            experiment_settings.circular_LED_pattern
                                                                            )

        pupil_guess = get_defocused_pupil(imaging_system = imaging_system, defocus = experiment_settings.defocus_guess)
        if zernike_coefficients is not None:
            pupil_guess = get_zernike_pupil(imaging_system=imaging_system, zernike_coefficients=zernike_coefficients)

        algorithm_result = recover(method=experiment_settings.method, data_patch=data_patch, imaging_system=imaging_system,
                                illumination_pattern=illumination_pattern, pupil_guess=pupil_guess,
                                step_description=experiment_settings.step_description)

        file_name = f"LEDs_{max_array_size}x{max_array_size}_size_{patch_size[0]}x{patch_size[1]}_offset_{patch_offset[0]}_{patch_offset[1]}"

        pickle_algorithm_results(algorithm_result=algorithm_result,
                                experiment_name=experiment_name, 
                                file_name=file_name)
    return




    
