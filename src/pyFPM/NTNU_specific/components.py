from pyFPM.setup.Setup_parameters import Camera, Lens, Lens_type
from pyFPM.aberrations.dot_array.Dot_array import Dot_array

###### LED array ######
class LED_type(object):
    def __init__(self, wavelength, offset):
        self.wavelength = wavelength #m
        self.offset = offset #m
        
class LED_array(object):
    def __init__(self, LED_pitch, array_size, red: LED_type, green: LED_type, blue: LED_type):
        self.LED_pitch = LED_pitch #m
        self.array_size = array_size
        self.red = red
        self.green = green
        self.blue = blue

# offsets are relative green LEDs
MAIN_LED_ARRAY = LED_array(
    LED_pitch = 6e-3,
    array_size = [32, 32],
    red = LED_type(wavelength = 625e-9, offset = [0, -700e-6]),
    green = LED_type(wavelength = 520e-9, offset = [0, 0]),
    blue = LED_type(wavelength = 470e-9, offset = [50e-6, 100e-6])
)

###### Cameras ######

HAMAMATSU_C11440_42U30 = Camera(
    camera_pixel_size = 6.5e-6,
    raw_image_size = [2048, 2048],
    bit_depth = int(2**16 - 1)
    )

UI3580CP_REV2 = Camera(
    camera_pixel_size = 2.2e-6,
    raw_image_size = [2560, 1920],
    bit_depth = int(2**8-1)
)

###### Lenses ######

INFINITYCORRECTED_2X = Lens(
    NA = 0.055,
    magnification = 2,
    diameter = None,
    focal_length = 100e-3,
    working_distance = 34e-3,
    depth_of_field = 91e-6,
    lens_type = Lens_type.INFINITY_CORRECTED
)

TELECENTRIC_3X = Lens(
    NA = 0.09,
    magnification = 3,
    diameter = None,
    focal_length = 58.51e-3,
    working_distance = 77e-3,
    depth_of_field = 34e-6,
    lens_type = Lens_type.TELECENTRIC
)

###### Aberration target ######

EO_DOT_ARRAY = Dot_array(
    spacing = 125e-6,
    spacing_tolerance = 2e-6,
    diameter = 62.5e-6,
    diameter_tolerance = 2e-6  
)
