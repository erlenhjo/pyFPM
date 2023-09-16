import matplotlib.pyplot as plt
import numpy as np

import pyFPM
from setup_2x_hamamatsu import setup_2x_hamamatsu

#datadirpath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\20230825_USAFtarget"
#datadirpath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\EHJ290823_USAF1951_infcorr2x_hamamatsu"
datadirpath = r"c:\Users\erlen\Documents\GitHub\FPM\data\EHJ20230915_dotarray_2x_inf"

pixel_scale_factor = 4
patch_start = [949, 979] # [x, y]
patch_size = [64, 64] # [x, y]

setup_parameters, rawdata, preprocessed_data, imaging_system, illumination_pattern = setup_2x_hamamatsu(
    datadirpath = datadirpath,
    patch_start = patch_start,
    patch_size = patch_size,
    pixel_scale_factor = pixel_scale_factor
)

pyFPM.calibration.defocus_calibration.primitive_defocus_calibration(
    preprocessed_data = preprocessed_data,
    imaging_system = imaging_system,
    illumination_pattern = illumination_pattern
)


