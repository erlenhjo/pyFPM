import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes, mark_inset
import numpy as np

# setup imports
from pyFPM.aberrations.zernike_polynomials.plot_zernike_coefficients import plot_zernike_coefficients
from pyFPM.aberrations.pupils.zernike_pupil import decompose_zernike_pupil
from pyFPM.recovery.algorithms.Algorithm_result import Algorithm_result


def plot_results_all(
        algorithm_result: Algorithm_result,
        title = "",
        max_j = 25
    ):
    imaging_system = algorithm_result.imaging_system

    fig, axes = plt.subplots(nrows=2, ncols=4, constrained_layout=True, figsize=(12,9))
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

    full_spectrum = np.log(np.abs(algorithm_result.recovered_object_fourier_transform)**2)
    cropped_spectrum = full_spectrum[min_y:max_y, min_x:max_x]
    recovered_CTF = algorithm_result.recovered_CTF
    cropped_recovered_CTF = recovered_CTF[min_y:max_y, min_x:max_x]
    
    spectrum = np.ma.masked_where(cropped_recovered_CTF == 0, cropped_spectrum)

    axes[3].set_title(f"Recovered fourier spectrum")
    axes[3].matshow(spectrum)
    axes[3].axis("off")
    axes[3].margins(x=0, y=0)

    imaging_system = algorithm_result.imaging_system
    pupil = algorithm_result.pupil

    nonzero_y, nonzero_x = np.nonzero(imaging_system.low_res_CTF)
    min_x, max_x = np.min(nonzero_x), np.max(nonzero_x)+1
    min_y, max_y = np.min(nonzero_y), np.max(nonzero_y)+1
    cropped_low_res_CTF = imaging_system.low_res_CTF[min_y:max_y, min_x:max_x]
    cropped_pupil = pupil[min_y:max_y, min_x:max_x]
    pupil_amplitude = np.ma.masked_where(cropped_low_res_CTF == 0, np.abs(cropped_pupil))
    pupil_phase = np.ma.masked_where(cropped_low_res_CTF == 0, np.angle(cropped_pupil))


    axes[4].set_title(f"Recovered pupil amplitude")
    axes[4].matshow(pupil_amplitude)
    axes[4].axis("off")
    axes[4].margins(x=0, y=0)

    axes[5].set_title(f"Recovered pupil angle")
    axes[5].matshow(pupil_phase, vmin=-np.pi, vmax=np.pi)
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


def plot_results_object(
        algorithm_result: Algorithm_result,
    ):
    fig, axes = plt.subplots(1, 3, constrained_layout=True, figsize=(10,8))
    axes: list[plt.Axes] = axes.flatten()
    
    low_res_intensity = algorithm_result.low_res_image**2
    recovered_intensity = np.abs(algorithm_result.recovered_object)**2
    recovered_phase = np.angle(algorithm_result.recovered_object)

    axes[0].set_title("Low resolution intensity")
    axes[0].matshow(low_res_intensity)
    axes[0].axis("off")
    axes[0].margins(x=0, y=0)

    axes[1].set_title(f"Recovered intensity")
    axes[1].matshow(recovered_intensity)    
    axes[1].axis("off")
    axes[1].margins(x=0, y=0)

    axes[2].set_title(f"Recovered phase")
    axes[2].matshow(recovered_phase, vmin=-np.pi, vmax=np.pi)    
    axes[2].axis("off")
    axes[2].margins(x=0, y=0)
    
    inset_axes_size = [1, 1] # width, height
    inset_axes_locs = [[0, -1.05], [0, -1.05], [0, -1.05]]
    inset_line_color = "red"

    for ax, axes_loc, image in zip([axes[0], axes[1], axes[2]], inset_axes_locs, [low_res_intensity, recovered_intensity, recovered_phase]):
        max_x = image.shape[1]
        max_y = image.shape[0]
        center_x = max_x // 2
        center_y = max_y // 2 
        size = max_x // 4        

        start_x = center_x - size//2
        stop_x = center_x + size//2
        start_y = center_y - size//2
        stop_y = center_y + size//2
    
        subimage = image[start_y:stop_y, start_x:stop_x]

        axin = ax.inset_axes(
            axes_loc + inset_axes_size,
            xlim = (start_x, stop_x),
            ylim = (start_y, stop_y)
        )
        _, connector_lines = ax.indicate_inset_zoom(axin, edgecolor=inset_line_color)
        for line in connector_lines:
            line.set_visible(True)

        axin.set_xlim(auto=True)
        axin.set_ylim(auto=True)
        axin.imshow(subimage)
        axin.set_xticks([])
        axin.set_yticks([])

    fig.set_constrained_layout_pads()

    return fig


