from pyFPM.setup.Imaging_system import Setup_parameters

from dataclasses import dataclass
import numpy as np

@dataclass
class Rawdata:
    LED_indices: list
    images: np.ndarray
    background_image: np.ndarray|None
             

class Preprocessed_data:
    def __init__(self, rawdata: Rawdata, setup_parameters: Setup_parameters, remove_background: bool,
                noise_reduction_regions, threshold_value):
        center_indices = setup_parameters.LED_info.center_indices
        LED_indices = rawdata.LED_indices
        images = rawdata.images
        background_image = rawdata.background_image
        exposure_times = setup_parameters.LED_info.exposure_times
        bit_depth = setup_parameters.camera.bit_depth
        float_type = setup_parameters.camera.float_type

        images, background_image = _normalize_images(
            images = images, 
            background_image = background_image,
            bit_depth = bit_depth,
            float_type = float_type
            )

        if exposure_times is not None:
            images, background_image = _compensate_for_exposure_times(
                images = images,
                background_image = background_image,
                center_indices = center_indices,
                LED_indices = LED_indices,
                exposure_times = exposure_times
                )
            
        if remove_background:
            images = _subtract_background_image(images=images, background_image=background_image, 
                                                background_removal_regions = noise_reduction_regions)

        if threshold_value > 0 and remove_background:
            images = _threshold(images=images, threshold_value=threshold_value)
        elif threshold_value > 0:
            images = _alternative_threshold(images=images, threshold_value=threshold_value, noise_reduction_regions=noise_reduction_regions)
        


        self.amplitude_images = np.sqrt(images)   # take amplitude
        self.LED_indices = LED_indices

@dataclass
class Simulated_data:
    LED_indices: list
    amplitude_images: np.ndarray

class Data_patch:
    def __init__(self, data: Preprocessed_data|Simulated_data, patch_start, patch_size):
        x_start = patch_start[0]
        x_end = patch_start[0] + patch_size[0]
        y_start = patch_start[1]
        y_end = patch_start[1] + patch_size[1]

        self.patch_start = patch_start
        self.patch_size = patch_size
        self.amplitude_images = data.amplitude_images[:, y_start:y_end, x_start:x_end]
        self.LED_indices = data.LED_indices



def _normalize_images(images:np.ndarray, background_image:np.ndarray, bit_depth, float_type):
    return images.astype(float_type)/bit_depth, background_image.astype(float_type)/bit_depth


def _compensate_for_exposure_times(images, background_image, center_indices, LED_indices, exposure_times):
    exposure_times = exposure_times/np.min(exposure_times)
    for n, [x_index, y_index] in enumerate(LED_indices):
        images[n] = images[n] / exposure_times[y_index, x_index]
    background_image = background_image/exposure_times[center_indices[1], center_indices[0]]
    
    return images, background_image

def _subtract_background_image(images, background_image, background_removal_regions):
    region_size = 200
    if background_removal_regions is None:
        images = images-background_image
    else:
        for n in range(images.shape[0]):
            image=images[n]
            numerator = 0
            denominator = 0
            for region_x, region_y in background_removal_regions:
                image_region = image[region_y:region_y+region_size, region_x:region_x+region_size]
                background_region = background_image[region_y:region_y+region_size, region_x:region_x+region_size]
                numerator += np.sum(image_region*background_region)
                denominator += np.sum(image_region*image_region)
            alpha = numerator/denominator
            images[n] -= alpha*background_image

    images[images<0] = 0
    return images


def _threshold(images: np.ndarray, threshold_value):
    images[images<threshold_value]=0
    return images

def _alternative_threshold(images: np.ndarray, threshold_value, noise_reduction_regions):

    return images

