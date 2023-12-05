import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import os

from pyFPM.aberrations.dot_array.plot_dot_array import (plot_example_dots, plot_dot_error)
from pyFPM.aberrations.dot_array.locate_dot_array import (locate_dots,
                                                          assemble_dots_in_grid)                                          
from pyFPM.NTNU_specific.components import (EO_DOT_ARRAY, HAMAMATSU_C11440_42U30, INFINITYCORRECTED_2X, 
                                            TELECENTRIC_3X, COMPACT_2X, DOUBLE_CONVEX)



def locate_and_plot_dots():
    datadirpath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\Magnification\Magnification_per_defocus_all"
    outputdirpath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\generated_plots\magnification"
    print(os.listdir(datadirpath))
    for filename in os.listdir(datadirpath):
        filepath = os.path.join(datadirpath,filename)
        lens_name = filename.split("_")[0]
        if lens_name == "compact":
            lens = COMPACT_2X
        elif lens_name == "infinity":
            lens = INFINITYCORRECTED_2X
        elif lens_name == "telecentric":
            lens = TELECENTRIC_3X
        else:
            #print(f"{filename} was skipped")
            lens = DOUBLE_CONVEX
        print(f"{filename} is being processed")
        fig_1, fig_2 = locate_and_plot(filepath, lens, filename)
        fig_1.savefig(os.path.join(r"C:\Users\erlen\Documents\GitHub\pyFPM\examples\project_thesis\results\mag_per_defocus",filename.split(".")[0]+".png"))
        fig_2.savefig(os.path.join(r"C:\Users\erlen\Documents\GitHub\pyFPM\examples\project_thesis\results\mag_per_defocus",filename.split(".")[0]+"_dots.png"))
    plt.show()



def locate_and_plot(filepath, lens, filename):
    image = np.array(Image.open(filepath))

    dot_array = EO_DOT_ARRAY
    camera = HAMAMATSU_C11440_42U30

    fig_1, axes = plt.subplots(nrows=1,ncols=1)

    object_pixel_size = camera.camera_pixel_size / lens.magnification
    
    located_blobs = locate_dots(image, dot_array, object_pixel_size, sub_precision=8)
    blobs, grid_points, grid_indices, rotation = assemble_dots_in_grid(image, located_blobs, dot_array, object_pixel_size)
    print(f"The total rotation was {rotation} degrees")       
    plot_dot_error(ax=axes, blobs=blobs, grid_points=grid_points, 
                    grid_indices=grid_indices, object_pixel_size=object_pixel_size)

    fig_1.tight_layout()

    fig_2 = plt.figure()

    plot_example_dots(fig_2, image, blobs, grid_points, grid_indices, dot_array, object_pixel_size)

    fig_1.suptitle(filename)
    fig_2.suptitle(filename)

    return fig_1, fig_2



def main():
    locate_and_plot_dots()

if __name__ == "__main__":
    main()
