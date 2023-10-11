from pyFPM.setup.Imaging_system import Imaging_system, calculate_frequency_mesh_grids

import numpy as np

def get_defocused_pupil(imaging_system: Imaging_system, defocus):
        pupil = calculate_defocused_pupil(
            defocus = defocus,
            pixel_size = imaging_system.raw_image_pixel_size,
            frequency = imaging_system.frequency,
            image_region_size = imaging_system.patch_size
        )
        return pupil


def calculate_defocused_pupil(defocus, pixel_size, frequency, image_region_size):
    fx_mesh, fy_mesh = calculate_frequency_mesh_grids(pixel_size=pixel_size, image_region_size=image_region_size)
    fz_mesh = np.emath.sqrt(frequency**2 - fx_mesh**2 - fy_mesh**2)

    return np.exp(1j*2*np.pi*defocus*np.real(fz_mesh)) * np.exp(-(abs(defocus)*2*np.pi*abs(np.imag(fz_mesh))))