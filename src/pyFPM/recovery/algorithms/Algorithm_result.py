from dataclasses import dataclass
import numpy as np

from pyFPM.setup.Imaging_system import Imaging_system

@dataclass
class Algorithm_result:
    recovered_object: np.ndarray
    recovered_object_fourier_transform: np.ndarray
    pupil: np.ndarray
    convergence_index: np.ndarray
    real_space_error_metric: np.ndarray
    low_res_image: np.ndarray
    recovered_CTF: np.ndarray
    imaging_system: Imaging_system
    amplitude_error: np.ndarray
    masked_amplitude_error: np.ndarray
