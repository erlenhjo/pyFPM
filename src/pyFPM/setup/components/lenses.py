from enum import Enum

class Lens_type(Enum):
    INFINITY_CORRECTED = 1
    TELECENTRIC = 2

class Lens(object):
    def __init__(self, NA, magnification, infinity_corrected):
        self.NA = NA
        self.magnification = magnification
        self.infinity_corrected = infinity_corrected

INFINITYCORRECTED_2X = Lens(
    NA=0.055,
    magnification = 2,
    lens_type = Lens_type.INFINITY_CORRECTED
)