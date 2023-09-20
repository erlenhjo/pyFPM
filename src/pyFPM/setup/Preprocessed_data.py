import numpy as np

from pyFPM.setup.Imaging_system import Setup_parameters
from pyFPM.setup.Rawdata import Rawdata

class Preprocessed_data(object):
    def __init__(self, rawdata: Rawdata, setup_parameters: Setup_parameters, remove_background: bool, threshold_value):
    
        LED_indices = rawdata.LED_indices
        images = rawdata.images
        background_image = rawdata.background_image
        exposure_times = setup_parameters.LED_info.exposure_times
        bit_depth = setup_parameters.camera.bit_depth

        images, background_image = normalize_images(
            images = images, 
            background_image = background_image,
            bit_depth = bit_depth
            )

        if exposure_times is not None:
            images = compensate_for_exposure_times(
                images = images,
                LED_indices=LED_indices,
                exposure_times=exposure_times
                )
        
        if remove_background:
            subtract_background_image()

        if threshold_value > 0:
            threshold()


        
        self.amplitude_images = np.sqrt(images)   # take amplitude
        self.LED_indices = LED_indices




def normalize_images(images, background_image, bit_depth):
    return images/bit_depth, background_image/bit_depth


def compensate_for_exposure_times(images, LED_indices, exposure_times):
    for n, [x_index, y_index] in enumerate(LED_indices):
        images[n] = images[n] / exposure_times[y_index, x_index]
    return images


def threshold(images: np.ndarray, threshold_value):
    raise "Not implemented thresholding"


def subtract_background_image():
    raise "Not implemented background removal"



