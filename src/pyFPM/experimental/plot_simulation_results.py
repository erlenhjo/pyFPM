import matplotlib.pyplot as plt
import numpy as np

from pyFPM.aberrations.zernike_polynomials.plot_zernike_coefficients import plot_zernike_coefficients
from pyFPM.aberrations.pupils.zernike_pupil import decompose_zernike_pupil
from pyFPM.recovery.algorithms.Algorithm_result import Algorithm_result



def plot_simulation_results(
        algorithm_result: Algorithm_result,
        original_zernike_coefficients,
        original_pupil
    ):
    imaging_system = algorithm_result.imaging_system
    low_res_CTF = imaging_system.low_res_CTF

    fig, axes = plt.subplots(nrows=3, ncols=4, layout='constrained', figsize=(12,9))
    axes: list[plt.Axes] = axes.flatten()
    
    axes[0].set_title("Low resolution image")
    axes[0].matshow(algorithm_result.low_res_image**2)
    axes[0].axis("off")
    axes[0].margins(x=0, y=0)

    axes[1].set_title(f"Recovered image")
    axes[1].matshow(np.abs(algorithm_result.recovered_object)**2)    
    axes[1].axis("off")
    axes[1].margins(x=0, y=0)

    axes[2].set_title(f"Recovered phase")
    cax = axes[2].matshow(np.angle(algorithm_result.recovered_object), vmin=-np.pi, vmax=np.pi)    
    axes[2].axis("off")
    axes[2].margins(x=0, y=0)
    fig.colorbar(cax)

    nonzero_y, nonzero_x = np.nonzero(algorithm_result.recovered_object_fourier_transform)
    min_x, max_x = np.min(nonzero_x), np.max(nonzero_x)
    min_y, max_y = np.min(nonzero_y), np.max(nonzero_y)

    axes[3].set_title(f"Recovered fourier spectrum")
    axes[3].matshow(np.log(np.abs(algorithm_result.recovered_object_fourier_transform[min_y:max_y+1, min_x:max_x+1])**2))
    axes[3].axis("off")
    axes[3].margins(x=0, y=0)


    axes[4].set_title(f"Original pupil amplitude")
    axes[4].matshow(np.abs(original_pupil) * low_res_CTF)
    axes[4].axis("off")
    axes[4].margins(x=0, y=0)

    axes[5].set_title(f"Original pupil phase")
    axes[5].matshow(np.angle(original_pupil) * low_res_CTF, vmin=-np.pi, vmax=np.pi)
    axes[5].axis("off")
    axes[5].margins(x=0, y=0)

    axes[6].set_title(f"Recovered pupil amplitude")
    axes[6].matshow(np.abs(algorithm_result.pupil) * low_res_CTF)
    axes[6].axis("off")
    axes[6].margins(x=0, y=0)

    axes[7].set_title(f"Recovered pupil angle")
    axes[7].matshow(np.angle(algorithm_result.pupil) * low_res_CTF, vmin=-np.pi, vmax=np.pi)
    axes[7].axis("off")
    axes[7].margins(x=0, y=0)

    plot_zernike_coefficients(axes[8], original_zernike_coefficients, title="Original zernike coefficients")

    recovered_zernike_coefficients = decompose_zernike_pupil(imaging_system=imaging_system,
                                                             pupil=algorithm_result.pupil, 
                                                             max_j=original_zernike_coefficients.shape[0]-1)
    
    plot_zernike_coefficients(axes[9], recovered_zernike_coefficients, title="Recovered zernike coefficients")

    error = recovered_zernike_coefficients[2:] - original_zernike_coefficients[2:]
    axes[10].plot(np.arange(error.shape[0])+2, error)
    axes[10].set_title("Error of Zernike coefficients")
    y_max = np.max(np.abs(error))*1.2
    axes[10].set_ylim(-y_max, y_max)


    axes[11].set_title(f"Real space error metric")
    axes[11].plot(algorithm_result.real_space_error_metric)
    axes[11].set_xlabel("Loop number")




