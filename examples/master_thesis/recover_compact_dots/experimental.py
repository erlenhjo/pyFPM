import matplotlib.pyplot as plt
import numpy as np

from recover_compact import recover_compact

patch_start = np.array([2856, 2848], dtype=int) // 2 - 256
patch_size = [512, 512]

def compact_5_overfocused_500():
    title = "Compact focus=500 5x5"
    datadirpath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\Master_thesis\defocus_190124\compact_dot_overfocused_500_5"
    defocus_guess = 0
    max_array_size = 5
    recover_compact(title, datadirpath, patch_start, patch_size, defocus_guess, max_array_size)

if __name__ == "__main__":
    compact_5_overfocused_500()
    plt.show()
