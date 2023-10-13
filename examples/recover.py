from enum import Enum
import matplotlib.pyplot as plt
import numpy as np

# FPM imports
from pyFPM.NTNU_specific.setup_2x_hamamatsu import setup_2x_hamamatsu
from pyFPM.recovery.algorithms.run_algorithm import recover, Method
from pyFPM.aberrations.pupils.defocused_pupil import get_defocused_pupil

# utility imports
from plotting.plot_experimental_results import plot_experimental_results


datadirpath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\20230825_USAFtarget"
#datadirpath = r"c:\Users\erlen\Documents\GitHub\pyFPM\data\EHJ20230915_dotarray_2x_inf"

pixel_scale_factor = 4
patch_start = [870, 870] # [x, y]
patch_size = [256, 256] # [x, y]

method = Method.Fraunhofer
loops = 3

setup_parameters, data_patch, imaging_system, illumination_pattern = setup_2x_hamamatsu(
    datadirpath = datadirpath,
    patch_start = patch_start,
    patch_size = patch_size,
    pixel_scale_factor = pixel_scale_factor
)

# define pupil
defocus_guess = 20e-6
pupil_guess = get_defocused_pupil(imaging_system = imaging_system, defocus = defocus_guess)


algorithm_result = recover(method=method, data_patch=data_patch, imaging_system=imaging_system,
                           illumination_pattern=illumination_pattern, pupil_guess=pupil_guess,
                           loops=loops)

plot_experimental_results(data_patch, illumination_pattern, imaging_system, algorithm_result)
