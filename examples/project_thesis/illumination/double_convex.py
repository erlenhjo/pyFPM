import matplotlib.pyplot as plt
from pyFPM.NTNU_specific.components import DOUBLE_CONVEX

from general_functions import illustrate_illumination_from_setup, illustrate_illumination_from_simulation

lens = DOUBLE_CONVEX
array_size = 7

savefolderpath = r"C:\Users\erlen\Documents\GitHub\pyFPM\examples\project_thesis\results\illumination"

def simulate_both():
    fig = illustrate_illumination_from_simulation(lens, spherical=True, Fresnel=True, z_LED=200e-3, arraysize=array_size)
    fig.savefig(savefolderpath+r"\double_convex_sim_both.pdf")

def simulate_illumination():
    fig = illustrate_illumination_from_simulation(lens, spherical=True, Fresnel=False, z_LED=200e-3, arraysize=array_size)
    fig.savefig(savefolderpath+r"\double_convex_sim_illum.pdf")

def experimental():
    datadirpath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\Illumination\double_convex_illumination"
    fig = illustrate_illumination_from_setup(datadirpath, lens, array_size)
    fig.savefig(savefolderpath+r"\double_convex_experimental.pdf")

if __name__ == "__main__":
    simulate_illumination()
    simulate_both()
    experimental()
    
    plt.show()

    