import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from pathlib import Path


size_recover = 512
size_plot = size_recover//10
location_recover = [-1.05, 0]
location_plot = [1.05, 0]

patch_offset_corner = np.array([-1090,-1062])
patch_offset_center = np.array([-37,-72])

corner_path = Path.cwd() / "data" / "Master_thesis" / "calibration_test" / "comp2x_usaf_corner" / "0_18-16_16.png"
center_path = Path.cwd() / "data" / "Master_thesis" / "sapphire window" / "compact2x_usaf_200mm" / "0_18-16_16.png"

result_folder = main_result_folder = Path.cwd() / "results" / "master_thesis" / "BFL_recovery"


def main():
    image_center = np.array(Image.open(center_path))
    image_corner = np.array(Image.open(corner_path))

    fig_center = create_figure(image_center, patch_offset_center)
    fig_corner = create_figure(image_corner, patch_offset_corner)

    fig_center.savefig(result_folder / "recovered_region_center.pdf", 
                       format = "pdf", 
                       bbox_inches="tight")
    fig_corner.savefig(result_folder / "recovered_region_corner.pdf", 
                       format = "pdf", 
                       bbox_inches="tight")

def create_figure(image, offset):
    fig, axes = plt.subplots(1, 1, constrained_layout=True)

    vlims = [0, np.max(image)]
    axes.matshow(image, vmin=vlims[0], vmax=vlims[1])    
    axes.axis("off")
    axes.margins(x=0, y=0)

    inset_line_color = "red"

    create_zoom(axes, image, location_plot, inset_line_color, vlims, size_plot, offset)
    create_zoom(axes, image, location_recover, inset_line_color, vlims, size_recover, offset)

    fig.set_constrained_layout_pads()

    return fig


def get_offset_zoomed_image(image, size, offset):
        max_x = image.shape[1]
        max_y = image.shape[0]
        center_x = max_x // 2
        center_y = max_y // 2       

        start_x = center_x + offset[0] - size//2
        stop_x = center_x + offset[0] + size//2
        start_y = center_y + offset[1] - size//2
        stop_y = center_y + offset[1] + size//2
    
        subimage = image[start_y:stop_y, start_x:stop_x]
        x_lim = (start_x, stop_x)
        y_lim = (start_y, stop_y)

        return subimage, x_lim, y_lim

def create_zoom(ax, image, location, inset_line_color, vlims, size, offset):
        inset_axes_size = (1, 1) # width, height
        inset_axes_loc = tuple(location)

        subimage, x_lim, y_lim = get_offset_zoomed_image(image, size, offset)

        axin = ax.inset_axes(
            inset_axes_loc + inset_axes_size,
            xlim = x_lim,
            ylim = y_lim
        )
        _, connector_lines = ax.indicate_inset_zoom(axin, edgecolor=inset_line_color)
        for line in connector_lines:
            line.set_visible(True)

        axin.set_xlim(auto=True)
        axin.set_ylim(auto=True)
        axin.imshow(subimage, vmin=vlims[0], vmax=vlims[1])
        axin.set_xticks([])
        axin.set_yticks([])


if __name__ == "__main__":
    main()