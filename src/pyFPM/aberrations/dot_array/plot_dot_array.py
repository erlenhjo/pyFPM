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
    cax = ax.matshow(error)
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

    cax = ax.matshow(error)
    plt.colorbar(cax, ax=ax)
    ax.set_title("Error in micrometers")