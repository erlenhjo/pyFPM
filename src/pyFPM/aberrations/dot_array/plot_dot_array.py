import numpy as np
import matplotlib.pyplot as plt

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
    ax.set_title("Dots vs. grid")

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
    fig.colorbar(cax)
    ax.set_title("Error in micrometers")


def plot_dot_error(ax: plt.Axes, blobs, grid_points, grid_indices, object_pixel_size):
    max_index = grid_indices.max()
    error = np.zeros(shape = (max_index+1, max_index+1))
    values = zip(blobs, grid_points, grid_indices)
    for blob, grid_point, indices in values:
        Y = indices[0]
        X = indices[1]
        distance_error = np.linalg.norm(blob-grid_point) * object_pixel_size *1e6
        error[Y, X] = distance_error

    cax = ax.matshow(error, vmin=0, vmax = max(10, error.max()))
    plt.colorbar(cax, ax=ax)
    ax.set_title("Error in micrometers")


def plot_example_dots(fig, image, blobs, grid_points, grid_indices, dot_array, object_pixel_size):
    dot_radius_pixels = dot_array.diameter/2 / object_pixel_size
    fig.suptitle("Example dots")
    
    axes = fig.subplots(3,3)
    center = grid_indices.max()//2
    min = 2
    max = grid_indices.max()-3
    # for y in [min, center, max]:
    #     for x in [min, center, max]:

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
    
    fig.tight_layout()

def plot_dot_subimage(ax, image, blob, grid_point, dot_radius_pixels):
    colors = ["red", "lime"]
    markers = ["x", "+"]
    
    delta = 1.6 * dot_radius_pixels
    y, x = blob
    x_min = int(x-delta)
    x_max = int(x+delta)
    y_min = int(y-delta)
    y_max = int(y+delta)

    blob_y, blob_x = blob - np.array([y_min, x_min])
    grid_y, grid_x = grid_point - np.array([y_min, x_min])

    ax.imshow(image[y_min:y_max, x_min:x_max])
    ax.plot(blob_x, blob_y, color=colors[0], marker=markers[0])

    ax.plot(grid_x, grid_y, color=colors[1], marker=markers[1])

    ax.set_axis_off()
