from pyFPM.experimental.plot_illumination import (plot_bright_field_images_with_BF_edge_internal,
                                                  plot_bright_field_images_internal,
                                                  calculate_BF_edge)
from pyFPM.setup.Data import Data_patch
from pyFPM.setup.Imaging_system import LED_calibration_parameters
from pyFPM.setup.Setup_parameters import Setup_parameters
from arrow import Arrow_style, Arrow_text, add_arrow
from BF_simulations import get_200

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
from pathlib import Path
from skimage.feature import canny
from skimage.filters import threshold_otsu



main_result_folder = Path.cwd() / "results" / "master_thesis"
illustration_folder = main_result_folder / "illustrations"
illustration_folder.mkdir(parents=True, exist_ok=True)

def illustrate_single_calibration_from_simulation():
    data_patch, setup_parameters, calibration_parameters = get_200()

    fig = illustrate_single_calibration(data_patch=data_patch, setup_parameters=setup_parameters,
                                        calibration_parameters=calibration_parameters, array_size=5)

    fig.savefig(illustration_folder / "illustrate_single_calibration.pdf")




def illustrate_single_calibration(data_patch: Data_patch, setup_parameters: Setup_parameters, 
                                  calibration_parameters, array_size):
    image_downsampling = 4
    edge_points_per_image= get_edge_points(data_patch, image_downsampling)    

    fig = plt.figure(figsize=(13,4.7), constrained_layout=False)
    gs = fig.add_gridspec(7, 20)

    axes_dummy_1 = plt.subplot(gs[0:1, 0:20])
    axes_dummy_1.set_axis_off()
    axes_dummy_2 = plt.subplot(gs[6:7, 0:20])
    axes_dummy_2.set_axis_off()

    subfig_0 = fig.add_subfigure(gs[1:6, 0:5])
    subfig_1 = fig.add_subfigure(gs[1:6, 5:10])
    subfig_2 = fig.add_subfigure(gs[1:6, 10:15])
    subfig_3 = fig.add_subfigure(gs[1:6, 15:20])
    axes_0 = subfig_0.subplots(nrows=array_size, ncols=array_size)
    axes_1 = subfig_1.subplots(nrows=array_size, ncols=array_size)
    axes_2 = subfig_2.subplots(nrows=array_size, ncols=array_size)
    axes_3 = subfig_3.subplots(nrows=1, ncols=1)
    
    

    plot_bright_field_images_internal(axes_0, data_patch, setup_parameters, array_size)
    plot_only_edgepoints(axes_1, data_patch, setup_parameters, edge_points_per_image, array_size)
    plot_bright_field_images_with_BF_edge_internal(axes_2, data_patch, setup_parameters, calibration_parameters, array_size)
    axes_3.set_axis_off()
    axes_3.annotate(text="With the optimized"+"\n"+"parameter values"+"\n"+"yielding a precise"+"\n"+"description of"+"\n"+"the BF edge",
                    xy=(0.5,0.5), xytext=(0.5,0.5), textcoords="axes fraction", va="center", ha="center", fontsize=20)


    subfig_0.suptitle("Calibration dataset")
    # subfig_3.suptitle("Final result")


    #add arrows
    arrow_style_over = Arrow_style(
        face_color = "r",
        edge_color = "k",
        connection_style = "arc3, rad=-0.2",
        arrow_style = "simple",
        alpha = 0.7,
        mutation_scale = 30
    )

    arrow_style_under = Arrow_style(
        face_color = "r",
        edge_color = "k",
        connection_style = "arc3, rad=0.2",
        arrow_style = "simple",
        alpha = 0.7,
        mutation_scale = 30
    )

    arrow_text_1 = Arrow_text(
        text = "Edge point localization",
        relative_x = 0,
        relative_y = -0.1,
        font_size = "large"
    )

    arrow_text_2 = Arrow_text(
        text = "Non-linear optimization",
        relative_x = 0,
        relative_y = 0.1,
        font_size = "large"
    )


    add_arrow(fig=fig, ax_from=subfig_0, ax_to=subfig_1,
              coord_from=(0.6, -0.02), 
              coord_to=(0.4, -0.02),
              arrow_style=arrow_style_under, 
              arrow_text=arrow_text_1,
              axes_coordinates = True,
              axes_are_subfigures = True
              )
    add_arrow(fig=fig, ax_from=subfig_1, ax_to=subfig_2,
              coord_from=(0.6, 1.02), 
              coord_to=(0.4, 1.02),
              arrow_style=arrow_style_over, 
              arrow_text=arrow_text_2,
              axes_coordinates = True,
              axes_are_subfigures = True
              )


    return fig


def get_edge_points(data_patch: Data_patch, image_downsampling):
    otsu_power = 2
    canny_sigma = 10
    downsample_edges = 10

    images = data_patch.amplitude_images[:]**2
    images = images[:, ::image_downsampling, ::image_downsampling]
    threshold = threshold_otsu(images**otsu_power)**(1/otsu_power)

    edges_per_image = []
     
    for image in images:
        binary = (image >= threshold)
        edge_image = canny(binary, sigma=canny_sigma)
        edge_points = np.flip(np.transpose(edge_image.nonzero()), axis=1)
        edge_points = edge_points[np.where(edge_points[:,0]>canny_sigma)]
        edge_points = edge_points[np.where(edge_points[:,1]>canny_sigma)]
        edge_points = edge_points[np.where(edge_points[:,0]<image.shape[1]-canny_sigma-1)]
        edge_points = edge_points[np.where(edge_points[:,1]<image.shape[0]-canny_sigma-1)]

        edges_per_image.append(edge_points[::downsample_edges,:]*image_downsampling)
    
    return edges_per_image

def plot_only_edgepoints(axes, data_patch: Data_patch, setup_parameters: Setup_parameters, 
                         edge_points_per_image, 
                         array_size: int):
    LED_indices = data_patch.LED_indices
    center_indices = setup_parameters.LED_info.center_indices
    center_x = center_indices[0]
    center_y = center_indices[1]
    y_min = center_y - array_size//2
    x_min = center_x - array_size//2
    y_max = y_min + array_size
    x_max = x_min + array_size

    max_intensity = 10000 * np.max(data_patch.amplitude_images)**2

    for image_nr, (indices, edge_points) in enumerate(zip(LED_indices, edge_points_per_image)):
        x,y = indices
        if x>=x_min and x<x_max and y>=y_min and y<y_max:
            m = (array_size-1) - (y_max-y-1)
            n = (array_size-1) - (x_max-x-1)

            axes[m,n].matshow(data_patch.amplitude_images[image_nr]**2, vmin=0, vmax=max_intensity)
            axes[m,n].axis("off")

            axes[m,n].scatter(edge_points[:,0],edge_points[:,1], marker=".", s=3, color="r")


            

if __name__ == "__main__": 
    illustrate_single_calibration_from_simulation()
    plt.show()




