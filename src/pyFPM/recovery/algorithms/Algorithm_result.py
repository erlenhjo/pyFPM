from dataclasses import dataclass
import numpy as np

@dataclass
class Algorithm_result:
    recovered_object: np.ndarray
    recovered_object_fourier_transform: np.ndarray
    pupil: np.ndarray
    convergence_index: np.ndarray
    real_space_error_metric: np.ndarray
