from enum import Enum

class LED_infos(object):
    def __init__(self, array_to_object_distance, LED_pitch, wavelength, LED_array_size,
                 LED_offset, center_indices, exposure_times):
        self.array_to_object_distance = array_to_object_distance # m
        self.LED_pitch = LED_pitch # m
        self.wavelength = wavelength # m
        self.LED_array_size = LED_array_size # [x, y]
        self.LED_offset = LED_offset # m, [x, y]
        self.center_indices = center_indices # [x,y]
        self.exposure_times = exposure_times # 2D array of exposure times of size (LED_array_size + 1)^2 where indexation correspondes to LED_indices

class Camera(object):
    def __init__(self, camera_pixel_size, raw_image_size, bit_depth):
        self.camera_pixel_size = camera_pixel_size # m
        self.raw_image_size = raw_image_size # number of pixels in [x, y]
        self.bit_depth = bit_depth

class Lens_type(Enum):
    INFINITY_CORRECTED = 1
    TELECENTRIC = 2

class Lens(object):
    def __init__(
            self, 
            NA, 
            magnification, 
            diameter,
            focal_length,
            working_distance,
            depth_of_field, 
            lens_type: Lens_type
        ):
        self.NA = NA
        self.magnification = magnification
        self.diameter = diameter # m
        self.focal_length = focal_length # m
        self.working_distance = working_distance # m
        self.depth_of_field = depth_of_field # m
        self.lens_type: Lens_type = lens_type

def get_object_to_lens_distance(lens: Lens):
    if lens.lens_type == Lens_type.INFINITY_CORRECTED:
        return lens.focal_length
    if lens.lens_type == Lens_type.TELECENTRIC:
        return (1+1/lens.magnification)*lens.focal_length


class Setup_parameters(object):
    def __init__(self, lens: Lens, camera: Camera, LED_info: LED_infos):
        self.lens: Lens = lens
        self.camera: Camera = camera
        self.LED_info: LED_infos = LED_info

        




