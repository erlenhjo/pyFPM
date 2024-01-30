import matplotlib.pyplot as plt
from pyFPM.NTNU_specific.components import TELECENTRIC_3X

from general_functions import illustrate_dataset_from_setup

lens = TELECENTRIC_3X
array_size = 9


def test_camera():
    datadirpath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\Fourier_Ptychography\usaf_test_new_camera_3x_telecentric"
    fig = illustrate_dataset_from_setup(datadirpath, lens, array_size)

def underfocused_500():
    datadirpath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\Master_thesis\defocus_190124\telecentric_dot_underfocused_500_9"
    fig = illustrate_dataset_from_setup(datadirpath, lens, array_size)

if __name__ == "__main__": 
    underfocused_500()
    plt.show()