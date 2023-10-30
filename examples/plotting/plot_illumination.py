import matplotlib.pyplot as plt
import numpy as np

from pyFPM.setup.Illumination_pattern import Illumination_pattern
from pyFPM.setup.Data import Data_patch
from pyFPM.setup.Setup_parameters import Setup_parameters


def plot_bright_field_images(data_patch: Data_patch, illumination_pattern: Illumination_pattern, setup_parameters: Setup_parameters, array_size):
    relative_NAs = illumination_pattern.relative_NAs
    LED_indices = data_patch.LED_indices

    center_indices = setup_parameters.LED_info.center_indices
    center_x = center_indices[0]
    center_y = center_indices[1]
    y_min = center_y - array_size//2
    x_min = center_x - array_size//2
    y_max = y_min + array_size
    x_max = x_min + array_size

    max_intensity = np.max(data_patch.amplitude_images)**2

    fig, axes = plt.subplots(nrows=array_size, ncols=array_size, figsize=(5,5))


    for image_nr, indices in enumerate(LED_indices):
        x,y = indices
        if x >= x_min and x<x_max and y>=y_min and y<y_max:
            m=y_max-y-1
            n=x_max-x-1
            axes[m,n].matshow(data_patch.amplitude_images[image_nr]**2, vmin=0, vmax=max_intensity)
            axes[m,n].axis("off")
    
    fig.subplots_adjust(wspace=0.05, hspace=0.05)