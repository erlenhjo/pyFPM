import numpy as np
import matplotlib.pyplot as plt

from pyFPM.setup.Setup_parameters import Setup_parameters
from pyFPM.setup.Imaging_system import Imaging_system

class Illumination_pattern(object):
    def __init__(self, LED_indices, max_array_size, circle: bool,
                 imaging_system: Imaging_system, setup_parameters: Setup_parameters):
        LED_array_size = setup_parameters.LED_info.LED_array_size
        center_indices = setup_parameters.LED_info.center_indices
        LED_frequencies_x = imaging_system.LED_shifts_x_Fresnel * imaging_system.df_x
        LED_frequencies_y = imaging_system.LED_shifts_y_Fresnel * imaging_system.df_y
        cutoff_frequency = imaging_system.cutoff_frequency

        if not circle:
            avaliable_LEDs = determine_available_LEDs(LED_indices=LED_indices, LED_array_size=LED_array_size, 
                                                    center_indices = center_indices, max_array_size = max_array_size)
        else:
            avaliable_LEDs = determine_available_LEDs_circle(LED_indices=LED_indices, LED_array_size=LED_array_size, 
                                                            center_indices = center_indices, max_array_size = max_array_size)
        

        self.relative_NAs = calculate_relative_NA(
             LED_frequencies_x = LED_frequencies_x,
             LED_frequencies_y = LED_frequencies_y,
             cutoff_frequency = cutoff_frequency
        )

        # self.update_order, self.update_order_matrix \
        #     = spiral_indices(LED_indices = LED_indices, center_indices=center_indices, 
        #                      LED_array_size=LED_array_size, avaliable_LEDs=avaliable_LEDs)
        
        self.update_order, self.update_order_matrix \
            = low_NA_first_indices(LED_indices = LED_indices, center_indices=center_indices, 
                                   LED_array_size=LED_array_size, avaliable_LEDs=avaliable_LEDs,
                                   relative_LED_frequencies = self.relative_NAs)
        

def calculate_relative_NA(LED_frequencies_x, LED_frequencies_y, cutoff_frequency):
    return np.sqrt(LED_frequencies_x**2 + LED_frequencies_y**2) / cutoff_frequency

def determine_available_LEDs(LED_indices, LED_array_size, center_indices, 
                             max_array_size):
    available_LEDs = np.zeros(shape = (LED_array_size[1] + 2, LED_array_size[0] + 2), dtype = bool)
    if max_array_size is None:
        max_index_x = LED_array_size[0]
        max_index_y = LED_array_size[1]
        min_index_x = 0
        min_index_y = 0
    else:
        max_index_x = center_indices[0]+max_array_size//2
        max_index_y = center_indices[1]+max_array_size//2
        min_index_x = center_indices[0]-max_array_size//2
        min_index_y = center_indices[1]-max_array_size//2

    for x, y in LED_indices:
        if (min_index_x <= x) and (max_index_x >= x) and (min_index_y <= y) and (max_index_y >= y):
            available_LEDs[y,x] = True

    return available_LEDs

def determine_available_LEDs_circle(LED_indices, LED_array_size, center_indices, 
                             max_array_size):
    available_LEDs = np.zeros(shape = (LED_array_size[1] + 2, LED_array_size[0] + 2), dtype = bool)

    radius = max_array_size/2
    center_x = center_indices[0]
    center_y = center_indices[1]
    for x, y in LED_indices:
        if ((x-center_x)**2 + (y-center_y)**2 <= radius**2):
            available_LEDs[y,x] = True
    return available_LEDs


def spiral_indices(LED_indices, center_indices, LED_array_size, avaliable_LEDs):
    center_x_index = center_indices[0]
    center_y_index = center_indices[1]

    order_matrix = np.zeros(shape=(LED_array_size[1]+2, LED_array_size[0]+2), dtype = int)
    order_list = np.empty(shape=len(LED_indices), dtype = int)


    x_index = center_x_index
    y_index = center_y_index
    order_matrix[y_index,x_index] = 0  
    update_index = 1  
    direction = 0 #when mod4 = 0 down, 1 left, 2 up, 3 right, 4 up etc
    while (0 < x_index) and (x_index < LED_array_size[1]+1) and (0 < y_index) and (y_index < LED_array_size[0]+1):
        for n in range(int(np.ceil((direction)//2+1))):
            if direction % 4 == 0:
                y_index += 1
            elif direction % 4 == 1:
                x_index -= 1
            elif direction % 4 == 2:
                y_index -= 1
            elif direction % 4 == 3:
                x_index += 1

            if avaliable_LEDs[y_index, x_index]:
                order_matrix[y_index, x_index] = update_index
                update_index += 1

        direction += 1


    for n, (x, y) in enumerate(LED_indices):
        update_index = order_matrix[y,x]
        order_list[update_index] = n

    return order_list, order_matrix
    

def low_NA_first_indices(LED_indices, center_indices, LED_array_size, avaliable_LEDs, relative_LED_frequencies):
    order_matrix = np.zeros(shape=(LED_array_size[1]+2, LED_array_size[0]+2), dtype = int)
    order_list = np.empty(shape=len(LED_indices), dtype = int)

    numerical_apertures = []

    for n, (x, y) in enumerate(LED_indices):
        numerical_apertures.append(relative_LED_frequencies[y,x])

    order_list = np.array(numerical_apertures).argsort()
    for n, (x, y) in enumerate(LED_indices):
        order_matrix[y,x] = np.argwhere(order_list == n)
    
    return order_list, order_matrix
    