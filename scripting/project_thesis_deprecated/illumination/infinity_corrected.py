import matplotlib.pyplot as plt
from pyFPM.NTNU_specific.components import INFINITYCORRECTED_2X

from general_functions import illustrate_illumination_from_setup, illustrate_illumination_from_simulation

lens = INFINITYCORRECTED_2X
array_size = 5
savefolderpath = r"C:\Users\erlen\Documents\GitHub\pyFPM\scripting\project_thesis_deprecated\results\illumination"

def simulate_both():
    fig = illustrate_illumination_from_simulation(lens, spherical=True, Fresnel=True, z_LED=200e-3, arraysize=array_size)
    fig.savefig(savefolderpath+r"\infinity_sim_both.pdf")

def simulate_illumination():
    fig = illustrate_illumination_from_simulation(lens, spherical=True, Fresnel=False, z_LED=200e-3, arraysize=array_size)
    fig.savefig(savefolderpath+r"\infinity_sim_illum.pdf")

def experimental():
    datadirpath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\Illumination\infinity_2x_illumnation"
    fig = illustrate_illumination_from_setup(datadirpath, lens, array_size)
    fig.savefig(savefolderpath+r"\infinity_experimental.pdf")

if __name__ == "__main__": 
    simulate_illumination()
    #simulate_both()
    #experimental()
    plt.show()