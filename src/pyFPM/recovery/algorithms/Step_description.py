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
    start_EPRY_at_iteration: int
    start_adaptive_at_iteration: int


def get_standard_adaptive_step_description(illumination_pattern: Illumination_pattern,
                                           max_iterations: int,
                                           start_EPRY_at_iteration: int,
                                           start_adaptive_at_iteration: int):
    return Step_description(alpha=1,
                            beta=1,
                            eta=0.01,
                            converged_alpha=1e-3,
                            max_iterations=max_iterations,
                            start_EPRY_at_iteration = start_EPRY_at_iteration,
                            start_adaptive_at_iteration = start_adaptive_at_iteration)

def get_constant_step_description(max_iterations, start_EPRY_at_iteration):
    return Step_description(alpha=1,
                            beta=1,
                            eta=None,
                            converged_alpha=0,
                            max_iterations=max_iterations,
                            start_EPRY_at_iteration = start_EPRY_at_iteration,
                            start_adaptive_at_iteration=2*max_iterations)