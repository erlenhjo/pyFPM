import numpy as np
import matplotlib.pyplot as plt
import cmasher

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


def plot_located_dots_vs_grid(image, detected_blobs, grid_points):
    colors = ["red", "lime"]
    markers = ["x", "+"]

    fig, ax = plt.subplots()
    ax.imshow(image)

    blob_color = colors[0]
    blob_marker = markers[0]
    for blob in detected_blobs:
        y, x = blob
        ax.plot(x, y, color=blob_color, marker=blob_marker)

    grid_color = colors[1]
    grid_marker = markers[1]
    for grid_point in grid_points:
        y, x = grid_point
        ax.plot(x, y, color=grid_color, marker=grid_marker)

    ax.set_axis_off()


def plot_located_dot_error(blobs, grid_points, grid_indices, object_pixel_size):
    max_index = grid_indices.max()
    error = np.zeros(shape = (max_index+1, max_index+1))
    values = zip(blobs, grid_points, grid_indices)
    for blob, grid_point, indices in values:
        Y = indices[0]
        X = indices[1]
        distance_error = np.linalg.norm(blob-grid_point) * object_pixel_size *1e6
        error[Y, X] = distance_error

    fig = plt.figure()
    ax = fig.add_subplot(111)
    cax = ax.matshow(error, vmin=0, vmax = max(10, error.max()))
    fig.colorbar(cax, ax=ax)
    ax.set_title("Error in micrometers")


def plot_dot_error(ax: plt.Axes, blobs, grid_points, grid_indices, object_pixel_size):
    max_index_x, max_index_y = grid_indices.max(axis=0)
    error_value_grid = np.zeros(shape = (max_index_y+1, max_index_x+1))
    values = zip(blobs, grid_points, grid_indices)
    for blob, grid_point, indices in values:
        Y = indices[0]
        X = indices[1]
        distance_error = np.linalg.norm(blob-grid_point) * object_pixel_size *1e6
        error_value_grid[Y, X] = distance_error

    error_vectors_x = (blobs[:,1]-grid_points[:,1]) / (np.linalg.norm(blobs-grid_points, axis=1) + 1e-10)
    error_vectors_y = (blobs[:,0]-grid_points[:,0]) / (np.linalg.norm(blobs-grid_points, axis=1) + 1e-10)
    error_values = np.linalg.norm(blobs-grid_points, axis=1) * object_pixel_size *1e6
    print(error_vectors_y)
    
    scale = 2
    width = 1
    headwidth = 3 * width
    headlength = 5 * width
    headaxislength = 5 * width
    minshaft = 1
    minlength = 0.9 / scale
    
    cmap = cmasher.get_sub_cmap("viridis", 0, 0.85)

    cax = ax.imshow(error_value_grid, vmin=0, vmax = error_values.max(), cmap=cmap)
    ax.quiver(grid_indices[:,1], grid_indices[:,0].max()-grid_indices[:,0], error_vectors_x, error_vectors_y,
              pivot="mid", scale_units = "xy", units = "xy", color = "black",
              width=width, headwidth=headwidth, headlength=headlength, headaxislength=headaxislength,
              minshaft=minshaft, minlength=minlength, scale = scale)
    cbar = plt.colorbar(cax, ax=ax)
    cbar.set_label("Positional mismatch [µm]")
    ax.set_axis_off()


def plot_example_dots(fig, image, blobs, grid_points, grid_indices, dot_array, object_pixel_size):
    dot_radius_pixels = dot_array.diameter/2 / object_pixel_size
    
    axes = fig.subplots(3,3)
    center = grid_indices.max()//2
    min = 0
    max = grid_indices.max()

    values = zip(blobs, grid_points, grid_indices)
    for blob, grid_point, indices in values:
        Y = indices[0]
        X = indices[1]

        if Y == min: n=0
        elif Y == center: n=1
        elif Y == max: n=2
        else: continue

        if X == min: m=0
        elif X == center: m=1
        elif X == max: m=2
        else: continue
            
        ax = axes[n,m]
            
        plot_dot_subimage(ax, image, blob, grid_point, dot_radius_pixels)
    

def plot_dot_subimage(ax, image, blob, grid_point, dot_radius_pixels):
    colors = ["red", "lime"]
    markers = ["x", "+"]
    
    delta = 1.6 * dot_radius_pixels
    y, x = blob
    x_min = int(x)-int(np.floor(delta))
    x_max = int(x)+int(np.ceil(delta))
    y_min = int(y)-int(np.floor(delta))
    y_max = int(y)+int(np.ceil(delta))

    print(x_max-x_min)
    print(y_max-y_min)

    blob_y, blob_x = blob - np.array([y_min, x_min])
    grid_y, grid_x = grid_point - np.array([y_min, x_min])

    ax.imshow(image[y_min:y_max, x_min:x_max])
    ax.plot(blob_x, blob_y, color=colors[0], marker=markers[0])

    ax.plot(grid_x, grid_y, color=colors[1], marker=markers[1])

    ax.set_axis_off()
