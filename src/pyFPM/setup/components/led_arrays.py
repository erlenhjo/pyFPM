class LED_type(object):
    def __init__(self, wavelength, offset):
        self.wavelength = wavelength #m
        self.offset = offset #m
        
class LED_array(object):
    def __init__(self, LED_pitch, red: LED_type, green: LED_type, blue: LED_type):
        self.LED_pitch = LED_pitch #m
        self.red = red
        self.green = green
        self.blue = blue

# offsets are relative green LEDs
MAIN_LED_ARRAY = LED_array(
    LED_pitch = 6e-3,
    red = LED_type(wavelength = 625e-9, offset = [0, -700e-6]),
    green = LED_type(wavelength = 520e-9, offset = [0, 0]),
    blue = LED_type(wavelength = 470e-9, offset = [50e-6, 100e-6])
)