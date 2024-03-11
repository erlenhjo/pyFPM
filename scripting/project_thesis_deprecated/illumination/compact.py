import matplotlib.pyplot as plt
from pyFPM.NTNU_specific.components import COMPACT_2X

from general_functions import illustrate_illumination_from_setup, illustrate_illumination_from_simulation

lens = COMPACT_2X
array_size = 3

savefolderpath = r"C:\Users\erlen\Documents\GitHub\pyFPM\examples\project_thesis\results\illumination"

def simulate_both_WD():
    fig = illustrate_illumination_from_simulation(lens, spherical=True, Fresnel=True, z_LED=200e-3, arraysize=array_size, 
                                                  use_working_distance=True)
    #fig.savefig(savefolderpath+r"\compact_sim_both_working_distance.pdf")

def simulate_both():
    fig = illustrate_illumination_from_simulation(lens, spherical=True, Fresnel=True, z_LED=200e-3, arraysize=array_size)
    #fig.savefig(savefolderpath+r"\compact_sim_both.pdf")

def simulate_illumination():
    fig = illustrate_illumination_from_simulation(lens, spherical=True, Fresnel=False, z_LED=200e-3, arraysize=array_size)
    #fig.savefig(savefolderpath+r"\compact_sim_illum.pdf")

def experimental():
    datadirpath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\Illumination\compact_2x_illumination"
    fig = illustrate_illumination_from_setup(datadirpath, lens, array_size)
    #fig.savefig(savefolderpath+r"\compact_experimental.pdf")

if __name__ == "__main__": 
    #simulate_illumination()
    simulate_both()
    simulate_both_WD()
    experimental()
    plt.show()