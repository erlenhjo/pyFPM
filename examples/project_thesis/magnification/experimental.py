import matplotlib.pyplot as plt

from general_functions import locate_and_plot_dots, locate_and_scatter_plot

from pyFPM.NTNU_specific.components import  TELECENTRIC_3X, INFINITYCORRECTED_2X, COMPACT_2X, DOUBLE_CONVEX

subprecision = 8
result_folder = r"C:\Users\erlen\Documents\GitHub\pyFPM\examples\project_thesis\results\magnification"

def telecentric():
    lens = TELECENTRIC_3X
    filepath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\Magnification\Magnification_per_defocus_telecentric\-0,05.tif"
    locate_and_scatter_plot(lens=lens, filepath=filepath, subprecision=subprecision)

    filepath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\Magnification\Magnification_per_defocus_telecentric\-0,04.tif"
    locate_and_scatter_plot(lens=lens, filepath=filepath, subprecision=subprecision)

    filepath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\Magnification\Magnification_per_defocus_telecentric\-0,03.tif"
    locate_and_scatter_plot(lens=lens, filepath=filepath, subprecision=subprecision)

    filepath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\Magnification\Magnification_per_defocus_telecentric\-0,02.tif"
    locate_and_scatter_plot(lens=lens, filepath=filepath, subprecision=subprecision)

    filepath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\Magnification\Magnification_per_defocus_telecentric\-0,01.tif"
    locate_and_scatter_plot(lens=lens, filepath=filepath, subprecision=subprecision)

    filepath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\Magnification\Magnification_per_defocus_telecentric\0.tif"
    locate_and_scatter_plot(lens=lens, filepath=filepath, subprecision=subprecision)

    filepath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\Magnification\Magnification_per_defocus_telecentric\0,01.tif"
    locate_and_scatter_plot(lens=lens, filepath=filepath, subprecision=subprecision)

    filepath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\Magnification\Magnification_per_defocus_telecentric\0,02.tif"
    locate_and_scatter_plot(lens=lens, filepath=filepath, subprecision=subprecision)

    filepath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\Magnification\Magnification_per_defocus_telecentric\0,03.tif"
    locate_and_scatter_plot(lens=lens, filepath=filepath, subprecision=subprecision)

    filepath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\Magnification\Magnification_per_defocus_telecentric\0,04.tif"
    locate_and_scatter_plot(lens=lens, filepath=filepath, subprecision=subprecision)

    filepath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\Magnification\Magnification_per_defocus_telecentric\0,05.tif"
    locate_and_scatter_plot(lens=lens, filepath=filepath, subprecision=subprecision)


def infinity_corrected():
    lens = INFINITYCORRECTED_2X
    filepath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\Magnification\Magnification_per_defocus_all\infinity_0.tif"
    
    locate_and_plot_dots(lens=lens, filepath=filepath, subprecision=subprecision)


def compact():
    lens = COMPACT_2X
    filepath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\Magnification\Magnification_per_defocus_all\compact_0.tif"
    
    locate_and_plot_dots(lens=lens, filepath=filepath, subprecision=subprecision)


def double_convex(save):
    lens = DOUBLE_CONVEX
    filepath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\Magnification\Magnification_per_defocus_all\Single_lens_in_focus.tif"
    fig_0, fig_1, fig_2 = locate_and_plot_dots(lens=lens, filepath=filepath, subprecision=subprecision)
    if save:
        fig_0.savefig(result_folder+"\magnification_double_convex_image.pdf", dpi = 4000)
        fig_1.savefig(result_folder+"\magnification_double_convex_error.pdf", dpi = 4000)


    





if __name__ == "__main__":
    telecentric()
    #infinity_corrected()
    #compact()
    #double_convex(save=False)
    plt.show()