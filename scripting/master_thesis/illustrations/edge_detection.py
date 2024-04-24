from pyFPM.experimental.plot_illumination import plot_bright_field_images_with_BF_edge
from pyFPM.NTNU_specific.simulate_images.only_illumination import simulate_illumination
from pyFPM.setup.Setup_parameters import Lens, Lens_type
from pyFPM.setup.Data import Data_patch
from pyFPM.setup.Setup_parameters import Setup_parameters
from pyFPM.setup.Imaging_system import LED_calibration_parameters
from pyFPM.NTNU_specific.components import IDS_U3_31J0CP_REV_2_2
from arrow import Arrow_style, Arrow_text, add_arrow

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from skimage.feature import canny
from skimage.filters import threshold_otsu


lens = Lens(
    NA = 0.05,
    magnification = 2,
    focal_length = 60e-3,
    working_distance = None,
    depth_of_field = None,
    max_FoV_sensor = None,
    lens_type = Lens_type.SINGLE_LENS
)
camera = IDS_U3_31J0CP_REV_2_2
array_size = 3

main_result_folder = Path.cwd() / "results" / "master_thesis"
illustration_folder = main_result_folder / "illustrations"
illustration_folder.mkdir(parents=True, exist_ok=True)

def illustrate_edge_detection_from_simulation(lens, camera,
                                              spherical, Fresnel, 
                                              z_LED, arraysize, 
                                              patch_offset=[0,0]):
    setup_parameters, data_patch, imaging_system, illumination_pattern, applied_pupil, high_res_complex_object\
       = simulate_illumination(lens = lens, 
                               camera = camera,
                               correct_spherical_wave_illumination = spherical, 
                               correct_Fresnel_propagation = Fresnel,
                               arraysize=arraysize,
                               calibration_parameters=LED_calibration_parameters(z_LED,0,0,0),
                               patch_offset=patch_offset)


    fig = illustrate_edge_detection(data_patch=data_patch, setup_parameters=setup_parameters)

    fig.savefig(illustration_folder / "illustrate_edge_detection.pdf")
    fig.savefig(illustration_folder / "illustrate_edge_detection.png")


def illustrate_edge_detection(data_patch: Data_patch, setup_parameters: Setup_parameters):
    otsu_power = 2
    canny_sigma = 10
    downsample_image = 4
    downsample_edges = 10

    images = data_patch.amplitude_images[:]**2
    images = images[:,::downsample_image, ::downsample_image]
    threshold = threshold_otsu(images**otsu_power)**(1/otsu_power)

    binarized_images = []
    edge_images = []
    edges_per_image = []
     
    for image in images:
        binary = (image >= threshold)
        binarized_images.append(binary)
        edge_image = canny(binary, sigma=canny_sigma)
        edge_images.append(edge_image)
        edge_points = np.flip(np.transpose(edge_image.nonzero()), axis=1)
        edge_points = edge_points[np.where(edge_points[:,0]>canny_sigma)]
        edge_points = edge_points[np.where(edge_points[:,1]>canny_sigma)]
        edge_points = edge_points[np.where(edge_points[:,0]<image.shape[1]-canny_sigma-1)]
        edge_points = edge_points[np.where(edge_points[:,1]<image.shape[0]-canny_sigma-1)]

        edges_per_image.append(edge_points[::downsample_edges,:])


    return plotting(image = images[2], binary_image = binarized_images[2], 
                    edge_image = edge_images[2], edge_points = edges_per_image[2])


def plotting(image, binary_image, edge_image, edge_points):
    fig = plt.figure(figsize=(10,4), constrained_layout=False)
    gs = fig.add_gridspec(7, 20)

    axes_0 = plt.subplot(gs[1:6, 0:5])
    axes_1 = plt.subplot(gs[1:6, 5:10])
    axes_2 = plt.subplot(gs[1:6, 10:15])
    axes_3 = plt.subplot(gs[1:6, 15:20])
    axes_dummy_1 = plt.subplot(gs[0:1, 0:20])
    axes_dummy_1.set_axis_off()
    axes_dummy_2 = plt.subplot(gs[6:7, 0:20])
    axes_dummy_2.set_axis_off()

    axes_0.imshow(image)
    axes_1.imshow(binary_image)
    axes_2.imshow(edge_image)
    axes_3.imshow(image)
    axes_3.scatter(edge_points[:,0],edge_points[:,1], marker=".", s=3, color="r")

    axes_0.set_title("Original image")
    axes_3.set_title("Detected edge points")

    axes_0.set_xticks([])
    axes_1.set_xticks([])
    axes_2.set_xticks([])
    axes_3.set_xticks([])
    axes_0.set_yticks([])
    axes_1.set_yticks([])
    axes_2.set_yticks([])
    axes_3.set_yticks([])

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
        text = "Otsu threshold and binarization",
        relative_x = 0,
        relative_y = -0.1,
        font_size = "large"
    )

    arrow_text_2 = Arrow_text(
        text = "Canny algorithm edge detection",
        relative_x = 0,
        relative_y = 0.1,
        font_size = "large"
    )

    arrow_text_3 = Arrow_text(
        text = "Conversion to individual points",
        relative_x = 0,
        relative_y = -0.1,
        font_size = "large"
    )


    # axes_0.set_xlim() # needed for some reason?
    # axes_0.set_ylim()
    # axes_1.set_xlim()
    # axes_1.set_ylim()
    # axes_2.set_xlim()
    # axes_2.set_ylim()
    # axes_3.set_xlim()
    # axes_3.set_ylim()

    fig.tight_layout()


    add_arrow(fig=fig, ax_from=axes_0, ax_to=axes_1,
              coord_from=(0.6, 0), 
              coord_to=(0.4, 0),
              arrow_style=arrow_style_under, 
              arrow_text=arrow_text_1,
              axes_coordinates = True
              )
    add_arrow(fig=fig, ax_from=axes_1, ax_to=axes_2,
              coord_from=(0.6, 1), 
              coord_to=(0.4, 1),
              arrow_style=arrow_style_over, 
              arrow_text=arrow_text_2,
              axes_coordinates = True
              )
    add_arrow(fig=fig, ax_from=axes_2, ax_to=axes_3,
              coord_from=(0.6, 0), 
              coord_to=(0.4, 0),
              arrow_style=arrow_style_under, 
              arrow_text=arrow_text_3,
              axes_coordinates = True
              )

    return fig



if __name__ == "__main__": 
    illustrate_edge_detection_from_simulation(lens=lens, camera=camera,
                                              spherical=True, Fresnel=True, 
                                              z_LED=200e-3, arraysize=array_size)
    plt.show()




