import numpy as np
from skimage.feature import blob_log, blob_dog
from dataclasses import dataclass
import matplotlib.pyplot as plt

@dataclass
class Dot_array(object):
    spacing: float
    spacing_tolerance: float
    diameter: float
    diameter_tolerance: float


EO_DOT_ARRAY = Dot_array(
    spacing = 125e-6,
    spacing_tolerance = 2e-6,
    diameter = 62.5e-6,
    diameter_tolerance = 2e-6  
)
            

def locate_dots(image, dot_radius, pixel_size):
    inverted_image = np.max(image) - image
    
    pixel_radius = dot_radius/pixel_size

    # find blobs with Laplacian of Gaussian algorithm
    blobs_LoG = blob_log(inverted_image, min_sigma=pixel_radius/2, max_sigma=pixel_radius, num_sigma=10, threshold=.1)
    blobs_LoG[:, 2] = blobs_LoG[:, 2] * np.sqrt(2) # converts the returned sigma into a radius equivalent

    # find blobs with Difference of Gaussian algorithm
    blobs_DoG = blob_dog(inverted_image, min_sigma=pixel_radius/2, max_sigma=pixel_radius, threshold=.1)
    blobs_DoG[:, 2] = blobs_DoG[:, 2] * np.sqrt(4) # converts the returned sigma into a radius equivalent


    return blobs_LoG, blobs_DoG
    
    
def plot_located_dots(image, blobs_list):
    colors = ["red", "lime", "green"]
    markers = ["o", "x", "+"]
    sequence = zip(blobs_list, colors[:len(blobs_list)], markers[:len(blobs_list)])

    fig, axes = plt.subplots(1, 2, figsize=(12, 6), sharex=True, sharey=True)
    ax=axes.ravel()
    ax[0].imshow(image)
    ax[1].imshow(image)
    ax[0].set_title("Centers")
    ax[1].set_title("Bounding circles")

    for (blobs, color, marker) in sequence:
        for blob in blobs:
            y, x, r = blob
            ax[0].plot(x,y,color=color, marker=marker)
            circle = plt.Circle((x, y), r, color=color, linewidth=2, fill=False)
            ax[1].add_patch(circle)

    ax[0].set_axis_off()
    ax[1].set_axis_off()

    plt.tight_layout()
    plt.show()


def get_dot_array_image(dot_radius, dot_spacing, pixel_number, nr_of_dots):

    dot_image = np.zeros(shape = (pixel_number, pixel_number))
    dot_blobs = []

    image_size = nr_of_dots * dot_spacing
    pixel_size = image_size / pixel_number

    positions = np.arange(pixel_number)*pixel_size

    X, Y = np.meshgrid(positions, positions)

    for y_dot in range(nr_of_dots):
        for x_dot in range(nr_of_dots):
            dot_center_x = (1/2 + x_dot) * dot_spacing
            dot_center_y = (1/2 + y_dot) * dot_spacing

            dot_image += (X-dot_center_x)**2 + (Y - dot_center_y)**2 < dot_radius**2
            dot_blobs.append([dot_center_x/pixel_size, dot_center_y/pixel_size, dot_radius/pixel_size])
                
    dot_image = 1-dot_image # invert as the dot array is an absorbtion target

    return dot_image, dot_blobs, pixel_size









