import matplotlib.pyplot as plt
import numpy as np

from recover_telecentric import recover_telecentric

patch_start = np.array([2856, 2848], dtype=int) // 2 - 256
patch_size = [512, 512]

def telecentric_9_focus():
    title = "Telecentric focused 9x9"
    datadirpath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\Master_thesis\defocus_190124\telecentric_dot_focused_9"
    defocus_guess = 0
    max_array_size = 9
    recover_telecentric(title, datadirpath, patch_start, patch_size, defocus_guess, max_array_size)
    
def telecentric_7_focus():
    title = "Telecentric focused 7x7"
    datadirpath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\Master_thesis\defocus_190124\telecentric_dot_focused_7"
    defocus_guess = 0
    max_array_size = 7
    recover_telecentric(title, datadirpath, patch_start, patch_size, defocus_guess, max_array_size)

def telecentric_5_focus():
    title = "Telecentric focused 5x5"
    datadirpath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\Master_thesis\defocus_190124\telecentric_dot_focused_5"
    defocus_guess = 0
    max_array_size = 5
    recover_telecentric(title, datadirpath, patch_start, patch_size, defocus_guess, max_array_size)

def telecentric_5_overfocus_500():
    title = "Telecentric focus=500 5x5"
    datadirpath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\Master_thesis\defocus_190124\telecentric_dot_overfocused_500_5"
    defocus_guess = 0
    max_array_size = 5
    recover_telecentric(title, datadirpath, patch_start, patch_size, defocus_guess, max_array_size)

def telecentric_5_overfocus_100():
    title = "Telecentric focus=100 5x5"
    datadirpath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\Master_thesis\defocus_190124\telecentric_dot_overfocused_100_5"
    defocus_guess = 0
    max_array_size = 5
    recover_telecentric(title, datadirpath, patch_start, patch_size, defocus_guess, max_array_size)

def telecentric_5_underfocus_500():
    title = "Telecentric focus=-500 5x5"
    datadirpath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\Master_thesis\defocus_190124\telecentric_dot_underfocused_500_5"
    defocus_guess = 0
    max_array_size = 5
    recover_telecentric(title, datadirpath, patch_start, patch_size, defocus_guess, max_array_size)


if __name__ == "__main__":
    telecentric_9_focus()
    #telecentric_7_focus()
    #telecentric_5_focus()
    #telecentric_5_overfocus_100()
    #telecentric_5_overfocus_500()
    telecentric_5_underfocus_500()
    plt.show()
