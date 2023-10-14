from pyFPM.setup.Imaging_system import Imaging_system, calculate_frequency_mesh_grids
from pyFPM.aberrations.zernike_polynomials.fast_synthesis import evaluate_zernike_polynomial

import numpy as np
import matplotlib.pyplot as plt

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