from pyFPM.setup.Imaging_system import Imaging_system, calculate_frequency_mesh_grids
from pyFPM.aberrations.zernike_polynomials.fast_synthesis import evaluate_zernike_polynomial

import numpy as np
from skimage.restoration import unwrap_phase
from scipy.integrate import simpson

def get_zernike_pupil(imaging_system: Imaging_system, zernike_coefficients):
        pupil = calculate_zernike_pupil(
            zernike_coefficients = zernike_coefficients,
            pixel_size = imaging_system.raw_image_pixel_size,
            spatial_cutoff_frequency = imaging_system.cutoff_frequency,
            image_region_size = imaging_system.patch_size
        )
        return pupil


def calculate_zernike_pupil(zernike_coefficients, pixel_size, spatial_cutoff_frequency, image_region_size):
    fx_mesh, fy_mesh = calculate_frequency_mesh_grids(pixel_size=pixel_size, image_region_size=image_region_size)
    normalized_fx_mesh = fx_mesh/(spatial_cutoff_frequency)
    normalized_fy_mesh = fy_mesh/(spatial_cutoff_frequency)

    wavefront_error = np.zeros(shape=(image_region_size[1], image_region_size[0]))
    for j, zernike_coefficient in enumerate(zernike_coefficients):
        if j < 1 or (zernike_coefficient == 0):
            continue
        zernike_mode = evaluate_zernike_polynomial(normalized_fx_mesh, normalized_fy_mesh, j)
        wavefront_error += zernike_coefficient * zernike_mode
 
    pupil_phase = np.exp(1j * wavefront_error)

    return pupil_phase


def decompose_zernike_pupil(imaging_system: Imaging_system, pupil, max_j):
        pupil = calculate_decomposed_zernike_coefficients(
            pupil = pupil,
            max_j = max_j,
            pixel_size = imaging_system.raw_image_pixel_size,
            spatial_cutoff_frequency = imaging_system.cutoff_frequency,
            image_region_size = imaging_system.patch_size
        )
        return pupil

def calculate_decomposed_zernike_coefficients(pupil, max_j, pixel_size, spatial_cutoff_frequency, image_region_size):
    fx_mesh, fy_mesh = calculate_frequency_mesh_grids(pixel_size=pixel_size, image_region_size=image_region_size)
    normalized_fx_mesh = fx_mesh/(spatial_cutoff_frequency)
    normalized_fy_mesh = fy_mesh/(spatial_cutoff_frequency)
    dx = normalized_fx_mesh[0,1]-normalized_fx_mesh[0,0]
    dy = normalized_fy_mesh[1,0]-normalized_fy_mesh[0,0]

    wavefront_error = np.angle(pupil)
    wavefront_error = unwrap_phase(wavefront_error)

    zernike_coefficients = np.zeros(shape=max_j+1)
    unit_disk = normalized_fx_mesh**2 + normalized_fy_mesh**2 < 1
    for j in range(1, max_j+1):
        zernike_mode = evaluate_zernike_polynomial(normalized_fx_mesh, normalized_fy_mesh, j)
        integrand = wavefront_error * zernike_mode * unit_disk
        
        integral_x = simpson(y=integrand, dx=dx)
        integral_x_and_y = simpson(y=integral_x, dx=dy)
        zernike_coefficient = 1/np.pi * integral_x_and_y
        
        zernike_coefficients[j] = zernike_coefficient

    return zernike_coefficients