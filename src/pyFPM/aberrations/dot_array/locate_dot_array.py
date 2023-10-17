from pyFPM.aberrations.dot_array.Dot_array import Dot_array

import numpy as np
from skimage.feature import blob_log
from scipy.spatial.transform import Rotation

def locate_dots(image, dot_array: Dot_array, pixel_size, sub_precision):
    inverted_image = np.max(image) - image
    
    dot_radius = dot_array.diameter/2
    pixel_radius = dot_radius/pixel_size
    sigma_factor = 0.8
    sigma = sigma_factor * pixel_radius

    # find blobs with Laplacian of Gaussian algorithm
    blobs_LoG = blob_log(inverted_image, min_sigma=sigma, max_sigma=sigma, num_sigma=1, threshold_rel=.1)
    blobs_LoG[:, 2] = blobs_LoG[:, 2] * np.sqrt(2) # converts the returned sigma into a radius equivalent

    filtered_blobs = filter_blobs(blobs=blobs_LoG,
                                  filter_edge=True,
                                  pixel_radius=pixel_radius,
                                  image_shape=image.shape)
    
    filtered_blobs = get_precise_location(image=inverted_image,
                                          blobs=filtered_blobs,
                                          low_res_sigma=sigma,
                                          scaling_factor=sub_precision)
    
    return filtered_blobs

def filter_blobs(blobs, filter_edge, pixel_radius, image_shape):
    # filtering
    filtered_blobs = []
    for blob in blobs:
        y, x, r = blob

        if filter_edge:
            # filter out blobs uncomfortably close to edge
            if y < 1.5 * pixel_radius:
                continue
            elif x < 1.5 * pixel_radius:
                continue
            elif y > image_shape[0] - 1.5 * pixel_radius:
                continue
            elif x > image_shape[1] - 1.5 * pixel_radius:
                continue
        
        filtered_blobs.append(blob)

    return np.array(filtered_blobs)

def increase_pixel_count(image, scaling_factor):
    ones = np.ones(shape = (scaling_factor, scaling_factor))
    return np.kron(image, ones)

def get_precise_location(image, blobs, low_res_sigma, scaling_factor):
    high_pixel_count_sigma = low_res_sigma * scaling_factor

    precise_blobs = []

    for blob in blobs:
        y, x, _ = blob
        delta = 1.5 * low_res_sigma
        y_min, y_max = int(y-delta), int(y+delta)
        x_min, x_max = int(x-delta), int(x+delta)
        
        sub_image = image[y_min:y_max, x_min:x_max]
        high_pixel_count_sub_image = increase_pixel_count(image=sub_image, scaling_factor=scaling_factor)
        
        precise_blob_sub_location = blob_log(image=high_pixel_count_sub_image, 
                                     min_sigma=high_pixel_count_sigma, 
                                     max_sigma=high_pixel_count_sigma,
                                     num_sigma=1, 
                                     threshold_rel=.1)[0]
        
        # downscale to low res pixel values, where the subvalues within a pixel goes from -0.5 to 0.5
        precise_blob = precise_blob_sub_location / scaling_factor + np.array([y_min-0.5, x_min-0.5, 0])

        precise_blobs.append(precise_blob)


    return np.array(precise_blobs) 


def assemble_dots_in_grid(image_size, blobs, dot_spacing, pixel_size):
    rotation_tolerance = 1e-3 # degrees

    # do not care about radius, but will need a z=0 coordinate
    blobs = blobs * np.array([1, 1, 0]) 
    
    # note that image_size is in x, y
    dot_spacing_pixels = dot_spacing / pixel_size

    # find central blob to define as (0, 0)
    image_center_coords = np.array([image_size[1]//2,image_size[0]//2]) # y, x
    distances_from_center_squared = (blobs[:,0]-image_center_coords[0])**2 + (blobs[:,1]-image_center_coords[1])**2
    center_blob_index = np.argmin(distances_from_center_squared)
    center_blob_coords = blobs[center_blob_index]
    
    # create untilted grid of expected dot positions/coordinates in pixels
    array_size_buffer = 2
    dot_array_size = (np.array(image_size)*pixel_size/dot_spacing + array_size_buffer).astype(np.int16) # size of grid to map onto
    center_dot_index_Y = dot_array_size[0]//2
    center_dot_index_X = dot_array_size[1]//2
    untilted_grid = np.zeros(shape=(dot_array_size[1], dot_array_size[0], 3))  # indexes Y, X plus y, x, z coords
    for Y in range(dot_array_size[1]):
        for X in range(dot_array_size[0]):
            y_coord = (Y - center_dot_index_Y) * dot_spacing_pixels
            x_coord = (X - center_dot_index_X) * dot_spacing_pixels
            untilted_grid[Y, X] = np.array([y_coord, x_coord, 0])

    blobs = blobs - center_blob_coords # shift coordinate system to have center most blob in the center
    blobs = blobs[np.argsort(distances_from_center_squared)] # sort by distance from center

    total_rotation = 0
    tilted_grid = untilted_grid
    grid_points = np.zeros(shape = blobs.shape)
    grid_indices = np.zeros(shape = (blobs.shape[0],2), dtype=np.int16)
    for i, blob in enumerate(blobs):
        blob_y, blob_x, _ = blob
        grid_points[i], grid_indices[i] = get_closest_grid_point(tilted_grid, blob_y, blob_x)
        if i > 0:
            estimated_rotation, _ = Rotation.align_vectors(blobs[:i+1], grid_points[:i+1])
            additional_rotation = estimated_rotation.as_rotvec(degrees=True)[2]
            if np.abs(additional_rotation) > rotation_tolerance:
                total_rotation += additional_rotation
                rotation_matrix = get_rotation_matrix(additional_rotation)
                grid_points = grid_points.dot(rotation_matrix)
                tilted_grid = tilted_grid.dot(rotation_matrix)

    # shift coordinate system back
    blobs = blobs + center_blob_coords
    grid_points = grid_points + center_blob_coords

    # strip z coordinates
    blobs = blobs[:,:2]
    grid_points = grid_points[:,:2]

    return blobs, grid_points, grid_indices, total_rotation



def get_closest_grid_point(grid, y, x):
    distance_from_point_squared = (grid[:,:,0]-y)**2 + (grid[:,:,1]-x)**2
    index = np.argmin(distance_from_point_squared)
    Y, X = np.unravel_index(index, grid.shape[0:2])
    return grid[Y,X], np.array([Y, X], dtype=np.int16)



def get_rotation_matrix(degrees):
    # matrix for rotating image coordinates y, x clocwise
    cos = np.cos(degrees*np.pi/180)
    sin = np.sin(degrees*np.pi/180)
    rotation_matrix = [[cos,  sin, 0],
                       [-sin, cos, 0],
                       [  0,    0, 1]]
    
    return np.array(rotation_matrix)