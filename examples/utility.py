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
    axes[0].imshow(preprocessed_data.amplitude_images[illumination_pattern.update_order[0]]**2)
    axes[0].axis("off")

    axes[1].set_title("Raw fourier spectrum")
    axes[1].imshow(np.log(np.abs(fftshift(fft2(ifftshift(preprocessed_data.amplitude_images[illumination_pattern.update_order[0]]))))**2))
    axes[1].axis("off")

    axes[2].set_title("Coherent transfer function")
    axes[2].imshow(imaging_system.low_res_CTF)
    axes[2].axis("off")

    axes[3].set_title(f"Recovered image")
    axes[3].imshow(np.abs(algorithm_result.recovered_object)**2)    
    axes[3].axis("off")

    axes[4].set_title(f"Recovered fourier spectrum")
    axes[4].imshow(np.log(np.abs(algorithm_result.recovered_object_fourier_transform)**2))
    axes[4].axis("off")

    axes[5].set_title(f"Recovered pupil")
    axes[5].imshow(np.angle(algorithm_result.pupil) * imaging_system.low_res_CTF)
    axes[5].axis("off")

    fig.tight_layout()
    plt.show()

