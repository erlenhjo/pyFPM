import os
import numpy as np
from PIL import Image

from pyFPM.setup.Data import Rawdata
from pyFPM.setup.Imaging_system import calculate_patch_start_and_end


def get_rawdata_from_files(datadirpath, image_format, center_indices, max_array_size, 
                           float_type, binning_factor, desired_step_nr = 0, 
                           limited_import_patch = None, limited_import_shift = np.array([0,0]),
                           LED_circle = False):
        background_filename = "dark_image"

        image_files, background_file = get_image_filenames(
            datadirpath = datadirpath,
            image_format = image_format,
            background_filename = background_filename
        )

        background_image = load_single_image(
            datadirpath = datadirpath,
            file = background_file,
            binning_factor = binning_factor,
            limited_import_patch = limited_import_patch,
            limited_import_shift = limited_import_shift
            )
        
        LED_indices, images = load_images(
            datadirpath = datadirpath,
            image_files = image_files,
            center_indices = center_indices,
            max_array_size = max_array_size,
            desired_step_nr = desired_step_nr,
            binning_factor = binning_factor,
            limited_import_patch = limited_import_patch,
            limited_import_shift = limited_import_shift,
            LED_circle = LED_circle
        )

        return Rawdata(LED_indices=LED_indices, images=images.astype(float_type), 
                       background_image=background_image)

        
        

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

def load_images(datadirpath, image_files, center_indices, max_array_size, desired_step_nr, 
                binning_factor, limited_import_patch, limited_import_shift, LED_circle):
    LED_indices = []
    images = []

    center_x = center_indices[0]
    center_y = center_indices[1]
    max_X = center_x + max_array_size//2
    min_X = center_x - max_array_size//2
    max_Y = center_y + max_array_size//2
    min_Y = center_y - max_array_size//2
    radius = max_array_size/2

    for file in image_files:
        X, Y, step_nr = indices_from_image_title(file)

        if not LED_circle:
            if (X<min_X or X>max_X ) or (Y<min_Y or Y>max_Y):
                continue
        else:
            if ((X-center_x)**2 + (Y-center_y)**2 > radius**2):
                continue

        if step_nr != desired_step_nr:
            continue

        LED_indices.append([X,Y])  
        image = load_single_image(
            datadirpath = datadirpath,
            file = file,
            binning_factor = binning_factor,
            limited_import_patch = limited_import_patch,
            limited_import_shift = limited_import_shift
            )
        
        images.append(image)
        
    return LED_indices, np.array(images)
     

def load_single_image(datadirpath, file, binning_factor, limited_import_patch, limited_import_shift):
    full_image = np.array(Image.open(os.path.join(datadirpath, file)), dtype=np.uint32) # note int type

    if limited_import_patch is not None: # only supported with center at [0,0] currently
        patch_start, patch_end = calculate_patch_start_and_end(
            image_size = np.array([full_image.shape[1], full_image.shape[0]]),
            patch_offset = limited_import_shift,
            patch_size = limited_import_patch
        )
        limited_image = full_image[patch_start[1]:patch_end[1], patch_start[0]:patch_end[0]]
        return bin_image(limited_image, binning_factor)
    else:
        return bin_image(full_image, binning_factor)


def bin_image(image, binning_factor):
    binned_image = 0
    image_size = np.array(image.shape)    
    
    binning_shift = image_size % binning_factor / 2
    image = image[int(np.floor(binning_shift[0])):image_size[0]-int(np.ceil(binning_shift[0])),
                  int(np.floor(binning_shift[1])):image_size[1]-int(np.ceil(binning_shift[1]))]

    for dx in range(binning_factor):
        for dy in range(binning_factor):
            binned_image = binned_image + image[dy::binning_factor,
                                                dx::binning_factor]
            
    return binned_image / (binning_factor**2)


