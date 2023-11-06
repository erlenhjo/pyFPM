from dataclasses import dataclass
import numpy as np

from pyFPM.setup.Illumination_pattern import Illumination_pattern

@dataclass
class Step_description:
    alpha: float
    beta: float
    eta: float|None
    converged_alpha: float
    max_iterations: int
    use_adaptive_step_size: bool


def get_standard_adaptive_step_description(illumination_pattern: Illumination_pattern,
                                           max_iterations: int):
    return Step_description(alpha=1,
                            beta=1/np.sqrt(np.sqrt(len(illumination_pattern.update_order))),
                            eta=0.01,
                            converged_alpha=1e-3,
                            max_iterations=max_iterations,
                            use_adaptive_step_size=True)

def get_constant_step_description(max_iterations):
    return Step_description(alpha=1,
                            beta=1,
                            eta=None,
                            converged_alpha=0,
                            max_iterations=max_iterations,
                            use_adaptive_step_size=False)