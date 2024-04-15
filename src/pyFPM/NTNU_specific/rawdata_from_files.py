import os
import numpy as np
from PIL import Image

from pyFPM.setup.Data import Rawdata


def get_rawdata_from_files(datadirpath, image_format, center_indices, max_array_size, 
                           float_type, desired_step_nr = 0):
        background_filename = "dark_image"

        image_files, background_file = get_image_filenames(
            datadirpath = datadirpath,
            image_format = image_format,
            background_filename = background_filename
        )

        background_image = load_single_image(
            datadirpath = datadirpath,
            file = background_file
            )
        
        LED_indices, images = load_images(
            datadirpath = datadirpath,
            image_files = image_files,
            center_indices = center_indices,
            max_array_size = max_array_size,
            desired_step_nr = desired_step_nr
        )

        return Rawdata(LED_indices=LED_indices, images=images.astype(float_type), background_image=background_image)

        
        

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
    filename = filename.split("-")
    filename_start = filename[0]
    filename_end = filename[1]

    step_nr_image_nr = filename_start.split("_")
    x_y_index = filename_end.split("_")

    step_nr = int(step_nr_image_nr[0])
    x_index = int(x_y_index[0])
    y_index = int(x_y_index[1])

    return x_index, y_index, step_nr

def load_images(datadirpath, image_files, center_indices, max_array_size, desired_step_nr):
    LED_indices = []
    images = []
    max_X = center_indices[0] + max_array_size//2
    min_X = center_indices[0] - max_array_size//2
    max_Y = center_indices[1] + max_array_size//2
    min_Y = center_indices[1] - max_array_size//2

    for file in image_files:
        X, Y, step_nr = indices_from_image_title(file)

        if (X<min_X or X>max_X ) or (Y<min_Y or Y>max_Y):
            continue

        if step_nr != desired_step_nr:
            continue

        LED_indices.append([X,Y])  
        image = load_single_image(
            datadirpath = datadirpath,
            file = file
            )
        images.append(image)

    return LED_indices, np.array(images)
     

def load_single_image(datadirpath, file):
    return np.array(Image.open(os.path.join(datadirpath, file)))