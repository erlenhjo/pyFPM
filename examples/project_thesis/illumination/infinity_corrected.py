import matplotlib.pyplot as plt
from pyFPM.NTNU_specific.components import INFINITYCORRECTED_2X

from general_functions import illustrate_illumination_from_setup, illustrate_illumination_from_simulation

lens = INFINITYCORRECTED_2X
array_size = 5


def simulate_both():
    illustrate_illumination_from_simulation(lens, spherical=True, Fresnel=True, z_LED=201e-3, arraysize=array_size)

def simulate_illumination():
    illustrate_illumination_from_simulation(lens, spherical=True, Fresnel=False, z_LED=201e-3, arraysize=array_size)

def experimental():
    datadirpath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\dotarray_2x_dark_no_object"
    illustrate_illumination_from_setup(datadirpath, lens, array_size)

if __name__ == "__main__": 
    simulate_illumination()
    simulate_both()
    experimental()
    plt.show()