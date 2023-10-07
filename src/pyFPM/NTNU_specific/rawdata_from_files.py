import os
import numpy as np
from PIL import Image

from pyFPM.setup.Data import Rawdata


def get_rawdata_from_files(datadirpath, background_filename, image_format):
                
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
            image_files = image_files
        )

        return Rawdata(LED_indices=LED_indices, images=images, background_image=background_image)

        
        

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
    

def load_images(datadirpath, image_files):
    LED_indices = []
    images = []
    
    for n, file in enumerate(image_files):
        x, y = indices_from_image_title(file)
        LED_indices.append([x,y])  
        image = load_single_image(
            datadirpath = datadirpath,
            file = file
            )
        images.append(image)

    return LED_indices, np.array(images)
     

def load_single_image(datadirpath, file):
    return np.array(Image.open(os.path.join(datadirpath, file)))