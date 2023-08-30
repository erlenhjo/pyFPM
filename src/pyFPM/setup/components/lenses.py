from enum import Enum

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

INFINITYCORRECTED_2X = Lens(
    NA=0.055,
    magnification = 2,
    diameter = None,
    focal_length = 100e-3,
    working_distance = 34e-3,
    depth_of_field = 91e-6,
    lens_type = Lens_type.INFINITY_CORRECTED
)