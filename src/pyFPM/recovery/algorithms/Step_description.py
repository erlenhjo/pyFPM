from dataclasses import dataclass

@dataclass
class Step_description:
    alpha: float
    beta: float
    eta: float|None
    converged_alpha: float
    max_iterations: int
    start_EPRY_at_iteration: int
    start_adaptive_at_iteration: int
    apply_BF_mask_from_iteration: int


def get_standard_adaptive_step_description(max_iterations: int,
                                           start_EPRY_at_iteration: int,
                                           start_adaptive_at_iteration: int,
                                           apply_BF_mask_from_iteration: int):
    return Step_description(alpha=1,
                            beta=1,
                            eta=0.01,
                            converged_alpha=1e-3,
                            max_iterations=max_iterations,
                            start_EPRY_at_iteration = start_EPRY_at_iteration,
                            start_adaptive_at_iteration = start_adaptive_at_iteration,
                            apply_BF_mask_from_iteration = apply_BF_mask_from_iteration)
