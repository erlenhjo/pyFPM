from enum import Enum
import matplotlib.pyplot as plt
import numpy as np

# FPM imports
from pyFPM.NTNU_specific.simulated_images import simulate_cameraman_2x
from pyFPM.recovery.algorithms.run_algorithm import recover, Method

# import plotting
from plotting.plot_simulation_results import plot_simulation_results

method = Method.Epry_Gradient_Descent
loops = 100

setup_parameters, data_patch, imaging_system, illumination_pattern, applied_pupil\
      = simulate_cameraman_2x(noise_fraction=0, zernike_coefficients=[0,0,0,0,0.1])


# define pupil
pupil_guess = applied_pupil * 0 + 1

algorithm_result = recover(
    method=method,
    data_patch=data_patch,
    imaging_system=imaging_system,
    illumination_pattern=illumination_pattern,
    pupil_guess=pupil_guess,
    loops=loops
)

plot_simulation_results(data_patch, illumination_pattern, imaging_system, algorithm_result)

print(algorithm_result.convergence_index)