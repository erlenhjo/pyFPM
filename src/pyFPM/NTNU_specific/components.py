from pyFPM.setup.Setup_parameters import Camera, Lens, Lens_type


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


HAMAMATSU = Camera(
    camera_pixel_size = 6.5e-6,
    raw_image_size = [2048, 2048],
    bit_depth = int(2**16 - 1)
    )

# offsets are relative green LEDs
MAIN_LED_ARRAY = LED_array(
    LED_pitch = 6e-3,
    array_size = [32, 32],
    red = LED_type(wavelength = 625e-9, offset = [0, -700e-6]),
    green = LED_type(wavelength = 520e-9, offset = [0, 0]),
    blue = LED_type(wavelength = 470e-9, offset = [50e-6, 100e-6])
)

INFINITYCORRECTED_2X = Lens(
    NA = 0.055,
    magnification = 2,
    diameter = None,
    focal_length = 100e-3,
    working_distance = 34e-3,
    depth_of_field = 91e-6,
    lens_type = Lens_type.INFINITY_CORRECTED
)

