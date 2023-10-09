from enum import Enum
import matplotlib.pyplot as plt
import numpy as np

# setup imports
from pyFPM.NTNU_specific.setup_2x_hamamatsu import setup_2x_hamamatsu

# recovery method imports
from pyFPM.recovery.algorithms.primitive_algorithm import primitive_fourier_ptychography_algorithm

# utility imports
from utility import plot_results


class Method(Enum):
    Primitive = 1
    Epry = 2
    Epry_Gradient_Descent = 3
    Fresnel = 4
    Fresnel_Epry = 5

datadirpath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\20230825_USAFtarget"
#datadirpath = r"c:\Users\erlen\Documents\GitHub\pyFPM\data\EHJ20230915_dotarray_2x_inf"

pixel_scale_factor = 4
patch_start = [870, 870] # [x, y]
patch_size = [256, 256] # [x, y]

method = Method.Primitive
defocus_guess = 20e-6
loops = 3

setup_parameters, data_patch, imaging_system, illumination_pattern = setup_2x_hamamatsu(
    datadirpath = datadirpath,
    patch_start = patch_start,
    patch_size = patch_size,
    pixel_scale_factor = pixel_scale_factor
)

if method == Method.Primitive:
    algorithm_result = primitive_fourier_ptychography_algorithm(
        data_patch = data_patch,
        imaging_system = imaging_system,
        illumination_pattern = illumination_pattern,
        pupil = imaging_system.get_pupil(defocus = defocus_guess),
        loops = loops
    )
elif method == Method.Epry:
    algorithm_result = primitive_fourier_ptychography_algorithm(
        data_patch = data_patch,
        imaging_system = imaging_system,
        illumination_pattern = illumination_pattern,
        pupil = imaging_system.get_pupil(defocus = defocus_guess),
        loops = loops,
        use_epry = True,
        use_gradient_descent = False
    )
elif method == Method.Epry_Gradient_Descent:
    algorithm_result = primitive_fourier_ptychography_algorithm(
        data_patch = data_patch,
        imaging_system = imaging_system,
        illumination_pattern = illumination_pattern,
        pupil = imaging_system.get_pupil(defocus = defocus_guess),
        loops = loops,
        use_epry = True,
        use_gradient_descent = True
    )
else:
    raise "Recovery with specified method not implemented"


plot_results(data_patch, illumination_pattern, imaging_system, algorithm_result)
