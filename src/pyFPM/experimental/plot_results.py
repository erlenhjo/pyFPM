import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes, mark_inset
import numpy as np

# setup imports
from pyFPM.aberrations.zernike_polynomials.plot_zernike_coefficients import plot_zernike_coefficients
from pyFPM.aberrations.pupils.zernike_pupil import decompose_zernike_pupil
from pyFPM.recovery.algorithms.Algorithm_result import Algorithm_result


def plot_results(
        algorithm_result: Algorithm_result,
        title = "",
        max_j = 25
    ):
    imaging_system = algorithm_result.imaging_system

    fig, axes = plt.subplots(nrows=2, ncols=4, layout='constrained', figsize=(12,9))
    fig.suptitle(title)
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
    axes[2].matshow(np.angle(algorithm_result.recovered_object), vmin=-np.pi, vmax=np.pi)    
    axes[2].axis("off")
    axes[2].margins(x=0, y=0)

    nonzero_y, nonzero_x = np.nonzero(algorithm_result.recovered_object_fourier_transform)
    min_x, max_x = np.min(nonzero_x), np.max(nonzero_x)
    min_y, max_y = np.min(nonzero_y), np.max(nonzero_y)

    axes[3].set_title(f"Recovered fourier spectrum")
    axes[3].matshow(np.log(np.abs(algorithm_result.recovered_object_fourier_transform[min_y:max_y+1, min_x:max_x+1])**2))
    axes[3].axis("off")
    axes[3].margins(x=0, y=0)


    axes[4].set_title(f"Recovered pupil amplitude")
    axes[4].matshow(np.abs(algorithm_result.pupil) * imaging_system.low_res_CTF)
    axes[4].axis("off")
    axes[4].margins(x=0, y=0)

    axes[5].set_title(f"Recovered pupil angle")
    axes[5].matshow(np.angle(algorithm_result.pupil) * imaging_system.low_res_CTF, vmin=-np.pi, vmax=np.pi)
    axes[5].axis("off")
    axes[5].margins(x=0, y=0)

    recovered_zernike_coefficients = decompose_zernike_pupil(imaging_system=imaging_system, pupil=algorithm_result.pupil, 
                                                             max_j=max_j)
    plot_zernike_coefficients(axes[6], recovered_zernike_coefficients, title="Recovered zernike coefficients")

    axes[7].set_title(f"Real space error metric")
    axes[7].plot(algorithm_result.real_space_error_metric)
    axes[7].set_xlabel("Loop number")
    axes[7].set_yscale("log")

    return fig


def plot_results_short(
        algorithm_result: Algorithm_result,
        title = ""
    ):
    fig, axes = plt.subplots(nrows=1, ncols=3, layout='constrained')
    fig.suptitle(title)
    axes: list[plt.Axes] = axes.flatten()
    
    axes[0].set_title("Low resolution image")
    axes[0].matshow(algorithm_result.low_res_image**2)
    axes[0].axis("off")
    axes[0].margins(x=0, y=0)

    axins_0 = zoomed_inset_axes(axes[0], zoom=4, loc="upper right")
    axins_0.matshow(algorithm_result.low_res_image**2)
    axins_0.set_xlim(105,135)
    axins_0.set_ylim(116,141)
    axins_0.xaxis.set_ticklabels([])
    axins_0.yaxis.set_ticklabels([])
    mark_inset(axes[0], axins_0, loc1=2, loc2=4, fc="none", ec="0.5")

    axes[1].set_title(f"Recovered image")
    axes[1].matshow(np.abs(algorithm_result.recovered_object)**2)    
    axes[1].axis("off")
    axes[1].margins(x=0, y=0)

    axins_1 = zoomed_inset_axes(axes[1], zoom=4, loc="upper right")
    axins_1.matshow(np.abs(algorithm_result.recovered_object)**2)
    axins_1.set_xlim(840,1080)
    axins_1.set_ylim(930,1130)
    axins_1.xaxis.set_ticklabels([])
    axins_1.yaxis.set_ticklabels([])

    mark_inset(axes[1], axins_1, loc1=2, loc2=4, fc="none", ec="0.5")

    axes[2].set_title(f"Recovered phase")
    axes[2].matshow(np.angle(algorithm_result.recovered_object), vmin=-np.pi, vmax=np.pi)    
    axes[2].axis("off")
    axes[2].margins(x=0, y=0)

    return fig


def plot_phase(
        algorithm_result: Algorithm_result
    ):
    fig, axes = plt.subplots(nrows=1, ncols=1, constrained_layout=True, figsize=(4,4))

    axes.matshow(np.angle(algorithm_result.recovered_object), vmin=-np.pi, vmax=np.pi)    
    axes.axis("off")

    return fig