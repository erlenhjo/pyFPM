from pyFPM.setup.Setup_parameters import Setup_parameters
from pyFPM.setup.Imaging_system import calculate_patch_start_and_end

from dataclasses import dataclass
import numpy as np

@dataclass
class Rawdata:
    LED_indices: list
    images: np.ndarray
    background_image: np.ndarray|None
             

class Preprocessed_data:
    def __init__(self, rawdata: Rawdata, setup_parameters: Setup_parameters,
                noise_reduction_regions, threshold_value):
        center_indices = setup_parameters.LED_info.center_indices
        LED_indices = rawdata.LED_indices
        float_type = setup_parameters.camera.float_type
        images = rawdata.images
        background_image = rawdata.background_image
        exposure_times = setup_parameters.LED_info.exposure_times

        if exposure_times is not None:
            images, background_image = _compensate_for_exposure_times(
                images = images,
                background_image = background_image,
                center_indices = center_indices,
                LED_indices = LED_indices,
                exposure_times = exposure_times
                )
        if noise_reduction_regions is not None:
            images = subtract_region_mean(images=images, threshold_value=threshold_value, noise_reduction_regions=noise_reduction_regions)
        
        self.amplitude_images = np.sqrt(images).astype(float_type)   # take amplitude and set float type
        self.LED_indices = LED_indices

@dataclass
class Simulated_data:
    LED_indices: list
    amplitude_images: np.ndarray

class Data_patch:
    def __init__(self, data: Preprocessed_data|Simulated_data, patch_offset, patch_size, binned_image_size):

        patch_start, patch_end = calculate_patch_start_and_end(
            image_size = binned_image_size,
            patch_offset = patch_offset,
            patch_size = patch_size
        )

        self.patch_start = patch_start
        self.patch_end = patch_end
        self.patch_offset = patch_offset
        self.patch_size = patch_size
        self.amplitude_images = data.amplitude_images[:, patch_start[1]:patch_end[1], patch_start[0]:patch_end[0]]
        self.LED_indices = data.LED_indices



def _compensate_for_exposure_times(images, background_image, center_indices, LED_indices, exposure_times):
    exposure_times = exposure_times/np.min(exposure_times)
    for n, [x_index, y_index] in enumerate(LED_indices):
        images[n] = images[n] / exposure_times[y_index, x_index]
    background_image = background_image/exposure_times[center_indices[1], center_indices[0]]
    
    return images, background_image


def subtract_region_mean(images: np.ndarray, threshold_value, noise_reduction_regions):
    prev_background = 0
    for n in range(images.shape[0]):
        image=images[n]
        background_mean_sum = 0
        for region_x, region_y, region_size_x, region_size_y in noise_reduction_regions:
            image_region = image[region_y:region_y+region_size_y, region_x:region_x+region_size_x]
            background_mean_sum += np.mean(image_region)

        image_background = background_mean_sum/len(noise_reduction_regions)
        if image_background > threshold_value:
            image_background = prev_background

        images[n] = images[n] - image_background
        prev_background = image_background
    images[images<0] = 0

    return images

