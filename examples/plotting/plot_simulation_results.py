import matplotlib.pyplot as plt

import numpy as np
from numpy.fft import fft2, fftshift, ifftshift

# setup imports
from pyFPM.setup.Illumination_pattern import Illumination_pattern
from pyFPM.setup.Data import Data_patch
from pyFPM.setup.Imaging_system import Imaging_system

# recovery method imports
from pyFPM.recovery.algorithms.Algorithm_result import Algorithm_result



def plot_simulation_results(
        data_patch: Data_patch, 
        illumination_pattern: Illumination_pattern,
        imaging_system: Imaging_system,
        algorithm_result: Algorithm_result
    ):
    fig, axes = plt.subplots(nrows=2, ncols=4)
    axes: list[plt.Axes] = axes.flatten()
    
    axes[0].set_title("Original image")
    axes[0].matshow(data_patch.amplitude_images[illumination_pattern.update_order[0]]**2)
    axes[0].axis("off")

    axes[1].set_title("Original fourier spectrum")
    axes[1].matshow(np.log(np.abs(fftshift(fft2(ifftshift(data_patch.amplitude_images[illumination_pattern.update_order[0]]))))**2))
    axes[1].axis("off")

    axes[2].set_title(f"Recovered pupil amplitude")
    axes[2].matshow(np.abs(algorithm_result.pupil) * imaging_system.low_res_CTF)
    axes[2].axis("off")

    axes[3].set_title(f"Recovered pupil angle")
    axes[3].matshow(np.angle(algorithm_result.pupil) * imaging_system.low_res_CTF, vmin=-np.pi, vmax=np.pi)
    axes[3].axis("off")

    axes[4].set_title(f"Recovered image")
    axes[4].matshow(np.abs(algorithm_result.recovered_object)**2)    
    axes[4].axis("off")

    axes[5].set_title(f"Recovered phase")
    axes[5].matshow(np.angle(algorithm_result.recovered_object), vmin=-np.pi, vmax=np.pi)    
    axes[5].axis("off")

    nonzero_y, nonzero_x = np.nonzero(algorithm_result.recovered_object_fourier_transform)
    min_x, max_x = np.min(nonzero_x), np.max(nonzero_x)
    min_y, max_y = np.min(nonzero_y), np.max(nonzero_y)

    axes[6].set_title(f"Recovered FS intensity")
    axes[6].matshow(np.log(np.abs(algorithm_result.recovered_object_fourier_transform[min_y:max_y+1, min_x:max_x+1])**2))
    axes[6].axis("off")

    axes[7].set_title(f"Recovered FS phase")
    axes[7].matshow(np.angle(algorithm_result.recovered_object_fourier_transform[min_y:max_y+1, min_x:max_x+1]), vmin=-np.pi, vmax=np.pi)
    axes[7].axis("off")

    fig.tight_layout()
    plt.show()

    plt.close()

