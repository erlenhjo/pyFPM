import numpy as np

from pyFPM.setup.Setup_parameters import Setup_parameters
from pyFPM.setup.Imaging_system import Imaging_system

class Illumination_pattern(object):
    def __init__(self, LED_indices, imaging_system: Imaging_system, setup_parameters: Setup_parameters):
        LED_array_size = setup_parameters.LED_info.LED_array_size
        center_indices = setup_parameters.LED_info.center_indices
        LED_frequencies_x = imaging_system.LED_frequencies_x
        LED_frequencies_y = imaging_system.LED_frequencies_y
        cutoff_frequency = imaging_system.cutoff_frequency

        available_LEDs = determine_available_LEDs(
            LED_indices = LED_indices, 
            LED_array_size = LED_array_size
            )
        
        relative_NAs = calculate_relative_NA(
            LED_frequencies_x = LED_frequencies_x,
            LED_frequencies_y = LED_frequencies_y,
            cutoff_frequency = cutoff_frequency
        )

        BF_edge = determine_BF_edge(
            relative_NAs = relative_NAs
        )

        self.available_LEDs = available_LEDs
        self.BF_edge = BF_edge

        self.update_order = matlab_indices(LED_indices = LED_indices, BF_edge = BF_edge)



def determine_available_LEDs(LED_indices, LED_array_size):
    available_LEDs = np.zeros(shape = (LED_array_size[1] + 1, LED_array_size[0] + 1), dtype = bool)   # plus 1 in case array indices are one indexed
    
    for x, y in LED_indices:
        available_LEDs[y,x] = True

    return available_LEDs

def calculate_relative_NA(LED_frequencies_x, LED_frequencies_y, cutoff_frequency):
    return np.sqrt(LED_frequencies_x**2 + LED_frequencies_y**2) / cutoff_frequency

def determine_BF_edge(relative_NAs):
    lower_NA_limit = 0.9
    upper_NA_limit = 1.5
    return (relative_NAs > lower_NA_limit) * (relative_NAs < upper_NA_limit)

def indices_NA_first(LED_indices, center):
    raise "Not implemented NA first ordering"


def matlab_indices(LED_indices, BF_edge):
    # this follows a spiral from the center and out, starting up and then anti-clockwise
    matlab_order = np.array([41,50,49,40,31,32,33,42,51,60,59,58,57,48,39,30,21,22,23,24,25,34,43,52,61,\
                             70,69,68,67,66,65,56,47,38,29,20,11,12,13,14,15,16,17,26,35,44,53,62,71,80,79,\
                             78,77,76,75,74,73,64,55,46,37,28,19,10,1,2,3,4,5,6,7,8,9,18,27,36,45,54,63,72,81])

    index_matrix = np.zeros(shape=(33,33), dtype = int)
    ordered_matrix = np.zeros(shape=(33,33), dtype = int)
    ordered_list = np.empty(shape=len(LED_indices), dtype = int)

    nr = 1
    for y_index in range(20,11,-1):
        for x_index in range(12, 21):
            index_matrix[y_index, x_index] = nr
            nr += 1

    for n, indices in enumerate(LED_indices):
        x = indices[0]
        y = indices[1]

        update_index = np.argwhere( matlab_order == index_matrix[y,x])

        ordered_matrix[y,x] = update_index
        ordered_list[update_index] = n

    return ordered_list


