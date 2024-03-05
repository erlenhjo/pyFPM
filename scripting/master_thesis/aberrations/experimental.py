import matplotlib.pyplot as plt
import numpy as np

from recover_telecentric import recover_telecentric
from recover_10x import recover_10x

patch_start = np.array([2848, 2844], dtype=int) // 2 - np.array([512+128,256+128])
patch_size = [64, 64]
max_array_size = 3
result_folder = r"C:\Users\erlen\Documents\GitHub\pyFPM\scripting\master_thesis\aberrations\results"

def telecentric_dot_array_window():
    title = "Telecentric dot array window"
    datadirpath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\Master_thesis\aberrations_040324\dot_array_3x_tele_window"
    recover_telecentric(title, datadirpath, patch_start, patch_size, max_array_size, result_folder)

def telecentric_usaf_focused():
    title = "Telecentric USAF focused"
    datadirpath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\Master_thesis\aberrations_040324\usaf_3x_tele_0"
    recover_telecentric(title, datadirpath, patch_start, patch_size, max_array_size, result_folder)

def telecentric_usaf_m10():
    title = "Telecentric USAF -10um"
    datadirpath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\Master_thesis\aberrations_040324\usaf_3x_tele_m10"
    recover_telecentric(title, datadirpath, patch_start, patch_size, max_array_size, result_folder)

def telecentric_usaf_m20():
    title = "Telecentric USAF -20um"
    datadirpath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\Master_thesis\aberrations_040324\usaf_3x_tele_m20"
    recover_telecentric(title, datadirpath, patch_start, patch_size, max_array_size, result_folder)
    
def telecentric_usaf_p20():
    title = "Telecentric USAF +20um"
    datadirpath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\Master_thesis\aberrations_040324\usaf_3x_tele_p20"
    recover_telecentric(title, datadirpath, patch_start, patch_size, max_array_size, result_folder)
    
def telecentric_usaf_p10():
    title = "Telecentric USAF +10um"
    datadirpath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\Master_thesis\aberrations_040324\usaf_3x_tele_p10"
    recover_telecentric(title, datadirpath, patch_start, patch_size, max_array_size, result_folder)
    
def telecentric_usaf_backwards():
    title = "Telecentric USAF backwards"
    datadirpath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\Master_thesis\aberrations_040324\usaf_3x_tele_backwards"
    recover_telecentric(title, datadirpath, patch_start, patch_size, max_array_size, result_folder)

def telecentric_usaf_window():
    title = "Telecentric USAF window"
    datadirpath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\Master_thesis\aberrations_040324\usaf_3x_tele_window"
    recover_telecentric(title, datadirpath, patch_start, patch_size, max_array_size, result_folder)

def inf10x_usaf_focused():
    title = "Infinity 10x USAF focused"
    datadirpath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\Master_thesis\aberrations_040324\usaf_10x_inf_0"
    recover_10x(title, datadirpath, patch_start, patch_size, max_array_size, result_folder)

def inf10x_usaf_p3():
    title = "Infinity 10x USAF +3um"
    datadirpath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\Master_thesis\aberrations_040324\usaf_10x_inf_p3"
    recover_10x(title, datadirpath, patch_start, patch_size, max_array_size, result_folder)

def inf10x_usaf_m3():
    title = "Infinity 10x USAF -3um"
    datadirpath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\Master_thesis\aberrations_040324\usaf_10x_inf_m3"
    recover_10x(title, datadirpath, patch_start, patch_size, max_array_size, result_folder)


if __name__ == "__main__":
    #telecentric_dot_array_window()
    #telecentric_usaf_p20()
    #telecentric_usaf_p10()
    telecentric_usaf_m10()
    #telecentric_usaf_m20()
    #telecentric_usaf_focused()
    #telecentric_usaf_backwards()
    #telecentric_usaf_window()
    #inf10x_usaf_focused()
    #inf10x_usaf_m3()
    #inf10x_usaf_p3()
    plt.show()
