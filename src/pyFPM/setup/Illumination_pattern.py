import numpy as np
import matplotlib.pyplot as plt

from pyFPM.setup.Setup_parameters import Setup_parameters
from pyFPM.setup.Imaging_system import Imaging_system

class Illumination_pattern(object):
    def __init__(self, LED_indices, imaging_system: Imaging_system, setup_parameters: Setup_parameters):
        LED_array_size = setup_parameters.LED_info.LED_array_size
        center_indices = setup_parameters.LED_info.center_indices
        LED_frequencies_x = imaging_system.LED_frequencies_x
        LED_frequencies_y = imaging_system.LED_frequencies_y
        cutoff_frequency = imaging_system.cutoff_frequency
        

        self.relative_NAs = calculate_relative_NA(
            LED_frequencies_x = LED_frequencies_x,
            LED_frequencies_y = LED_frequencies_y,
            cutoff_frequency = cutoff_frequency
        )

        self.update_order, _ = spiral_indices(LED_indices = LED_indices, 
                                              center_indices=center_indices,
                                              LED_array_size=LED_array_size)




def calculate_relative_NA(LED_frequencies_x, LED_frequencies_y, cutoff_frequency):
    return np.sqrt(LED_frequencies_x**2 + LED_frequencies_y**2) / cutoff_frequency

def spiral_indices(LED_indices, center_indices, LED_array_size):
    center_x_index = center_indices[0]
    center_y_index = center_indices[1]

    order_matrix = np.zeros(shape=(LED_array_size[1]+1, LED_array_size[0]+1), dtype = int)
    order_list = np.empty(shape=len(LED_indices), dtype = int)


    x_index = center_x_index
    y_index = center_y_index
    order_matrix[y_index,x_index] = 0  
    update_index = 1  
    direction = 0 #when mod4 = 0 up, 1 left, 2 down, 3 right, 4 up etc
    while (0 < x_index) and (x_index < 33) and (0 < y_index) and (y_index < 33):
        for n in range(int(np.ceil((direction)//2+1))):
            if direction % 4 == 0:
                y_index -= 1
            elif direction % 4 == 1:
                x_index -= 1
            elif direction % 4 == 2:
                y_index += 1
            elif direction % 4 == 3:
                x_index += 1

            order_matrix[y_index, x_index] = update_index
            update_index += 1

        direction += 1

    for n, indices in enumerate(LED_indices):
        x = indices[0]
        y = indices[1]

        update_index = order_matrix[y,x]
        order_list[update_index] = n

    return order_list, order_matrix
    
    
    