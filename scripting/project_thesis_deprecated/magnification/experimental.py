import matplotlib.pyplot as plt

from general_functions import locate_and_plot_dots, locate_and_scatter_plot

from pyFPM.NTNU_specific.components import  TELECENTRIC_3X, INFINITYCORRECTED_2X, COMPACT_2X, DOUBLE_CONVEX

subprecision = 8
result_folder = r"C:\Users\erlen\Documents\GitHub\pyFPM\examples\project_thesis\results\magnification"
dpi = 1000

def telecentric(save):
    lens = TELECENTRIC_3X
    filepath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\Magnification\Magnification_per_defocus_all\telecentric_0.tif"
    
    fig_0, fig_1, fig_2, fig_3 = locate_and_plot_dots(lens=lens, filepath=filepath, subprecision=subprecision)
    if save:
        fig_0.savefig(result_folder+"\magnification_telecentric_image.pdf", dpi = dpi)
        fig_1.savefig(result_folder+"\magnification_telecentric_error_matrix.pdf", dpi = dpi)
        fig_2.savefig(result_folder+"\magnification_telecentric_example_dots.pdf", dpi = dpi)
        fig_3.savefig(result_folder+"\magnification_telecentric_error_plots.pdf", dpi = dpi)

def infinity_corrected(save):
    lens = INFINITYCORRECTED_2X
    filepath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\Magnification\Magnification_per_defocus_all\infinity_0.tif"
    enforced_grid_shift = [0.1,1.4]

    fig_0, fig_1, fig_2, fig_3 = locate_and_plot_dots(lens=lens, filepath=filepath, subprecision=subprecision, enforced_grid_shift=enforced_grid_shift)
    if save:
        fig_0.savefig(result_folder+"\magnification_infinity_image.pdf", dpi = dpi)
        fig_1.savefig(result_folder+"\magnification_infinity_error_matrix.pdf", dpi = dpi)
        fig_2.savefig(result_folder+"\magnification_infinity_example_dots.pdf", dpi = dpi)
        fig_3.savefig(result_folder+"\magnification_infinity_error_plots.pdf", dpi = dpi)




def compact(save):
    lens = COMPACT_2X
    filepath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\Magnification\Magnification_per_defocus_all\compact_0.tif"
    
    fig_0, fig_1, fig_2, fig_3 = locate_and_plot_dots(lens=lens, filepath=filepath, subprecision=subprecision)
    if save:
        fig_0.savefig(result_folder+"\magnification_compact_image.pdf", dpi = dpi)
        fig_1.savefig(result_folder+"\magnification_compact_error_matrix.pdf", dpi = dpi)
        fig_2.savefig(result_folder+"\magnification_compact_example_dots.pdf", dpi = dpi)
        fig_3.savefig(result_folder+"\magnification_compact_error_plots.pdf", dpi = dpi)


def double_convex(save):
    lens = DOUBLE_CONVEX
    filepath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\Magnification\Magnification_per_defocus_all\Single_lens_in_focus.tif"
    fig_0, fig_1, fig_2, fig_3 = locate_and_plot_dots(lens=lens, filepath=filepath, subprecision=subprecision)
    if save:
        fig_0.savefig(result_folder+"\magnification_double_convex_image.pdf", dpi = dpi)
        fig_1.savefig(result_folder+"\magnification_double_convex_error_matrix.pdf", dpi = dpi)
        fig_2.savefig(result_folder+"\magnification_double_convex_example_dots.pdf", dpi = dpi)
        fig_3.savefig(result_folder+"\magnification_double_convex_error_plots.pdf", dpi = dpi)


    





if __name__ == "__main__":
    save=False
    telecentric(save)
    infinity_corrected(save)
    compact(save)
    double_convex(save)
    plt.show()