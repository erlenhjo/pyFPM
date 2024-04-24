from enum import Enum
import numpy as np

class LED_infos(object):
    def __init__(self, LED_pitch, wavelength, LED_array_size,
                 LED_offset, center_indices, exposure_times):
        self.LED_pitch = LED_pitch # m
        self.wavelength = wavelength # m
        self.LED_array_size = LED_array_size # [x, y]
        self.LED_offset = LED_offset # m, [x, y]
        self.center_indices = center_indices # [x,y]
        self.exposure_times = exposure_times # 2D array of exposure times of size (LED_array_size + 1)^2 where indexation correspondes to LED_indices

class Camera(object):
    def __init__(self, camera_pixel_size, raw_image_size, float_type):
        self.camera_pixel_size = camera_pixel_size # m
        self.raw_image_size = raw_image_size # number of pixels in [x, y]
        self.float_type = float_type # currently requires np.float64 due to casting with numba and fft

class Lens(object):
    def __init__(
            self, 
            NA, 
            magnification,
            effectiv_object_to_aperture_distance,
            focal_length,
            working_distance,
            depth_of_field, 
            max_FoV_sensor,
            
        ):
        self.NA = NA
        self.magnification = magnification
        self.effective_object_to_aperture_distance = effectiv_object_to_aperture_distance
        self.focal_length = focal_length # m
        self.working_distance = working_distance # m
        self.depth_of_field = depth_of_field # m
        
        if max_FoV_sensor is not None:
            self.max_FoV = max_FoV_sensor/magnification # m in diameter at the object plane
        else:
            self.max_FoV = None


class Setup_parameters(object):
    def __init__(self, lens: Lens, camera: Camera, LED_info: LED_infos, 
                 image_format: str = "", binning_factor = 1):
        self.lens: Lens = lens
        self.camera: Camera = camera
        self.LED_info: LED_infos = LED_info
        self.image_format: str = image_format
        self.binning_factor: int = binning_factor

        




