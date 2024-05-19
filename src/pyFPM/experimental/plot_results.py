# setup imports
from pyFPM.aberrations.zernike_polynomials.plot_zernike_coefficients import plot_zernike_coefficients, plot_zernike_coefficients_comparative
from pyFPM.aberrations.pupils.zernike_pupil import decompose_zernike_pupil
from pyFPM.recovery.algorithms.Algorithm_result import Algorithm_result
from pyFPM.experimental.plot_info import Zoom_location
from pyFPM.aberrations.pupils.defocus_and_window import defocus_distance_from_zernike_coefficient

import matplotlib.pyplot as plt
from matplotlib.figure import SubFigure
import numpy as np
from typing import List

def get_central_zoomed_image(image, zoom_ratio):
        max_x = image.shape[1]
        max_y = image.shape[0]
        center_x = max_x // 2
        center_y = max_y // 2 
        size = int(max_x // zoom_ratio)        

        start_x = center_x - size//2
        stop_x = center_x + size//2
        start_y = center_y - size//2
        stop_y = center_y + size//2
    
        subimage = image[start_y:stop_y, start_x:stop_x]
        x_lim = (start_x, stop_x)
        y_lim = (start_y, stop_y)

        return subimage, x_lim, y_lim

def create_central_zoom(ax, image, location: Zoom_location, inset_line_color, vlims, zoom_ratio):
        inset_axes_size = (1, 1) # width, height
        inset_axes_loc = location.coordinates

        subimage, x_lim, y_lim = get_central_zoomed_image(image, zoom_ratio)

        axin = ax.inset_axes(
            inset_axes_loc + inset_axes_size,
            xlim = x_lim,
            ylim = y_lim
        )
        _, connector_lines = ax.indicate_inset_zoom(axin, edgecolor=inset_line_color)
        for line in connector_lines:
            line.set_visible(True)

        axin.set_xlim(auto=True)
        axin.set_ylim(auto=True)
        axin.imshow(subimage, vmin=vlims[0], vmax=vlims[1])
        axin.set_xticks([])
        axin.set_yticks([])


def plot_overview(
        algorithm_result: Algorithm_result,
        title,
        max_j
    ):
    imaging_system = algorithm_result.imaging_system

    fig, axes = plt.subplots(nrows=2, ncols=4, constrained_layout=True, figsize=(12,9))
    fig.suptitle(title)
    axes: list[plt.Axes] = axes.flatten()
    
    vlims_raw = (0, np.max(algorithm_result.low_res_image**2))
    axes[0].set_title("Low resolution image")
    axes[0].matshow(algorithm_result.low_res_image**2, vmin=vlims_raw[0], vmax=vlims_raw[1])
    axes[0].axis("off")
    axes[0].margins(x=0, y=0)

    vlims_intensity = (0, np.max(np.abs(algorithm_result.recovered_object)**2))
    axes[1].set_title(f"Recovered image")
    axes[1].matshow(np.abs(algorithm_result.recovered_object)**2, vmin=vlims_intensity[0], vmax=vlims_intensity[1])    
    axes[1].axis("off")
    axes[1].margins(x=0, y=0)

    vlims_phase = (-np.pi, np.pi)
    axes[2].set_title(f"Recovered phase")
    axes[2].matshow(np.angle(algorithm_result.recovered_object), vmin=vlims_phase[0], vmax=vlims_phase[1])    
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
    axes[4].matshow(pupil_amplitude, vmin=0, vmax=2)
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


def plot_object_overview(
        algorithm_result: Algorithm_result,
        zoom_ratio
    ):
    fig, axes = plt.subplots(1, 3, constrained_layout=True, figsize=(10,8))
    axes: list[plt.Axes] = axes.flatten()
    
    low_res_intensity = algorithm_result.low_res_image**2
    recovered_intensity = np.abs(algorithm_result.recovered_object)**2
    recovered_phase = np.angle(algorithm_result.recovered_object)

    vlims_raw = (0, np.max(low_res_intensity))
    axes[0].set_title("Low resolution intensity")
    axes[0].matshow(low_res_intensity, vmin=vlims_raw[0], vmax=vlims_raw[1])
    axes[0].axis("off")
    axes[0].margins(x=0, y=0)

    vlims_intensity = (0, np.max(recovered_intensity))
    axes[1].set_title(f"Recovered intensity")
    axes[1].matshow(recovered_intensity, vmin=vlims_intensity[0], vmax=vlims_intensity[1])    
    axes[1].axis("off")
    axes[1].margins(x=0, y=0)

    vlims_phase = (-np.pi, np.pi)
    axes[2].set_title(f"Recovered phase")
    axes[2].matshow(recovered_phase, vmin=vlims_phase[0], vmax=vlims_phase[1])    
    axes[2].axis("off")
    axes[2].margins(x=0, y=0)

    inset_axes_locs = [Zoom_location.below, Zoom_location.below, Zoom_location.below]
    inset_line_color = "red"

    for ax, axes_loc, image, vlims in zip([axes[0], axes[1], axes[2]], inset_axes_locs, 
                                   [low_res_intensity, recovered_intensity, recovered_phase],
                                   [vlims_raw, vlims_intensity, vlims_phase]):
         create_central_zoom(ax, image, axes_loc, inset_line_color, vlims, zoom_ratio)

    fig.set_constrained_layout_pads()

    return fig

def plot_low_res_intensity_with_zoom(
        algorithm_result: Algorithm_result,
        zoom_location,
        zoom_ratio
    ):
    fig, axes = plt.subplots(1, 1, constrained_layout=True)
    
    low_res_intensity = algorithm_result.low_res_image**2
    vlims = [0, np.max(low_res_intensity)]

    axes.matshow(low_res_intensity, vmin=vlims[0], vmax=vlims[1])    
    axes.axis("off")
    axes.margins(x=0, y=0)

    inset_line_color = "red"

    create_central_zoom(axes, low_res_intensity, zoom_location, inset_line_color, vlims, zoom_ratio)

    fig.set_constrained_layout_pads()

    return fig

def plot_object_intensity_with_zoom(
        algorithm_result: Algorithm_result,
        zoom_location,
        zoom_ratio
    ):
    fig, axes = plt.subplots(1, 1, constrained_layout=True)
    
    recovered_intensity = np.abs(algorithm_result.recovered_object)**2
    vlims = [0, np.max(recovered_intensity)]

    axes.matshow(recovered_intensity, vmin=vlims[0], vmax=vlims[1])    
    axes.axis("off")
    axes.margins(x=0, y=0)

    inset_line_color = "red"

    create_central_zoom(axes, recovered_intensity, zoom_location, inset_line_color, vlims, zoom_ratio)

    fig.set_constrained_layout_pads()

    return fig

def plot_object_intensity_zoom_only(
        algorithm_result: Algorithm_result,
        zoom_ratio: float
    ):
    fig, axes = plt.subplots(1, 1, constrained_layout=True)
    
    recovered_intensity = np.abs(algorithm_result.recovered_object)**2
    vlims = [0, np.max(recovered_intensity)]
    zoomed_image, _, _ = get_central_zoomed_image(recovered_intensity, zoom_ratio)

    axes.matshow(zoomed_image, vmin=vlims[0], vmax=vlims[1])    
    axes.axis("off")
    axes.margins(x=0, y=0)

    return fig

def plot_object_phase_with_zoom(
        algorithm_result: Algorithm_result,
        zoom_location,
        zoom_ratio
    ):
    fig, axes = plt.subplots(1, 1, constrained_layout=True)
    
    recovered_phase = np.angle(algorithm_result.recovered_object)
    vlims = [-np.pi, np.pi]

    axes.matshow(recovered_phase, vmin=vlims[0], vmax=vlims[1])    
    axes.axis("off")
    axes.margins(x=0, y=0)

    inset_line_color = "red"

    create_central_zoom(axes, recovered_phase, zoom_location, inset_line_color, vlims, zoom_ratio)

    fig.set_constrained_layout_pads()

    return fig

def plot_object_phase_zoom_only(
        algorithm_result: Algorithm_result,
        zoom_ratio: float
    ):
    fig, axes = plt.subplots(1, 1, constrained_layout=True)
    
    recovered_phase = np.angle(algorithm_result.recovered_object)
    vlims = [-np.pi, np.pi]
    zoomed_image, _, _ = get_central_zoomed_image(recovered_phase, zoom_ratio)

    axes.matshow(zoomed_image, vmin=vlims[0], vmax=vlims[1])    
    axes.axis("off")
    axes.margins(x=0, y=0)

    return fig

def plot_object_phase(
        algorithm_result: Algorithm_result
    ):
    fig, axes = plt.subplots(nrows=1, ncols=1, constrained_layout=True, figsize=(4,4))

    axes.matshow(np.angle(algorithm_result.recovered_object), vmin=-np.pi, vmax=np.pi)    
    axes.axis("off")

    return fig


def plot_spectrum(
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

def plot_pupil_overview(
        algorithm_result: Algorithm_result,
        max_j: int,
        zernike_coefficient_max: float
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
    if zernike_coefficient_max is not None:
        ax3.set_ylim(bottom=-zernike_coefficient_max, top=zernike_coefficient_max)

    ax3.yaxis.set_label_position("right")
    ax3.yaxis.tick_right()

    sf1.suptitle("Amplitude")
    sf2.suptitle('Phase')
    sf3.suptitle('Zernike coefficients')

    return fig

def plot_pupil_amplitude(
        algorithm_result: Algorithm_result
    ):
    fig, axes = plt.subplots(1, 1, constrained_layout=True, figsize=(2.5, 3))

    imaging_system = algorithm_result.imaging_system
    pupil = algorithm_result.pupil

    nonzero_y, nonzero_x = np.nonzero(imaging_system.low_res_CTF)
    min_x, max_x = np.min(nonzero_x), np.max(nonzero_x)+1
    min_y, max_y = np.min(nonzero_y), np.max(nonzero_y)+1
    cropped_low_res_CTF = imaging_system.low_res_CTF[min_y:max_y, min_x:max_x]
    cropped_pupil = pupil[min_y:max_y, min_x:max_x]
    pupil_amplitude = np.ma.masked_where(cropped_low_res_CTF == 0, np.abs(cropped_pupil))

    axes.matshow(pupil_amplitude, vmin=0, vmax=1.5)
    axes.axis("off")
    return fig

def plot_pupil_phase(
        algorithm_result: Algorithm_result
    ):
    fig, axes = plt.subplots(1, 1, constrained_layout=True, figsize=(2.5, 3))

    imaging_system = algorithm_result.imaging_system
    pupil = algorithm_result.pupil

    nonzero_y, nonzero_x = np.nonzero(imaging_system.low_res_CTF)
    min_x, max_x = np.min(nonzero_x), np.max(nonzero_x)+1
    min_y, max_y = np.min(nonzero_y), np.max(nonzero_y)+1
    cropped_low_res_CTF = imaging_system.low_res_CTF[min_y:max_y, min_x:max_x]
    cropped_pupil = pupil[min_y:max_y, min_x:max_x]
    pupil_phase = np.ma.masked_where(cropped_low_res_CTF == 0, np.angle(cropped_pupil))

    axes.matshow(pupil_phase, vmin=-np.pi, vmax=np.pi)
    axes.axis("off")
    return fig

def plot_pupil_coefficients(
        algorithm_result: Algorithm_result,
        max_j,
        zernike_coefficient_max: float
    ):
    fig, axes = plt.subplots(1, 1, constrained_layout=True, figsize=(5, 3))

    imaging_system = algorithm_result.imaging_system
    pupil = algorithm_result.pupil

    recovered_zernike_coefficients = decompose_zernike_pupil(imaging_system=imaging_system, pupil=pupil, 
                                                             max_j=max_j)
    plot_zernike_coefficients(axes, recovered_zernike_coefficients, title=None)
    if zernike_coefficient_max is not None:
        axes.set_ylim(bottom=-zernike_coefficient_max, top=zernike_coefficient_max)

    return fig

def plot_pupil_amp_and_coefficients_comparative(
        algorithm_results: Algorithm_result,
        max_j,
        zernike_coefficient_limits: List[float],
        pupil_amplitude_limits: List[float],
        pupil_phase_limits: List[float],
        labels
    ):
    fig = plt.figure(figsize = (3, 5), constrained_layout = True)
    subfigs = fig.subfigures(2,1,height_ratios=[3,2])
    subfig_amp: SubFigure = subfigs[0]
    subfig_coeff: SubFigure = subfigs[1]
    axes_pupil_amplitude: List[List[plt.Axes]] = subfig_amp.subplots(2,2,sharex=True, sharey=True)
    axes_coefficients: plt.Axes = subfig_coeff.subplots(1,1)

    for axes, label, algorithm_result in zip(axes_pupil_amplitude, labels, algorithm_results):
        pupil = algorithm_result.pupil
        imaging_system = algorithm_result.imaging_system
        
        nonzero_y, nonzero_x = np.nonzero(imaging_system.low_res_CTF)
        min_x, max_x = np.min(nonzero_x), np.max(nonzero_x)+1
        min_y, max_y = np.min(nonzero_y), np.max(nonzero_y)+1
        cropped_low_res_CTF = imaging_system.low_res_CTF[min_y:max_y, min_x:max_x]
        cropped_pupil = pupil[min_y:max_y, min_x:max_x]
        pupil_amplitude = np.ma.masked_where(cropped_low_res_CTF == 0, np.abs(cropped_pupil))
        pupil_phase = np.ma.masked_where(cropped_low_res_CTF == 0, np.angle(cropped_pupil))
        pupil_phase = pupil_phase - np.mean([pupil_phase.min(), pupil_phase.max()])
        axes[0].matshow(pupil_amplitude, vmin=pupil_amplitude_limits[0], vmax=pupil_amplitude_limits[1])
        axes[1].matshow(pupil_phase, vmin=pupil_phase_limits[0], vmax=pupil_phase_limits[1])
        
        axes[0].spines[['right', 'top', "left", "bottom"]].set_visible(False)
        axes[1].spines[['right', 'top', "left", "bottom"]].set_visible(False)
        axes[0].set_xticks([])
        axes[1].set_xticks([])
        axes[0].set_yticks([])
        axes[1].set_yticks([])


    axes_pupil_amplitude[0,0].set_xlabel("Amplitude")
    axes_pupil_amplitude[0,1].set_xlabel("Phase")
    axes_pupil_amplitude[0,1].xaxis.set_label_position('top') 
    axes_pupil_amplitude[0,0].xaxis.set_label_position('top') 
    axes_pupil_amplitude[0,0].set_ylabel(labels[0])
    axes_pupil_amplitude[1,0].set_ylabel(labels[1])

    
    zernike_coefficients_list = []
    for label, algorithm_result in zip(labels, algorithm_results):
        imaging_system = algorithm_result.imaging_system
        pupil = algorithm_result.pupil

        recovered_zernike_coefficients = decompose_zernike_pupil(imaging_system=imaging_system, pupil=pupil, 
                                                                max_j=max_j)
        zernike_coefficients_list.append(recovered_zernike_coefficients)

        defocus_coefficient = recovered_zernike_coefficients[4]
        frequency = imaging_system.frequency
        numerical_aperture = imaging_system.cutoff_frequency/frequency
        defocus_distance = defocus_distance_from_zernike_coefficient(defocus_coefficient, numerical_aperture, frequency)
    
        print(f"Defocus ({label}): {defocus_distance*1e6} um from {defocus_coefficient}")
    print(f"Spherical aberration change ({labels[1]}-{labels[0]}):", zernike_coefficients_list[1][11]-zernike_coefficients_list[0][11])

    plot_zernike_coefficients_comparative(axes_coefficients, zernike_coefficients_list, colors=["b","r"], labels=labels)
    if (zernike_coefficient_limits[0] is not None) and (zernike_coefficient_limits[1] is not None):
        axes_coefficients.set_ylim(bottom=zernike_coefficient_limits[0], top=zernike_coefficient_limits[1])
            

    return fig