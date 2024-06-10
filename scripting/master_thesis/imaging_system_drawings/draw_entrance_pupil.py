import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Ellipse
import numpy as np
from pathlib import Path


main_result_folder = Path.cwd() / "results" / "master_thesis"
illustration_folder = main_result_folder / "illustrations"
illustration_folder.mkdir(parents=True, exist_ok=True)

colors = ["mediumseagreen", "firebrick", "deepskyblue"]

def draw_imaging_systems():
    magnification = 2
    numerical_aperture = 0.05
    focal_length = 60e-3
    
    relative_a_1_values = [0, 1, 1/2, 2]
    z_1_annotations = ["$f_{L1}$","$f_{L1}$","$f_{L1}$","$f_{L1}$"]
    a_1_annotations = ["","$f_{L1}$","$f_{L1}/2$","$2f_{L1}$"]
    z_q_annotations = ["$z_q=f_{L1}$", "$z_q=\infty$", "$z_q=2f_{L1}$", "$z_q=-f_{L1}$"]

    for diagram_nr in range(len(relative_a_1_values)):
        fig, ax = plt.subplots(1,1, figsize=(5,2), constrained_layout=True)

        z_1 = focal_length*(1+1/magnification)
        first_focal_length = z_1
        aperture_radius = numerical_aperture * first_focal_length
        a_1 = relative_a_1_values[diagram_nr] * first_focal_length
        if a_1 == 0:
            entrance_pupil = z_1
        elif a_1 == z_1:
            entrance_pupil = np.inf
        else:
            entrance_pupil = 1/(1/first_focal_length-a_1/first_focal_length**2)
        
        first_lens_plane_z = -a_1
        object_plane_z = -z_1-a_1
        aperture_plane_z = 0
        if entrance_pupil != np.inf:
            entrance_pupil_plane_z = object_plane_z + entrance_pupil
        else: 
            entrance_pupil_plane_z = object_plane_z + 3* first_focal_length
        object_points = [-1.5*aperture_radius, 0, 1.5*aperture_radius]
        lens_and_aperture_width = 0.01*(np.max([np.abs(entrance_pupil_plane_z-object_plane_z), np.abs(entrance_pupil_plane_z-aperture_plane_z)]))

        draw_planes(ax, object_plane_z, aperture_plane_z, first_lens_plane_z, entrance_pupil_plane_z)
        draw_lens(ax, aperture_radius, aperture_plane_z, first_lens_plane_z, first_focal_length, lens_and_aperture_width)
        draw_aperture(ax, aperture_radius, aperture_plane_z, lens_and_aperture_width)
        draw_entrance_pupil(ax, aperture_radius, entrance_pupil_plane_z, lens_and_aperture_width)
        
        # draw rays
        for color, object_point in zip(colors, object_points):
            image_point = - magnification * object_point
            
            if a_1 == 0:
                z_vals = [object_plane_z, aperture_plane_z]
            else:
                z_vals = [object_plane_z, first_lens_plane_z, aperture_plane_z]



            lines = [[], [], []]
            aperture_intersects =  [-aperture_radius, 0 , aperture_radius]

            for aperture_intersect, line in zip(aperture_intersects, lines):
                line.append(object_point)
                if a_1 != 0:
                    line.append(calculate_lens_y(object_point, aperture_intersect, z_1, a_1, first_focal_length)) 
                line.append(aperture_intersect)


            for line in lines:
                ax.plot(z_vals, line, color=color, zorder=4)

            for aperture_intersect, line in zip(aperture_intersects, lines):
                if aperture_intersect == 0:
                    if entrance_pupil != np.inf:
                        ax.plot([first_lens_plane_z, entrance_pupil_plane_z], [line[1], 0], color=color, zorder=4, linestyle="dashed")
                    else:
                        ax.plot([first_lens_plane_z, entrance_pupil_plane_z], [line[1], line[1]], color=color, zorder=4, linestyle="dashed")

            ax.fill_between(z_vals, lines[0], lines[-1], color=color, alpha=0.5, zorder=4)

            ax.scatter(x=object_plane_z, y=object_point, color=color, s=10)
        ax.set_axis_off()

        # distance annotation height
        height = 20e-3
        aperture_annotation_heigth = -19e-3
        z_q_height = -24e-3
        
        # annotate z_1
        width = z_1
        ax.annotate("", xy=(object_plane_z, height), xytext=(first_lens_plane_z, height), textcoords=ax.transData, arrowprops=dict(arrowstyle='<->'))
        bbox=dict(fc="white", ec="none")
        ax.text(object_plane_z+width/2, height, z_1_annotations[diagram_nr], ha="center", va="center", bbox=bbox)

        if a_1 != 0:
            # annotate a_1
            width = a_1
            ax.annotate("", xy=(first_lens_plane_z, height), xytext=(aperture_plane_z, height), textcoords=ax.transData, arrowprops=dict(arrowstyle='<->'))
            bbox=dict(fc="white", ec="none")
            ax.text(first_lens_plane_z+width/2, height, a_1_annotations[diagram_nr], ha="center", va="center", bbox=bbox)

        # annotate z_q
        width = entrance_pupil
        ax.annotate("", xy=(entrance_pupil_plane_z, z_q_height), xytext=(object_plane_z, z_q_height), textcoords=ax.transData, arrowprops=dict(arrowstyle='<->'))
        bbox=dict(fc="white", ec="none")
        ax.text((object_plane_z + entrance_pupil_plane_z)/2, z_q_height, z_q_annotations[diagram_nr], ha="center", va="center", bbox=bbox)

        # annotate AS and EnP
        bbox=dict(fc="white", ec="none", pad=0)
        if np.abs(aperture_plane_z - entrance_pupil_plane_z) < 10e-9:
            ax.text(entrance_pupil_plane_z, aperture_annotation_heigth, "AS/EnP", ha="center", va="center", bbox=bbox)
        else:
            ax.text(entrance_pupil_plane_z, aperture_annotation_heigth, "EnP", ha="center", va="center", bbox=bbox)
            ax.text(aperture_plane_z, aperture_annotation_heigth, "AS", ha="center", va="center", bbox=bbox)




        ax.set_ylim(-28e-3, 23e-3)




        fig.savefig(illustration_folder / f"illustrate_entrance_pupil_{diagram_nr}.pdf")

