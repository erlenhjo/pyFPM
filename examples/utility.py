import matplotlib.pyplot as plt
from matplotlib.colors import SymLogNorm
import numpy as np
from numpy.fft import fft2, ifft2, fftshift, ifftshift

# setup imports
from pyFPM.setup.Illumination_pattern import Illumination_pattern
from pyFPM.setup.Preprocessed_data import Preprocessed_data
from pyFPM.setup.Imaging_system import Imaging_system

# recovery method imports
from pyFPM.recovery.algorithms.Algorithm_result import Algorithm_result

def plot_results(
        preprocessed_data: Preprocessed_data, 
        illumination_pattern: Illumination_pattern,
        imaging_system: Imaging_system,
        algorithm_result: Algorithm_result
    ):
    fig, axes = plt.subplots(nrows=2, ncols=3)
    axes: list[plt.Axes] = axes.flatten()
    
    axes[0].set_title("Raw image")
    axes[0].matshow(preprocessed_data.amplitude_images[illumination_pattern.update_order[0]]**2)
    axes[0].axis("off")

    axes[1].set_title("Raw fourier spectrum")
    axes[1].matshow(np.log(np.abs(fftshift(fft2(ifftshift(preprocessed_data.amplitude_images[illumination_pattern.update_order[0]]))))**2))
    axes[1].axis("off")

    axes[2].set_title(f"Recovered pupil amplitude")
    axes[2].matshow(np.abs(algorithm_result.pupil) * imaging_system.low_res_CTF)
    axes[2].axis("off")

    axes[3].set_title(f"Recovered image")
    axes[3].matshow(np.abs(algorithm_result.recovered_object)**2)    
    axes[3].axis("off")

    nonzero_y, nonzero_x = np.nonzero(algorithm_result.recovered_object_fourier_transform)
    min_x, max_x = np.min(nonzero_x), np.max(nonzero_x)
    min_y, max_y = np.min(nonzero_y), np.max(nonzero_y)

    axes[4].set_title(f"Recovered fourier spectrum")
    axes[4].matshow(np.log(np.abs(algorithm_result.recovered_object_fourier_transform[min_y:max_y+1, min_x:max_x+1])**2))
    axes[4].axis("off")

    axes[5].set_title(f"Recovered pupil angle")
    axes[5].matshow(np.angle(algorithm_result.pupil) * imaging_system.low_res_CTF)
    axes[5].axis("off")

    fig.tight_layout()
    plt.show()

    plt.close()

