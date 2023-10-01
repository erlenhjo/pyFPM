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
     

def locate_dots(image, dot_radius, pixel_size):
    inverted_image = np.max(image) - image
    
    pixel_radius = dot_radius/pixel_size

    # find blobs with Laplacian of Gaussian algorithm
    blobs_LoG = blob_log(inverted_image, min_sigma=pixel_radius/2, max_sigma=pixel_radius, num_sigma=10, threshold=.1)
    blobs_LoG[:, 2] = blobs_LoG[:, 2] * np.sqrt(2) # converts the returned sigma into a radius equivalent

    # find blobs with Difference of Gaussian algorithm
    blobs_DoG = blob_dog(inverted_image, min_sigma=pixel_radius/2, max_sigma=pixel_radius, threshold=.1)
    blobs_DoG[:, 2] = blobs_DoG[:, 2] * np.sqrt(4) # converts the returned sigma into a radius equivalent

    # filtering
    filtered_blobs = []
    for blob in blobs_DoG:
        y, x, r = blob

        # filter out blobs uncomfortably close to edge
        if y < 1.5 * pixel_radius:
            continue
        elif x < 1.5 * pixel_radius:
            continue
        elif y > image.shape[0] - 1.5 * pixel_radius:
            continue
        elif x > image.shape[1] - 1.5 * pixel_radius:
            continue

        # filter out blobs where the two methods do not get the same result
        potential_indices_y = np.argwhere(blobs_LoG[:,0]==np.array(y))
        potential_indices_x = np.argwhere(blobs_LoG[:,1]==np.array(x))
        for index_y in potential_indices_y:
            for index_x in potential_indices_x:
                if index_x == index_y:
                    filtered_blobs.append(blob)


    return np.array(filtered_blobs)
    
    
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

    plt.show()

def assemble_dots_in_grid(image_size, blobs, dot_spacing, pixel_size):
    # note that image_size is in x, y
    dot_spacing_pixels = dot_spacing / pixel_size

    # find central blob to define as (0, 0)
    image_center_coords = np.array([image_size[1]//2,image_size[0]//2]) # y, x
    distances_from_center_squared = (blobs[:,0]-image_center_coords[0])**2 + (blobs[:,1]-image_center_coords[1])**2
    center_blob_index = np.argmin(distances_from_center_squared)
    center_blob = blobs[center_blob_index]
    shift_y = center_blob[0]
    shift_x = center_blob[1]
    array_size_buffer = 2
    dot_array_size = (np.array(image_size)*pixel_size/dot_spacing + array_size_buffer).astype(np.int16) # size of grid to map onto
    center_dot_index_Y = dot_array_size[0]//2
    center_dot_index_X = dot_array_size[1]//2

    # create untilted grid of expected dot positions/coordinates in pixels
    untilted_grid = np.zeros(shape=(dot_array_size[1], dot_array_size[0], 2))  # indexes Y, X plus y, x coords
    for Y in range(dot_array_size[1]):
        for X in range(dot_array_size[0]):
            y_coord = (center_dot_index_Y - Y) * dot_spacing_pixels
            x_coord = (center_dot_index_X - X) * dot_spacing_pixels
            untilted_grid[Y, X] = np.array([y_coord, x_coord])

    shifted_blobs = blobs - np.array([shift_y, shift_x, 0])

    total_tilt = 0
    tilted_grid = untilted_grid
    blobs_with_grid_positions = np.zeros(shape=(shifted_blobs.shape[0],4), dtype=np.int16) # (y, x, Y, X)
    for i, blob in enumerate(shifted_blobs):
        y, x, r = blob
        Y, X = get_closest_grid_point(tilted_grid, y, x)
        blobs_with_grid_positions[i] = np.array([y,x,Y,X], dtype=np.int16)
        
        #rotation_matrix = get_rotation_matrix(0)
        #tilted_grid = np.matmul(untilted_grid, rotation_matrix)

    blob_present_filter = np.zeros(shape=(dot_array_size[1], dot_array_size[0], 2))  # indexes Y, X, True/False if blob occupies grid position
    for blob in blobs_with_grid_positions:
        y,x,Y,X = blob
        blob_present_filter[Y, X] = [1, 1]
    
    shifted_grid = tilted_grid + np.array([shift_y, shift_x])
    filtered_grid = shifted_grid * blob_present_filter

    final_blob_grid = 0#blob_grid + np.array([shift_y, shift_x])

    return final_blob_grid, filtered_grid 

def get_rotation_matrix(degrees):
    # matrix for rotating image coordinates y, x clocwise
    cos = np.cos(degrees*np.pi/180)
    sin = np.sin(degrees*np.pi/180)
    rotation_matrix = [[sin, cos],
                       [cos, -sin]]
    
    return np.array(rotation_matrix)

def get_closest_grid_point(grid, y, x):
    distance_from_point_squared = (grid[:,:,0]-y)**2 + (grid[:,:,1]-x)**2
    index = np.argmin(distance_from_point_squared)
    Y, X = np.unravel_index(index, grid.shape[0:2])
    return Y, X

def plot_located_dots_vs_grid(image, detected_blobs, grid):
    colors = ["red", "lime"]
    markers = ["x", "+"]

    fig, ax = plt.subplots()
    ax.imshow(image)
    ax.set_title("Dots vs. grid")

    blob_color = colors[0]
    blob_marker = markers[0]
    for blob in detected_blobs:
        y, x, r = blob
        ax.plot(x, y, color=blob_color, marker=blob_marker)

    grid_color = colors[1]
    grid_marker = markers[1]
    grid_size = grid.shape
    image_size = image.shape
    for Y in range(grid_size[0]):
        for X in range(grid_size[1]):
            y, x = grid[Y, X]
            if y < 0 or x < 0 or y > image_size[0] or x > image_size[1]:
                continue
            else:
                ax.plot(x, y, color=grid_color, marker=grid_marker)

    ax.set_axis_off()

    plt.show()

