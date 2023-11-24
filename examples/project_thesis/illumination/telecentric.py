import matplotlib.pyplot as plt
from pyFPM.NTNU_specific.components import TELECENTRIC_3X

from general_functions import illustrate_illumination_from_setup, illustrate_illumination_from_simulation

lens = TELECENTRIC_3X
array_size = 7

def simulate_both():
    illustrate_illumination_from_simulation(lens, spherical=True, Fresnel=True, z_LED=201e-3, arraysize=array_size)

def simulate_illumination():
    illustrate_illumination_from_simulation(lens, spherical=True, Fresnel=False, z_LED=201e-3, arraysize=array_size)

def experimental_reflections():
    datadirpath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\dotarray_telecentric3x_dark_no_object"
    illustrate_illumination_from_setup(datadirpath, lens, array_size)

def experimental_proper():
    datadirpath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\telecentric_3x_illumination"
    illustrate_illumination_from_setup(datadirpath, lens, array_size)

if __name__ == "__main__": 
    simulate_illumination()
    simulate_both
    experimental_reflections()
    experimental_proper()
    plt.show()