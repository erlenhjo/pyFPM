import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionPatch
from pathlib import Path
                                         
from pyFPM.NTNU_specific.components import EO_DOT_ARRAY, IDS_U3_31J0CP_REV_2_2, FUJINON_MINWD_MAXNA


main_result_folder = Path.cwd() / "results" / "master_thesis"
fujinon_result_folder = main_result_folder / "fujinon"
fujinon_result_folder.mkdir(parents=True, exist_ok=True)
                                        


def plot_dots():
    filepath = Path.cwd() / "data" / "Master_thesis" / "fujinon" / "fujinon_magnification_dot_array_incoherent.png"

    patch_size = 512
    full_image = np.array(Image.open(filepath))
    image = full_image[full_image.shape[0]//2-patch_size//2:full_image.shape[0]//2+patch_size//2,\
                       full_image.shape[1]//2-patch_size//2:full_image.shape[1]//2+patch_size//2]

    dot_array = EO_DOT_ARRAY
    camera = IDS_U3_31J0CP_REV_2_2

    magnification = FUJINON_MINWD_MAXNA.magnification
    rotation = -0.1
    center_shift = np.array([-2.25,-2.5])

    object_pixel_size = camera.camera_pixel_size / magnification

    grid_points = get_grid_points(image_shape = image.shape, 
                                  pixel_size = object_pixel_size,
                                  dot_spacing = dot_array.spacing,
                                  rotation = rotation,
                                  center_shift = center_shift
                                  )

    fig = overlay_grid_points(image, grid_points)

    fig.savefig(fujinon_result_folder / "fujinon_magnification.png")
    fig.savefig(fujinon_result_folder / "fujinon_magnification.pdf")


def get_grid_points(image_shape, pixel_size, dot_spacing, rotation, center_shift):
    dot_array_size = ((np.array(image_shape)*pixel_size/dot_spacing).astype(np.int16)//2)*2 
    dot_spacing_pixels = dot_spacing / pixel_size
    
    center_y = image_shape[0]//2 + center_shift[0]
    center_x = image_shape[1]//2 + center_shift[1]
    size_y = dot_array_size[0]
    size_x = dot_array_size[1]
    

    untilted_grid = np.zeros(shape=(size_y+1, size_x+1, 2))  # indexes Y, X plus y, x coords
    for Y in range(size_y+1):
        for X in range(size_x+1):
            y_coord = (Y-size_y//2) * dot_spacing_pixels
            x_coord = (X-size_x//2) * dot_spacing_pixels
            untilted_grid[Y, X] = np.array([y_coord, x_coord])

    grid_points = untilted_grid.reshape(-1 ,untilted_grid.shape[-1])

    #rotate
    rotation_matrix = get_rotation_matrix(rotation)
    grid_points = grid_points.dot(rotation_matrix)

    return grid_points + np.array([center_y, center_x])


def get_rotation_matrix(degrees):
    # matrix for rotating image coordinates y, x clocwise
    cos = np.cos(degrees*np.pi/180)
    sin = np.sin(degrees*np.pi/180)
    rotation_matrix = [[cos,  sin],
                       [-sin, cos]]
    
    return np.array(rotation_matrix)


def overlay_grid_points(image, grid_points):
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8,4), constrained_layout=True)
    ax.imshow(image, cmap="gist_gray")
    ax.set_axis_off()
    for im in ax.get_images():
        im.set_clim(vmin=np.min(image), vmax=np.max(image))

    max_x = image.shape[1]
    max_y = image.shape[0]
    edge_offset = 100
    size = 100

    inset_regions = [
        (edge_offset, edge_offset, size),
        (edge_offset, max_y-edge_offset, size),
        (max_x//2, max_y//2, size),
        (max_x - edge_offset, edge_offset, size)
    ]

    inset_axes_size = [0.45, 0.45] # width, height
    inset_axes_pos = [
        [-0.5, 0.55],
        [-0.5, 0],
        [1.05, 0],
        [1.05, 0.55]
    ]

    grid_color = "red"
    grid_marker = "x"
    grin_marker_size = 2
    border_thickness = 1
    border_color = "red"

    for (x, y, size), inset_axes_position in zip(inset_regions, inset_axes_pos):
        start_x = x - size//2
        stop_x = x + size//2
        start_y = y - size//2
        stop_y = y + size//2
        
        subimage = image[start_y:stop_y, start_x:stop_x]

        axin = ax.inset_axes(
            inset_axes_position + inset_axes_size,
            xlim = (start_x, stop_x),
            ylim = (start_y, stop_y)
        )
        _, connector_lines = ax.indicate_inset_zoom(axin, edgecolor=border_color)
        for line in connector_lines:
            line: ConnectionPatch = line
            line.set_visible(True)



        axin.set_xlim(auto=True)
        axin.set_ylim(auto=True)
        axin.imshow(subimage, cmap="gist_gray")
        axin.set_xticks([])
        axin.set_yticks([])

        axin.spines['bottom'].set_color(border_color)
        axin.spines['bottom'].set_linewidth(border_thickness)
        axin.spines['top'].set_color(border_color) 
        axin.spines['top'].set_linewidth(border_thickness) 
        axin.spines['right'].set_color(border_color)
        axin.spines['right'].set_linewidth(border_thickness)
        axin.spines['left'].set_color(border_color)
        axin.spines['left'].set_linewidth(border_thickness)


        for im in axin.get_images():
            im.set_clim(vmin=np.min(image), vmax=np.max(image))
            
        for grid_point in grid_points:
            grid_y, grid_x = grid_point
            if grid_x < start_x or grid_x > stop_x:
                continue
            if grid_y < start_y or grid_y > stop_y:
                continue

            axin.plot(grid_x - start_x, grid_y - start_y, color=grid_color, marker=grid_marker, markersize=grin_marker_size)

    
        

    return fig




def main():
    plot_dots()

if __name__ == "__main__":
    main()



