from enum import Enum

class LED_infos(object):
    def __init__(self, array_to_object_distance, LED_pitch, wavelength, LED_array_size,
                 LED_offset, center_indices, BF_exposure_radius, BF_exposure_time,
                 DF_exposure_time):
        self.array_to_object_distance = array_to_object_distance
        self.LED_pitch = LED_pitch
        self.wavelength = wavelength   
        self.LED_array_size = LED_array_size
        self.LED_offset = LED_offset
        self.center_indices = center_indices
        self.BF_exposure_radius = BF_exposure_radius
        self.BF_exposure_time = BF_exposure_time
        self.DF_exposure_time = DF_exposure_time

class Camera(object):
    def __init__(self, ccd_pixel_size, raw_image_size, bit_depth):
        self.ccd_pixel_size = ccd_pixel_size # m
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
        self.diameter = diameter
        self.focal_length = focal_length
        self.working_distance = working_distance
        self.depth_of_field = depth_of_field
        self.lens_type: Lens_type = lens_type

class Slide(object):
    def __init__(self, thickness, refractive_index):
        self.thickness = thickness #m
        self.refractive_index = refractive_index

class Setup_parameters(object):
    def __init__(self, lens: Lens, camera: Camera, LED_info: LED_infos, slide: Slide = None):
        self.lens: Lens = lens
        self.camera: Camera = camera
        self.LED_info: LED_infos = LED_info
        self.slide: Slide = slide
        




