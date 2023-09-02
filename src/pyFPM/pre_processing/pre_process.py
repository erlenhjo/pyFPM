import numpy as np

from pyFPM.setup.Imaging_system import Imaging_system
from pyFPM.setup.Rawdata import Rawdata

def pre_process_images(rawdata: Rawdata, remove_background: bool, threshold_value, imaging_system: Imaging_system):
    LED_indices = rawdata.LED_indices
    images = rawdata.images
    background_image = rawdata.background_image
    BF_exposure_time = imaging_system.setup_parameters.BF_exposure_time
    DF_exposure_time = imaging_system.setup_parameters.DF_exposure_time
    BF_exposure_radius = imaging_system.setup_parameters.BF_exposure_radius
    center_indices = imaging_system.setup_parameters.center_indices
    bit_depth = imaging_system.setup_parameters.camera.bit_depth

    images, background_image = normalize_images(
        images = images, 
        background_image = background_image,
        bit_depth = bit_depth
        )

    images = compensate_for_exposure_times(
        images = images,
        BF_exposure_time = BF_exposure_time,
        DF_exposure_time = DF_exposure_time,
        BF_exposure_radius=BF_exposure_radius,
        LED_indices=LED_indices,
        center_indices=center_indices
        )
    

    if remove_background:
        subtract_background_image()

    if threshold_value > 0:
        threshold()

    return images




def normalize_images(images, background_image, bit_depth):
    return images/bit_depth, background_image/bit_depth


def compensate_for_exposure_times(images, BF_exposure_time, DF_exposure_time, BF_exposure_radius, LED_indices, center_indices):
    for n, [x_index, y_index] in enumerate(LED_indices):
        if (x_index - center_indices[0])**2 + (y_index - center_indices[1])**2 > BF_exposure_radius**2:
            images[n] = images[n]*BF_exposure_time/DF_exposure_time

    return images


def threshold(images: np.ndarray, threshold_value):
    raise "Not implemented thresholding"


def subtract_background_image():
    raise "Not implemented background removal"


def indices_NA_first(LED_indices, center):
    raise "Not implemented NA first ordering"