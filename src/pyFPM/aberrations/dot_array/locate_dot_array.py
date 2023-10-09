import numpy as np
from skimage.feature import blob_log, blob_dog
from scipy.spatial.transform import Rotation

def locate_dots(image, dot_radius, pixel_size):
    inverted_image = np.max(image) - image
    
    pixel_radius = dot_radius/pixel_size

    # find blobs with Laplacian of Gaussian algorithm
    blobs_LoG = blob_log(inverted_image, min_sigma=pixel_radius*0.6, max_sigma=pixel_radius*0.8, num_sigma=10, threshold=.1)
    blobs_LoG[:, 2] = blobs_LoG[:, 2] * np.sqrt(2) # converts the returned sigma into a radius equivalent

    # find blobs with Difference of Gaussian algorithm
    blobs_DoG = blob_dog(inverted_image, min_sigma=pixel_radius*0.6, max_sigma=pixel_radius*0.8, threshold=.1)
    blobs_DoG[:, 2] = blobs_DoG[:, 2] * np.sqrt(4) # converts the returned sigma into a radius equivalent

    filtered_blobs = filter_blobs(blobs_DoG=blobs_LoG, 
                                  blobs_LoG=blobs_LoG, 
                                  filter_edge=True,
                                  filter_identical=True,
                                  pixel_radius=pixel_radius,
                                  image_shape=image.shape)
    
    return [filtered_blobs, blobs_LoG, blobs_DoG]

def filter_blobs(blobs_DoG, blobs_LoG, filter_edge, filter_identical, pixel_radius, image_shape):
    # filtering
    filtered_blobs = []
    for blob in blobs_DoG:
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

        if filter_identical:
            # filter out blobs where the two methods do not get the same result
            potential_indices_y = np.argwhere(blobs_LoG[:,0]==np.array(y))
            potential_indices_x = np.argwhere(blobs_LoG[:,1]==np.array(x))
            for index_y in potential_indices_y:
                for index_x in potential_indices_x:
                    if index_x == index_y:
                        filtered_blobs.append(blob)
        else:
            filtered_blobs.append(blob)

    return np.array(filtered_blobs)


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