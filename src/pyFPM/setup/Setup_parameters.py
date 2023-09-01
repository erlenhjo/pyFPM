import os
from enum import Enum

from pyFPM.setup.components.led_arrays import LED_array
from pyFPM.setup.components.cameras import Camera
from pyFPM.setup.components.lenses import Lens
from pyFPM.setup.components.slides import Slide

class LED_patterns(Enum):
    SQUARE = 0
    CIRCULAR = 1

class Setup_parameters(object):
    def __init__(self, datadirpath, lens: Lens, camera: Camera, slide: Slide, LED_array: LED_array, z_LED):
        self.lens: Lens = lens
        self.camera: Camera = camera
        self.slide: Slide = slide
        self.z_LED = z_LED
        self.LED_pitch = LED_array.LED_pitch
    
        self.read_parameters_from_file(datadirpath,LED_array)


    def read_parameters_from_file(self, datadirpath, LED_array: LED_array):
        with open(os.path.join(datadirpath,"setup.txt")) as file:
            data = file.read()
            data = data.split("\n")

        # Exposure times
        self.BF_exposure_time = self.find_and_interpret(data, "Exposure time 1")
        if self.find_and_interpret(data, "Multiple exposure") == "TRUE":
            self.DF_exposure_time = float(self.find_and_interpret(data, "Exposure time 2"))
        else:
            self.DF_exposure_time = self.BF_exposure_time
        self.BF_exposure_radius = self.find_and_interpret(data, "Exposure 1 radius");

        # LED color, wavelength and offset
        rgb = [int(val) for val in self.find_and_interpret(data, "RGB").split(",")]
        if rgb == [1,0,0]: # red
            self.wavelength = LED_array.red.wavelength
            self.LED_offset = LED_array.red.offset
        elif rgb == [0,1,0]: # green
            self.wavelength = LED_array.green.wavelength
            self.LED_offset = LED_array.green.offset
        elif rgb == [0,0,1]: # blue
            self.wavelength = LED_array.blue.wavelength
            self.LED_offset = LED_array.blue.offset
        else:
            raise Exception(f"Unsupported rgb: {rgb}")

        # Center LED
        self.center_index = [int(n) for n in self.find_and_interpret(data,"Centre").split(",")]

        # LED array: shape and size
        shape = self.find_and_interpret(data,"LED shape")
        radius_width = float(self.find_and_interpret(data, "Radius/width"))

        if shape == "Circle":
            #file specifies radius
            self.LED_pattern = LED_patterns.CIRCULAR
            self.radius = radius_width + 0.5; # +0.5 for smoother circle?
            self.arraysize = int(2 * self.radius)
        elif shape == "Square":
            #file specifies width
            self.LED_pattern = LED_patterns.SQUARE
            self.arraysize = int(radius_width)
            self.radius = radius_width / 2
        else: 
            raise Exception("Undefined LED shape")

        # Image format
        self.image_format = self.find_and_interpret(data, "Image format")

    def find_and_interpret(self, data: list[str], parameter):
        for line in data:
            if line[:len(parameter)] != parameter:
                continue
            else:
                value = line.split(":")[1]
                value = value.strip(" ")
                return value

        raise Exception(f"Setup parameter {parameter} not found")

