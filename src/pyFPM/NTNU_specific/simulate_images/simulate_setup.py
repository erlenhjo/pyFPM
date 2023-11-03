from pyFPM.setup.Setup_parameters import Lens, Camera, LED_infos, Setup_parameters
from pyFPM.NTNU_specific.components import LED_array

import numpy as np

def simulate_setup_parameters(lens: Lens, camera: Camera, 
                              LED_array: LED_array, array_to_object_distance):

    x_size = LED_array.array_size[0]
    y_size = LED_array.array_size[1]

    exposure_times = np.zeros(shape = (y_size + 1, x_size + 1))

    # assume green LED
    wavelength = LED_array.green.wavelength
    LED_offset = LED_array.green.offset
    center_indices = [16,16]    

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