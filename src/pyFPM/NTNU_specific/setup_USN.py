from pyFPM.setup.Setup_parameters import Setup_parameters, LED_infos, Lens, Camera, Lens_type
from pyFPM.setup.Imaging_system import Imaging_system
from pyFPM.setup.Data import Preprocessed_data, Rawdata, Data_patch
from pyFPM.setup.Illumination_pattern import Illumination_pattern

import numpy as np
from PIL import Image
import os
import matplotlib.pyplot as plt

### USN ###
camera = Camera(
    camera_pixel_size = 2.4e-6,
    raw_image_size = np.array([5496,3672]),
    float_type = np.float64
)
lens = Lens(
    NA = 0.1,
    magnification = 4,
    focal_length = 7.6e-3,
    working_distance = 9.5e-3,
    depth_of_field = None,
    max_FoV_sensor = None,
    lens_type = Lens_type.SINGLE_LENS,
)


def setup_USN(
    datadirpath,
    patch_shift,
    patch_size,
    calibration_parameters,
    noise_threshold
):
    threshold_value = noise_threshold
    noise_reduction_regions = [
        [175-2, 40-2, 50, 50],
        [455-2, 465-2, 50, 50]
    ]

    array_size = 15
    pixel_scale_factor = 6
    LED_info = LED_infos(
        LED_pitch = 4e-3,
        wavelength = 520e-9,
        LED_array_size = [array_size, array_size],
        LED_offset = [0,0],
        center_indices = [8,8],
        exposure_times = np.ones(shape = (array_size + 1, array_size + 1))
    )

    setup_parameters: Setup_parameters = Setup_parameters(
        lens = lens,
        camera = camera,
        LED_info = LED_info,
        image_format = ".tiff"
    )

    rawdata: Rawdata = get_rawdata_from_files_USN(
        datadirpath = datadirpath,
        image_format = setup_parameters.image_format,
        array_size = array_size,
        patch_shift = patch_shift,
        patch_size = patch_size
        )

    preprocessed_data = Preprocessed_data(
        rawdata = rawdata,
        setup_parameters = setup_parameters,
        noise_reduction_regions = noise_reduction_regions, 
        threshold_value = threshold_value,
        )
    
    data_patch = Data_patch(
        data = preprocessed_data,
        patch_start = [0,0],
        patch_size = patch_size
        )

    imaging_system = Imaging_system(
        setup_parameters = setup_parameters,
        pixel_scale_factor = pixel_scale_factor,
        patch_start = patch_shift+(setup_parameters.camera.raw_image_size-patch_size)//2,
        patch_size = patch_size,
        LED_calibration_parameters = calibration_parameters
        )

    illumination_pattern = Illumination_pattern(
        LED_indices = data_patch.LED_indices,
        imaging_system = imaging_system,
        setup_parameters = setup_parameters,
        max_array_size = array_size
    )

    return setup_parameters, data_patch, imaging_system, illumination_pattern


def get_rawdata_from_files_USN(datadirpath, image_format, array_size, patch_size, patch_shift):
    patch_size_x, patch_size_y = patch_size
    patch_shift_x, patch_shift_y = patch_shift
    LED_indices = []
    images = []
    #image_backgrounds = []
    file_nr = 0

    for Y in range(1,array_size+1):
        for X in range(1,array_size+1):
            file_nr+=1
            file = os.path.join(datadirpath, f"{file_nr}{image_format}")
            image = np.array(Image.open(file))
            total_image_size_y, total_image_size_x = image.shape

            # background_mean_region_1 = np.mean(image[1580+40-2:1580+90-1,2492+175-2:2492+225-1])
            # background_mean_region_2 = np.mean(image[1580+465-2:1580+495-1,2492+455-2:2492+490-1])
            # image_background = np.mean([background_mean_region_1, background_mean_region_2])
            
            image = image[total_image_size_y//2-patch_size_y//2 -1+patch_shift_y:\
                        total_image_size_y//2+patch_size_y//2 -1+patch_shift_y,\
                        total_image_size_x//2-patch_size_x//2 -1+patch_shift_x:\
                        total_image_size_x//2+patch_size_x//2 -1+patch_shift_x]
            
            # if image_background > noise_threshold:
            #     if len(image_backgrounds)==0:
            #         image_background = 0
            #     else:
            #         image_background = image_backgrounds[-1]
            # image = image - image_background
            # image[image<0] = 0

            LED_indices.append([X,Y])
            images.append(image)
            #images.append(np.sqrt(image))
            #image_backgrounds.append(image_background)

    return Rawdata(LED_indices=LED_indices, 
                   images=np.array(images), 
                   background_image=np.zeros((total_image_size_y,total_image_size_x)))