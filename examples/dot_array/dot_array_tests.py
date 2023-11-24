import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

from pyFPM.aberrations.dot_array.plot_dot_array import (plot_example_dots, plot_dot_error)
from pyFPM.aberrations.dot_array.locate_dot_array import (locate_dots,
                                                          assemble_dots_in_grid)                                          
from pyFPM.NTNU_specific.components import EO_DOT_ARRAY, HAMAMATSU_C11440_42U30, INFINITYCORRECTED_2X, TELECENTRIC_3X



def locate_and_plot_dots():
    #filepath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\dotarray_telecentric3x_dark\0_34-16_16.tiff"
    filepath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\dotarray_2x_object\0_10-16_16.tiff"

    image = np.array(Image.open(filepath))#[1300:,1300:]

    dot_array = EO_DOT_ARRAY
    camera = HAMAMATSU_C11440_42U30
    lens = TELECENTRIC_3X
    #lens = INFINITYCORRECTED_2X

    fig, axes = plt.subplots(nrows=1,ncols=2)
    axes[0].matshow(image)
    axes[0].set_axis_off()
    
    object_pixel_size = camera.camera_pixel_size / lens.magnification
    
    located_blobs = locate_dots(image, dot_array, object_pixel_size, sub_precision=4)
    blobs, grid_points, grid_indices, rotation = assemble_dots_in_grid(image, located_blobs, dot_array, object_pixel_size)
    print(f"The total rotation was {rotation} degrees")       
    plot_dot_error(ax=axes[1], blobs=blobs, grid_points=grid_points, 
                    grid_indices=grid_indices, object_pixel_size=object_pixel_size)

    fig.tight_layout()
    fig_2 = plt.figure()
    plot_example_dots(fig_2, image, blobs, grid_points, grid_indices, dot_array, object_pixel_size)

    plt.show()


def profile_main():
    import cProfile
    import pstats

    with cProfile.Profile() as pr:
        main()
    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.dump_stats(filename=r"profiling_data\dot_array_raw_real.prof")

def main():
    locate_and_plot_dots()

if __name__ == "__main__":
    profile_main()
