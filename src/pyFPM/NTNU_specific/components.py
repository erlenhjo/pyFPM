import numpy as np

from pyFPM.setup.Setup_parameters import Camera, Lens
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
    float_type = np.float64  
    )

IDS_UI3580CP_REV2 = Camera(
    camera_pixel_size = 2.2e-6,
    raw_image_size = [2560, 1920],
    float_type = np.float64
)

IDS_U3_31J0CP_REV_2_2 = Camera(
    camera_pixel_size = 2.74e-6,
    raw_image_size = [2848, 2844],
    float_type = np.float64
)

###### Lenses ######

INFINITYCORRECTED_2X = Lens(
    NA = 0.055,
    magnification = 2,
    effectiv_object_to_aperture_distance = np.inf,
    focal_length = 100e-3,
    working_distance = 34e-3,
    depth_of_field = 91e-6,
    max_FoV_sensor = 11e-3
)

INFINITYCORRECTED_10X = Lens(
    NA = 0.28,
    magnification = 10,
    effectiv_object_to_aperture_distance = np.inf,
    focal_length = 20e-3,
    working_distance = 34e-3,
    depth_of_field = 3.5e-6,
    max_FoV_sensor = 11e-3
)

INFINITYCORRECTED_50X = Lens(
    NA = 0.55,
    magnification = 50,
    effectiv_object_to_aperture_distance = np.inf,
    focal_length = 4e-3,
    working_distance = 13e-3,
    depth_of_field = 0.9e-6,
    max_FoV_sensor = 11e-3
)

TELECENTRIC_3X = Lens(
    NA = 0.09,
    magnification = 3,
    effectiv_object_to_aperture_distance = np.inf,
    focal_length = 58.51e-3,
    working_distance = 77e-3,
    depth_of_field = 34e-6,
    max_FoV_sensor = 11e-3
)

COMPACT_2X = Lens(
    NA = 0.06,
    magnification = 2,
    effectiv_object_to_aperture_distance = 60.33e-3*(1 + 1/2),
    focal_length = 60.33e-3,
    working_distance = 92e-3,
    depth_of_field = 76e-6,
    max_FoV_sensor = 11e-3
)

COMPACT_2X_CALIBRATED = Lens(
    NA = 0.06,
    magnification = 2,
    effectiv_object_to_aperture_distance = 1/9.35,
    focal_length = 60.33e-3,
    working_distance = 92e-3,
    depth_of_field = 76e-6,
    max_FoV_sensor = 11e-3
)

FUJINON_MINWD_MAXNA = Lens(
    NA = 0.044,
    magnification = 0.1766,
    effectiv_object_to_aperture_distance = 1/10.49,
    focal_length = 16e-3,
    working_distance = 100e-3, #???
    depth_of_field = None, # large
    max_FoV_sensor = None 
)


double_convex_focal_length = 36e-3
double_convex_extension_length = (100 - 1 + 17.526) * 1e-3 
double_convex_clear_aperture = 5.2e-3
double_convex_working_distance = 1/(1/double_convex_focal_length - 1/double_convex_extension_length)
double_convex_numerical_aperture = (double_convex_clear_aperture/2)/double_convex_working_distance
double_convex_magnification = double_convex_extension_length/double_convex_working_distance

# print(double_convex_magnification)
# print(double_convex_working_distance)
# print(double_convex_extension_length)
# print(double_convex_numerical_aperture)

DOUBLE_CONVEX = Lens(
    NA = double_convex_numerical_aperture,
    magnification = double_convex_magnification,
    effectiv_object_to_aperture_distance = double_convex_working_distance,
    focal_length = double_convex_focal_length,
    working_distance = double_convex_working_distance,
    depth_of_field = None,
    max_FoV_sensor = None
)

###### Aberration target ######

EO_DOT_ARRAY = Dot_array(
    spacing = 125e-6,
    spacing_tolerance = 2e-6,
    diameter = 62.5e-6,
    diameter_tolerance = 2e-6  
)
