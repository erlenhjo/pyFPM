import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

from pyFPM.aberrations.dot_array.plot_dot_array import (plot_located_dots,
                                                        plot_located_dots_vs_grid,
                                                        plot_located_dot_error)
from pyFPM.aberrations.dot_array.locate_dot_array import (locate_dots,
                                                          assemble_dots_in_grid)                                          
from pyFPM.NTNU_specific.components import (HAMAMATSU_C11440_42U30, 
                                            INFINITYCORRECTED_2X,
                                            EO_DOT_ARRAY)


def locate_and_plot_dots():
    filepath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\EHJ20230915_dotarray_2x_inf\0_10-16_16.tiff"

    image = np.array(Image.open(filepath))

    dot_array = EO_DOT_ARRAY
    pixel_size = HAMAMATSU_C11440_42U30.camera_pixel_size
    magnification = INFINITYCORRECTED_2X.magnification

    object_pixel_size = pixel_size / magnification

    located_blobs = locate_dots(image, dot_array, object_pixel_size, sub_precision=4)

    blobs, grid_points, grid_indices, rotation = assemble_dots_in_grid(image.shape, located_blobs, dot_array.spacing, object_pixel_size)
    print(f"The total rotation was {rotation} degrees")
    plot_located_dots_vs_grid(image, blobs, grid_points)
    plot_located_dot_error(blobs, grid_points, grid_indices, object_pixel_size)
    plt.show()


def profile_main():
    import cProfile
    import pstats

    with cProfile.Profile() as pr:
        main()
    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.dump_stats(filename=r"profiling_data\dot_array_real.prof")

def main():
    locate_and_plot_dots()

if __name__ == "__main__":
    profile_main()
