import numpy as np
from pyFPM.NTNU_specific.components import (MAIN_LED_ARRAY, IDS_U3_31J0CP_REV_2_2, 
                                            COMPACT_2X, TELECENTRIC_3X, 
                                            INFINITYCORRECTED_2X, INFINITYCORRECTED_10X, 
                                            INFINITYCORRECTED_50X, FUJINON_MINWD_MAXNA)



def calculate_required_detector_pixel_size(magnification, wavelength, numerical_aperture):
    return magnification * wavelength / (2 * numerical_aperture)

def calcualate_necessary_pixel_scaling(magnification, wavelength, detector_pixel_size, synthetic_NA):
    return np.ceil(4 * detector_pixel_size * synthetic_NA / (wavelength * magnification))


detector_pixel_size = IDS_U3_31J0CP_REV_2_2.camera_pixel_size
wavelength = MAIN_LED_ARRAY.green.wavelength
lenses = [COMPACT_2X, 
          TELECENTRIC_3X, 
          INFINITYCORRECTED_10X, 
          INFINITYCORRECTED_50X,
          FUJINON_MINWD_MAXNA]


for lens in lenses:
    magnification = lens.magnification
    numerical_aperture = lens.NA

    required_pixel_size = calculate_required_detector_pixel_size(
        magnification = magnification,
        wavelength = wavelength,
        numerical_aperture = numerical_aperture
    )

    print(required_pixel_size, required_pixel_size / detector_pixel_size)