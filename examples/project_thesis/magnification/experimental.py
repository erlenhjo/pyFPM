import matplotlib.pyplot as plt

from general_functions import locate_and_plot_dots

from pyFPM.NTNU_specific.components import  TELECENTRIC_3X, INFINITYCORRECTED_2X, COMPACT_2X, DOUBLE_CONVEX

subprecision = 4

def telecentric():
    lens = TELECENTRIC_3X
    filepath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\Magnification_per_defocus_telecentric\0.tif"
    
    locate_and_plot_dots(lens=lens, filepath=filepath, subprecision=subprecision)


def infinity_corrected():
    lens = INFINITYCORRECTED_2X
    filepath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\dotarray_2x_dark_object\0_10-16_16.tiff"
    
    locate_and_plot_dots(lens=lens, filepath=filepath, subprecision=subprecision)


def compact():
    lens = COMPACT_2X
    filepath = r""
    
    locate_and_plot_dots(lens=lens, filepath=filepath, subprecision=subprecision)


def double_convex():
    lens = DOUBLE_CONVEX
    filepath = r""
    
    locate_and_plot_dots(lens=lens, filepath=filepath, subprecision=subprecision)





if __name__ == "__main__":
    telecentric()
    #infinity_corrected()
    #compact()
    #double_convex()
    plt.show()