import os
import numpy as np

from pyFPM.setup.Setup_parameters import Setup_parameters, Lens, Camera, LED_infos
from .components import LED_array


def setup_parameters_from_file(datadirpath, lens: Lens, camera: Camera, 
                                LED_array: LED_array, array_to_object_distance):

    BF_exposure_time, DF_exposure_time, \
        BF_exposure_radius, wavelength, \
            LED_offset, center_indices = read_parameters_from_file(datadirpath, LED_array)
    
    exposure_times = calculate_exposure_times(center_indices, BF_exposure_radius, BF_exposure_time, DF_exposure_time, LED_array.array_size)

    LED_info: LED_infos = LED_infos(
            array_to_object_distance = array_to_object_distance, 
            LED_pitch = LED_array.LED_pitch, 
            wavelength = wavelength, 
            LED_array_size = LED_array.array_size,
            LED_offset = LED_offset, 
            center_indices = center_indices, 
            exposure_times = exposure_times
        )

    setup_parameters: Setup_parameters = Setup_parameters(
        lens = lens,
        camera = camera,
        LED_info = LED_info
    )

    return setup_parameters


def find_and_interpret(data: list[str], parameter) -> str:
    for line in data:
        if line[:len(parameter)] != parameter:
            continue
        else:
            value = line.split(":")[1]
            value = value.strip(" ")
            return value

    raise Exception(f"Setup parameter {parameter} not found")


def read_parameters_from_file(datadirpath, LED_array: LED_array):
    with open(os.path.join(datadirpath,"setup.txt")) as file:
        data = file.read()
        data = data.split("\n")

    # Exposure times
    BF_exposure_time = float(find_and_interpret(data, "Exposure time 1"))
    if find_and_interpret(data, "Multiple exposure") == "TRUE":
        DF_exposure_time = float(find_and_interpret(data, "Exposure time 2"))
    else:
        DF_exposure_time = BF_exposure_time
    BF_exposure_radius = float(find_and_interpret(data, "Exposure 1 radius"))

    # LED color, wavelength and offset
    rgb = [int(val) for val in find_and_interpret(data, "RGB").split(",")]
    if rgb == [1,0,0]: # red
        wavelength = LED_array.red.wavelength
        LED_offset = LED_array.red.offset
    elif rgb == [0,1,0]: # green
        wavelength = LED_array.green.wavelength
        LED_offset = LED_array.green.offset
    elif rgb == [0,0,1]: # blue
        wavelength = LED_array.blue.wavelength
        LED_offset = LED_array.blue.offset
    else:
        raise Exception(f"Unsupported rgb: {rgb}")

    # Center LED
    center: str = find_and_interpret(data,"Centre")
    center_indices = [int(n) for n in center.split(",")]
    

    return BF_exposure_time, DF_exposure_time, BF_exposure_radius, \
            wavelength, LED_offset, center_indices

def calculate_exposure_times(center_indices, BF_exposure_radius, BF_exposure_time, DF_exposure_time, array_size):
    x_size = array_size[0]
    y_size = array_size[1]

    exposure_times = np.zeros(shape = (y_size + 1, x_size + 1))

    for y_index in range(y_size + 1):
        for x_index in range(x_size + 1):
            if (x_index - center_indices[0])**2 + (y_index - center_indices[1])**2 > (BF_exposure_radius + 1/2)**2:
                exposure_times[y_index, x_index] = DF_exposure_time
            else:
                exposure_times[y_index, x_index] = BF_exposure_time

    return exposure_times