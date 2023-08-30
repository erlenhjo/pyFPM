import os
from pyFPM.setup.components.led_arrays import LED_array

class Setup_parameters(object):
    def __init__(self, datadirpath, lens, camera, LED_array: LED_array, z_LED):
        self.lens = lens
        self.camera = camera
        self.z_LED = z_LED
        self.LED_array = LED_array
        #self.rotation = rotation
        #self.dark_image = "dark_image" ???
        #setup_params.raw_image_pixel_size = ccd_pixel_size / magnification;

    
        self.read_parameters_from_file(datadirpath)


    def read_parameters_from_file(self, datadirpath):
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
            self.wavelength = self.LED_array.red.wavelength
            self.offset = self.LED_array.red.offset
        elif rgb == [0,1,0]: # green
            self.wavelength = self.LED_array.green.wavelength
            self.offset = self.LED_array.green.offset
        elif rgb == [0,0,1]: # blue
            self.wavelength = self.LED_array.blue.wavelength
            self.offset = self.LED_array.blue.offset
        else:
            raise Exception(f"Unsupported rgb: {rgb}")

        # Center LED
        self.center_index = [int(n) for n in self.find_and_interpret(data,"Centre").split(",")]

        # LED array: shape and size
        shape = self.find_and_interpret(data,"LED shape")
        radius_width = float(self.find_and_interpret(data, "Radius/width"))
        if shape == "Circular":
            #file specifies radius
            self.circular = True
            self.radius = radius_width + 0.5; # +0.5 for smoother circle?
            self.arraysize = 2*self.radius +1
        elif shape == "Square":
            #file specifies width
            self.circular = False
            self.arraysize = radius_width
            self.radius = radius_width / 2
        else: 
            raise Exception("Undefined LED shape")

        # Image format
        self.image_format = self.find_and_interpret(data, "Image format")

    def find_and_interpret(self, data, parameter):
        for line in data:
            if line[:len(parameter)] != parameter:
                continue
            else:
                value = line.split(":")[1]
                value = value.strip(" ")
                return value

        raise Exception(f"Setup parameter {parameter} not found")

