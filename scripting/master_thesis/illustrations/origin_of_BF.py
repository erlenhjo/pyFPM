import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
from pathlib import Path
from matplotlib.colors import LinearSegmentedColormap

from pyFPM.experimental.plot_illumination import calculate_BF_edge
from BF_simulations import get_200, get_150, get_175

midnight_purple = [28/256,1/256,37/256]
colors = ["mediumseagreen", "firebrick", "deepskyblue"]

v_min = 0
v_max = 1.2

cm0 = LinearSegmentedColormap.from_list(
            "BlackToRed", [midnight_purple, colors[0]], N=1024)
cm1 = LinearSegmentedColormap.from_list(
            "BlackToGreen", [midnight_purple, colors[1]], N=1024)
cm2 = LinearSegmentedColormap.from_list(
            "BlackToBlue", [midnight_purple, colors[2]], N=1024)

color_maps = [cm0, cm1, cm2]

main_result_folder = Path.cwd() / "results" / "master_thesis"
illustration_folder = main_result_folder / "illustrations"
illustration_folder.mkdir(parents=True, exist_ok=True)

def illustrate_BF_origin():
    
    fig1, main_axes = plt.subplots(3,1, figsize=(6.5,5.5), sharex=True, sharey=True, constrained_layout=True)
    fig2 = plt.figure(figsize = (3, 4), constrained_layout = True)
    image_subfigs = fig2.subfigures(nrows=3,ncols=1,height_ratios=[1,1,1])

    data_functions = [get_200, get_175, get_150]
    for diagram_nr, (data_function, ax, image_subfig) in enumerate(zip(data_functions, main_axes, image_subfigs)):

        data_patch, setup_parameters, calibration_parameters = data_function()
        magnification = setup_parameters.lens.magnification
        numerical_aperture = setup_parameters.lens.NA
        focal_length = setup_parameters.lens.focal_length
        z_0 = calibration_parameters.LED_distance
        z_1 = focal_length*(1+1/magnification)
        z_2 = focal_length*(1+magnification)
        lens_radius = numerical_aperture * z_1
        detector_height = setup_parameters.camera.raw_image_size[1] * setup_parameters.camera.camera_pixel_size
        lens_plane_z = 0
        object_plane_z = -z_1
        LED_plane_z = -(z_1+z_0) 
        image_plane_z = z_2

        # generate axes and set title for BF image subfig   
        image_axes = image_subfig.subplots(nrows=1,ncols=3)
        image_subfig.suptitle(f"$z_0$={z_0*1000:.0f} mm")
        
        # draw planes
        ax.axvline(x=lens_plane_z, zorder=0, color="gray", linestyle="--")
        ax.axvline(x=object_plane_z, zorder=0, color="gray", linestyle="--")
        ax.axvline(x=LED_plane_z, zorder=0, color="gray", linestyle="--")
        ax.axvline(x=image_plane_z, zorder=0, color="gray", linestyle="--")

        # draw lens
        lens_width = lens_radius*0.7
        aperture_width = lens_width
        aperture_edge_width = aperture_width * 2
        aperture_height = 0.4*lens_radius
        aperture_edge_height = 0.15*aperture_height
        aperture_y = lens_radius + aperture_height*0.5
        aperture_edge_y = lens_radius + aperture_edge_height*0.5
        ax.add_artist(Rectangle(xy=(lens_plane_z-0.5*lens_width, -lens_radius), 
                        width=lens_width, height=2*lens_radius, color="mediumturquoise"))
        ax.add_artist(Rectangle(xy=(lens_plane_z-0.5*aperture_width, aperture_y-aperture_height*0.5), 
                                width=aperture_width, height=aperture_height, color="k"))
        ax.add_artist(Rectangle(xy=(lens_plane_z-0.5*aperture_width, -aperture_y-aperture_height*0.5), 
                                width=aperture_width, height=aperture_height, color="k"))
        ax.add_artist(Rectangle(xy=(lens_plane_z-0.5*aperture_edge_width, aperture_edge_y-aperture_edge_height*0.5), 
                                width=aperture_edge_width, height=aperture_edge_height, color="k"))
        ax.add_artist(Rectangle(xy=(lens_plane_z-0.5*aperture_edge_width, -aperture_edge_y-aperture_edge_height*0.5), 
                                width=aperture_edge_width, height=aperture_edge_height, color="k"))

        # draw detector
        detector_width = 0.5*lens_width
        ax.add_artist(Rectangle(xy=(image_plane_z-0.5*detector_width, -0.5*detector_height),
                                width=detector_width, height=detector_height, color="black"))
        
        # # draw object FoV
        # object_FoV_height = detector_height/magnification
        # object_FoV_width = detector_width
        # ax.add_artist(Rectangle(xy=(object_plane_z-0.5*object_FoV_width, -0.5*object_FoV_height),
        #                         width=object_FoV_width, height=object_FoV_height, color="gray"))

        # draw LED and rays
        LED_m_vals = [0, 1, 2]
        LED_n = 0
        for LED_m, color, color_map, image_ax in zip(LED_m_vals, colors, color_maps, image_axes):
            LED_y = setup_parameters.LED_info.LED_pitch * LED_m

            relative_indicies = [LED_n, LED_m]
            center_indices = setup_parameters.LED_info.center_indices 
            indices = np.array(center_indices)+np.array(relative_indicies)
            for k, (x,y) in enumerate(data_patch.LED_indices):
                if x==indices[0] and y==indices[1]:
                    image_nr = k
                    break

            BF_center_pixels, BF_radius_pixels = calculate_BF_edge(setup_parameters=setup_parameters,
                                                            calibration_parameters=calibration_parameters,
                                                            LED_n=LED_n, LED_m=LED_m)
            BF_center_detector = -BF_center_pixels[1] * setup_parameters.camera.camera_pixel_size + detector_height/2
            BF_radius_detector = -BF_radius_pixels * setup_parameters.camera.camera_pixel_size
            BF_center_object = -BF_center_detector / magnification
            BF_radius_object = -BF_radius_detector / magnification


            z_vals = [LED_plane_z, object_plane_z, lens_plane_z, image_plane_z]
            upper_line = [LED_y, BF_center_object+BF_radius_object,
                        lens_radius, BF_center_detector+BF_radius_detector]
            central_line = [LED_y, BF_center_object,
                        0, BF_center_detector]
            lower_line = [LED_y, BF_center_object-BF_radius_object,
                        -lens_radius, BF_center_detector-BF_radius_detector]
            ax.plot(z_vals, upper_line, color=color, zorder=0)
            ax.plot(z_vals, central_line, color=color, zorder=0)
            ax.plot(z_vals, lower_line, color=color, zorder=0)
            ax.fill_between(z_vals, upper_line, lower_line, color=color, alpha=0.5, zorder=0)

            image_ax.matshow(data_patch.amplitude_images[image_nr], cmap=color_map, vmin=v_min, vmax=v_max)
            image_ax.set_axis_off()

            ax.scatter(x=LED_plane_z, y=LED_y, color=color, s=10)
        ax.set_axis_off()

        # annotatate LED distance
        width = z_0
        height = - 2 * setup_parameters.LED_info.LED_pitch
        ax.annotate("", xy=(LED_plane_z, height), xytext=(object_plane_z, height), textcoords=ax.transData, arrowprops=dict(arrowstyle='<->'))
        bbox=dict(fc="white", ec="none")
        ax.text(LED_plane_z+width/2, height, f"$z_0$={z_0*1000:.0f} mm", ha="center", va="center", bbox=bbox)

        # for first diagram only
        if diagram_nr == 0:
            # annotate z_1
            width = z_1
            height = - 2 * setup_parameters.LED_info.LED_pitch
            ax.annotate("", xy=(object_plane_z, height), xytext=(lens_plane_z, height), textcoords=ax.transData, arrowprops=dict(arrowstyle='<->'))
            bbox=dict(fc="white", ec="none")
            ax.text(object_plane_z+width/2, height, f"$z_1$={z_1*1000:.0f} mm", ha="center", va="center", bbox=bbox)

            # annotate z_2
            width = z_2
            height = - 2 * setup_parameters.LED_info.LED_pitch
            ax.annotate("", xy=(lens_plane_z, height), xytext=(image_plane_z, height), textcoords=ax.transData, arrowprops=dict(arrowstyle='<->'))
            bbox=dict(fc="white", ec="none")
            ax.text(lens_plane_z+width/2, height, f"$z_2$={z_2*1000:.0f} mm", ha="center", va="center", bbox=bbox)

            # annotate detector, lens and aperture, LED array and object
            offset=5e-3
            height = 1.7 * setup_parameters.LED_info.LED_pitch
            ax.text(image_plane_z+offset, 0, "Detector", ha="left", va="center", rotation=90)
            ax.text(lens_plane_z+offset, height, "Lens", ha="left", va="center", rotation=90)
            ax.text(object_plane_z+offset, height, "Object", ha="left", va="center", rotation=90)
            ax.text(LED_plane_z-offset, 0, "LED array", ha="right", va="center", rotation=90)


    fig1.savefig(illustration_folder / "illustrate_BF_origin_raytrace.pdf")
    fig2.savefig(illustration_folder / "illustrate_BF_origin_simulated_BF.pdf")


if __name__ == "__main__": 
    illustrate_BF_origin()
    plt.show()