def calculate_lens_y(first_y, second_y, first_distance, second_distance, focal_length):
    return (second_y+first_y*(second_distance/first_distance))/(1+second_distance/first_distance-second_distance/focal_length)




def draw_planes(ax, object_plane_z, aperture_plane_z, first_lens_plane_z, entrance_pupil_plane_z):
    ax.axvline(x=object_plane_z, zorder=0, color="gray", linestyle="--")
    ax.axvline(x=aperture_plane_z, zorder=0, color="gray", linestyle="--")

    if first_lens_plane_z != aperture_plane_z:
        ax.axvline(x=first_lens_plane_z, zorder=0, color="gray", linestyle="--")
    if entrance_pupil_plane_z != aperture_plane_z:
        ax.axvline(x=entrance_pupil_plane_z, zorder=0, color="gray", linestyle="--")




def draw_lens(ax, aperture_radius, aperture_plane_z, lens_plane_z, focal_length, lens_width):
    if focal_length == np.inf:
        return # in this case the lens does not actually exist
    
    if aperture_plane_z == lens_plane_z:
        lens_radius = aperture_radius
        ax.add_artist(Rectangle(xy=(lens_plane_z-0.5*lens_width, -lens_radius), 
            width=lens_width, height=2*lens_radius, color="mediumturquoise", zorder=5))
    else:
        lens_radius = 20e-3
        ax.add_artist(Ellipse(xy=(lens_plane_z, 0), 
            width=lens_width, height=2*lens_radius, color="mediumturquoise", zorder=5))
        # ax.add_artist(Rectangle(xy=(lens_plane_z-0.5*lens_width, -lens_radius), 
        #     width=lens_width, height=2*lens_radius, color="mediumturquoise"))


def draw_aperture(ax, aperture_radius, aperture_plane_z, aperture_width):
    aperture_edge_width = aperture_width * 2
    aperture_height = 0.4*aperture_radius
    aperture_edge_height = 0.15*aperture_height
    aperture_y = aperture_radius + aperture_height*0.5
    aperture_edge_y = aperture_radius + aperture_edge_height*0.5
    
    ax.add_artist(Rectangle(xy=(aperture_plane_z-0.5*aperture_width, aperture_y-aperture_height*0.5), 
                            width=aperture_width, height=aperture_height, color="k", zorder=5))
    ax.add_artist(Rectangle(xy=(aperture_plane_z-0.5*aperture_width, -aperture_y-aperture_height*0.5), 
                            width=aperture_width, height=aperture_height, color="k", zorder=5))
    ax.add_artist(Rectangle(xy=(aperture_plane_z-0.5*aperture_edge_width, aperture_edge_y-aperture_edge_height*0.5), 
                            width=aperture_edge_width, height=aperture_edge_height, color="k", zorder=5))
    ax.add_artist(Rectangle(xy=(aperture_plane_z-0.5*aperture_edge_width, -aperture_edge_y-aperture_edge_height*0.5), 
                            width=aperture_edge_width, height=aperture_edge_height, color="k", zorder=5))
    

def draw_entrance_pupil(ax, aperture_radius, aperture_plane_z, aperture_width):
    aperture_radius = 2 * aperture_radius
    aperture_width = 2 * aperture_width

    aperture_edge_width = aperture_width * 2
    aperture_height = 0.4*aperture_radius
    aperture_edge_height = 0.15*aperture_height
    aperture_y = aperture_radius + aperture_height*0.5
    aperture_edge_y = aperture_radius + aperture_edge_height*0.5
    
    ax.add_artist(Rectangle(xy=(aperture_plane_z-0.5*aperture_width, aperture_y-aperture_height*0.5), 
                            width=aperture_width, height=aperture_height, color="gray", zorder=5))
    ax.add_artist(Rectangle(xy=(aperture_plane_z-0.5*aperture_width, -aperture_y-aperture_height*0.5), 
                            width=aperture_width, height=aperture_height, color="gray", zorder=5))
    ax.add_artist(Rectangle(xy=(aperture_plane_z-0.5*aperture_edge_width, aperture_edge_y-aperture_edge_height*0.5), 
                            width=aperture_edge_width, height=aperture_edge_height, color="gray", zorder=5))
    ax.add_artist(Rectangle(xy=(aperture_plane_z-0.5*aperture_edge_width, -aperture_edge_y-aperture_edge_height*0.5), 
                            width=aperture_edge_width, height=aperture_edge_height, color="gray", zorder=5))
    

if __name__ == "__main__": 
    draw_imaging_systems()
    plt.show()