def plot_results_phase(
        algorithm_result: Algorithm_result
    ):
    fig, axes = plt.subplots(nrows=1, ncols=1, constrained_layout=True, figsize=(4,4))

    axes.matshow(np.angle(algorithm_result.recovered_object), vmin=-np.pi, vmax=np.pi)    
    axes.axis("off")

    return fig


def plot_results_spectrum(
        algorithm_result: Algorithm_result
    ):
    fig, axes = plt.subplots(nrows=1, ncols=1, constrained_layout=True, figsize=(4,4))

    nonzero_y, nonzero_x = np.nonzero(algorithm_result.recovered_object_fourier_transform)
    min_x, max_x = np.min(nonzero_x), np.max(nonzero_x)
    min_y, max_y = np.min(nonzero_y), np.max(nonzero_y)

    full_spectrum = np.log(np.abs(algorithm_result.recovered_object_fourier_transform)**2)
    cropped_spectrum = full_spectrum[min_y:max_y, min_x:max_x]
    recovered_CTF = algorithm_result.recovered_CTF
    cropped_recovered_CTF = recovered_CTF[min_y:max_y, min_x:max_x]
    
    spectrum = np.ma.masked_where(cropped_recovered_CTF == 0, cropped_spectrum)

    axes.matshow(spectrum)
    axes.axis("off")

    return fig

def plot_results_pupil(
        algorithm_result: Algorithm_result,
        max_j = 25
    ):
    fig = plt.figure(constrained_layout=True, figsize=(10, 3))
    sf1, sf2, sf3 = fig.subfigures(1, 3, wspace=0.05, width_ratios=[0.25,0.25,0.5])
    ax1 = sf1.subplots(1,1)
    ax2 = sf2.subplots(1,1)
    ax3 = sf3.subplots(1,1)

    imaging_system = algorithm_result.imaging_system
    pupil = algorithm_result.pupil

    nonzero_y, nonzero_x = np.nonzero(imaging_system.low_res_CTF)
    min_x, max_x = np.min(nonzero_x), np.max(nonzero_x)+1
    min_y, max_y = np.min(nonzero_y), np.max(nonzero_y)+1
    cropped_low_res_CTF = imaging_system.low_res_CTF[min_y:max_y, min_x:max_x]
    cropped_pupil = pupil[min_y:max_y, min_x:max_x]
    pupil_amplitude = np.ma.masked_where(cropped_low_res_CTF == 0, np.abs(cropped_pupil))
    pupil_phase = np.ma.masked_where(cropped_low_res_CTF == 0, np.angle(cropped_pupil))

    ax1.matshow(pupil_amplitude)
    ax1.axis("off")

    ax2.matshow(pupil_phase, vmin=-np.pi, vmax=np.pi)
    ax2.axis("off")

    recovered_zernike_coefficients = decompose_zernike_pupil(imaging_system=imaging_system, pupil=pupil, 
                                                             max_j=max_j)
    plot_zernike_coefficients(ax3, recovered_zernike_coefficients, title=None)

    ax3.yaxis.set_label_position("right")
    ax3.yaxis.tick_right()

    sf1.suptitle("Amplitude")
    sf2.suptitle('Phase')
    sf3.suptitle('Zernike coefficients')

    return fig