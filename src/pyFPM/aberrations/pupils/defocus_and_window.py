from pyFPM.setup.Imaging_system import Imaging_system, calculate_frequency_mesh_grids

import numpy as np


def defocus_zernike_coefficient(defocus, numerical_aperture, frequency):
    return (-np.pi * defocus * numerical_aperture**2 * frequency) / (2 * np.sqrt(3))

def defocus_distance_from_zernike_coefficient(defocus_coefficient, numerical_aperture, frequency):
    return ( -2 * np.sqrt(3) * defocus_coefficient)/(np.pi * numerical_aperture**2 * frequency) 


def defocus_distance_from_window(refractive_index, thickness):
    return (refractive_index - 1)/ refractive_index * thickness

def spherical_aberration_from_window_zernike_coefficient(refractive_index, thickness, numerical_aperture, frequency):
    N = (refractive_index**2 - 1) / (refractive_index**3)
    return - np.pi * numerical_aperture**4 * N * thickness * frequency / (6*np.sqrt(5))

def defocus_from_window_zernike_coefficient(refractive_index, thickness, numerical_aperture, frequency):
    defocus = defocus_distance_from_window(refractive_index = refractive_index, 
                                           thickness = thickness)
    return defocus_zernike_coefficient(defocus = defocus, 
                                       numerical_aperture = numerical_aperture, 
                                       frequency = frequency)


def get_defocused_pupil(imaging_system: Imaging_system, defocus):
        pupil = calculate_defocused_pupil(
            defocus = defocus,
            pixel_size = imaging_system.raw_object_pixel_size,
            frequency = imaging_system.frequency,
            image_region_size = imaging_system.patch_size
        )
        return pupil


def calculate_defocused_pupil(defocus, pixel_size, frequency, image_region_size):
    fx_mesh, fy_mesh = calculate_frequency_mesh_grids(pixel_size=pixel_size, image_region_size=image_region_size)

    pupil_phase = -np.pi*defocus*frequency*(fx_mesh**2+fy_mesh**2) / (frequency**2)
    return np.exp(1j*pupil_phase)



