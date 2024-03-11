import matplotlib.pyplot as plt
from pyFPM.NTNU_specific.components import TELECENTRIC_3X

from general_functions import illustrate_illumination_from_setup, illustrate_illumination_from_simulation

lens = TELECENTRIC_3X
array_size = 7
savefolderpath = r"C:\Users\erlen\Documents\GitHub\pyFPM\examples\project_thesis_deprecated\results\illumination"

def simulate_both():
    fig = illustrate_illumination_from_simulation(lens, spherical=True, Fresnel=True, z_LED=200e-3, arraysize=array_size)
    #fig.savefig(savefolderpath+r"\telecentric_sim_both.pdf")

def simulate_illumination():
    fig = illustrate_illumination_from_simulation(lens, spherical=True, Fresnel=False, z_LED=200e-3, arraysize=array_size)
    #fig.savefig(savefolderpath+r"\telecentric_sim_illum.pdf")

def experimental_reflections():
    datadirpath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\dotarray_telecentric3x_dark_no_object"
    #fig = illustrate_illumination_from_setup(datadirpath, lens, array_size)

def experimental_proper():
    datadirpath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\Illumination\telecentric_3x_illumination_2"
    fig = illustrate_illumination_from_setup(datadirpath, lens, array_size)
    #fig.savefig(savefolderpath+r"\telecentric_experimental.pdf")

if __name__ == "__main__": 
    simulate_illumination()
    # simulate_both()
    # experimental_reflections()
    experimental_proper()
    plt.show()