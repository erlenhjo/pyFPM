import os

from PIL import Image
import numpy as np

from pyFPM.setup.Imaging_system import Imaging_system
from pyFPM.setup.Setup_parameters import Setup_parameters



class Rawdata(object):
    def __init__(self, datadirpath, background_filename, imaging_system: Imaging_system):
        image_format = imaging_system.setup_parameters.image_format
        LED_array_size = imaging_system.setup_parameters.LED_array_size
        patch_start = imaging_system.patch_start
        patch_size = imaging_system.patch_size

        
        image_files, background_file = get_image_filenames(
            datadirpath = datadirpath,
            image_format = image_format,
            background_filename = background_filename
        )

        available_LEDs = determine_available_LEDs(
            image_files = image_files,
            LED_array_size = LED_array_size
            ) 
        
        desired_LEDs = available_LEDs
        
        self.background_image = load_single_image(
            datadirpath = datadirpath,
            file = background_file,
            patch_start = patch_start,
            patch_size = patch_size
            )

        LED_indices, images = load_images(
            datadirpath = datadirpath,
            image_files = image_files,
            desired_LEDs = desired_LEDs,
            patch_start = patch_start,
            patch_size = patch_size
        )

        self.LED_indices = LED_indices
        self.images = images

 
            
def get_image_filenames(datadirpath, image_format, background_filename):
    image_files = []
    background_file = None

    files_in_dataset: list[str] = os.listdir(datadirpath)

    for file in files_in_dataset:
        if file.endswith(image_format):
            if file == f"{background_filename}.{image_format}":
                background_file = file
            else:
                image_files.append(file)

    if background_file == None:
        raise "Could not find background file"

    return image_files, background_file


def indices_from_image_title(filename: str):
    filename = filename.split(".")[0]
    filename = filename.split("-")[1]
    filename = filename.split("_")

    x_index = int(filename[0])
    y_index = int(filename[1])

    return x_index, y_index
    

def determine_available_LEDs(image_files: list[str], LED_array_size):
    available_LEDs = np.zeros(shape = (LED_array_size[1] + 1, LED_array_size[0] + 1), dtype = bool)   # plus 1 in case array indices are one indexed
    
    for file in image_files:
        x, y = indices_from_image_title(file)
        available_LEDs[y,x] = True

    return available_LEDs


def load_images(datadirpath, image_files, desired_LEDs, patch_start, patch_size):
    nr_of_images = np.sum(desired_LEDs)

    LED_indices = []
    images = np.empty(shape = (nr_of_images, patch_size[1], patch_size[0]))
    
    for n, file in enumerate(image_files):
        x, y = indices_from_image_title(file)
        
        if desired_LEDs[y, x]:
            LED_indices.append([x,y])  
            image = load_single_image(
                datadirpath = datadirpath,
                file = file,
                patch_start = patch_start,
                patch_size = patch_size
                )
            images[n, :, :] = image

    return LED_indices, images
     

def load_single_image(datadirpath, file, patch_start, patch_size):
    image = np.array(Image.open(os.path.join(datadirpath, file)))
    
    # select patch
    x_start = patch_start[0]
    x_end = patch_start[0] + patch_size[0]
    y_start = patch_start[1]
    y_end = patch_start[1] + patch_size[1]
    image = image[y_start:y_end, x_start:x_end]

    return image




