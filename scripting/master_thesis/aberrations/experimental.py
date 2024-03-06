import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

from recover_telecentric import recover_telecentric
from recover_10x import recover_10x

patch_start = np.array([2848, 2844], dtype=int) // 2 - np.array([512,512])
patch_size = [1024, 1024]
max_array_size = 9
cwd = Path.cwd()
result_folder = cwd / "scripting/master_thesis/aberrations/results"
data_folder = cwd / "data/Master_thesis/aberrations_040324"
Path.mkdir(result_folder, parents=True, exist_ok=True)

def telecentric_dot_array_window():
    title = "Telecentric dot array window"
    datadirpath = data_folder / "dot_array_3x_tele_window"
    recover_telecentric(title, datadirpath, patch_start, patch_size, max_array_size, result_folder)

def telecentric_usaf_focused():
    title = "Telecentric USAF focused"
    datadirpath = data_folder / "usaf_3x_tele_0"
    recover_telecentric(title, datadirpath, patch_start, patch_size, max_array_size, result_folder)

def telecentric_usaf_m10():
    title = "Telecentric USAF -10um"
    datadirpath = data_folder / "usaf_3x_tele_m10"
    recover_telecentric(title, datadirpath, patch_start, patch_size, max_array_size, result_folder)

def telecentric_usaf_m20():
    title = "Telecentric USAF -20um"
    datadirpath = data_folder / "usaf_3x_tele_m20"
    recover_telecentric(title, datadirpath, patch_start, patch_size, max_array_size, result_folder)
    
def telecentric_usaf_p20():
    title = "Telecentric USAF +20um"
    datadirpath = data_folder / "usaf_3x_tele_p20"
    recover_telecentric(title, datadirpath, patch_start, patch_size, max_array_size, result_folder)
    
def telecentric_usaf_p10():
    title = "Telecentric USAF +10um"
    datadirpath = data_folder / "usaf_3x_tele_p10"
    recover_telecentric(title, datadirpath, patch_start, patch_size, max_array_size, result_folder)
    
def telecentric_usaf_backwards():
    title = "Telecentric USAF backwards"
    datadirpath = data_folder / "usaf_3x_tele_backwards"
    recover_telecentric(title, datadirpath, patch_start, patch_size, max_array_size, result_folder)

def telecentric_usaf_window():
    title = "Telecentric USAF window"
    datadirpath = data_folder / "usaf_3x_tele_window"
    recover_telecentric(title, datadirpath, patch_start, patch_size, max_array_size, result_folder)

def inf10x_usaf_focused():
    title = "Infinity 10x USAF focused"
    datadirpath = data_folder / "usaf_10x_inf_0"
    recover_10x(title, datadirpath, patch_start, patch_size, max_array_size, result_folder)

def inf10x_usaf_p3():
    title = "Infinity 10x USAF +3um"
    datadirpath = data_folder / "usaf_10x_inf_p3"
    recover_10x(title, datadirpath, patch_start, patch_size, max_array_size, result_folder)

def inf10x_usaf_m3():
    title = "Infinity 10x USAF -3um"
    datadirpath = data_folder / "usaf_10x_inf_m3"
    recover_10x(title, datadirpath, patch_start, patch_size, max_array_size, result_folder)


if __name__ == "__main__":
    telecentric_dot_array_window()
    plt.close()
    telecentric_usaf_p20()
    plt.close()
    telecentric_usaf_p10()
    plt.close()
    telecentric_usaf_m10()
    plt.close()
    telecentric_usaf_m20()
    plt.close()
    telecentric_usaf_focused()
    plt.close()
    telecentric_usaf_backwards()
    plt.close()
    telecentric_usaf_window()
    plt.close()
    inf10x_usaf_focused()
    plt.close()
    inf10x_usaf_m3()
    plt.close()
    inf10x_usaf_p3()
    plt.close()
    #plt.show()
