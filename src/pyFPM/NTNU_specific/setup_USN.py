from pyFPM.setup.Setup_parameters import Setup_parameters, LED_infos, Lens, Camera
from pyFPM.setup.Imaging_system import Imaging_system
from pyFPM.setup.Data import Preprocessed_data, Rawdata, Data_patch
from pyFPM.setup.Illumination_pattern import Illumination_pattern

import numpy as np
from PIL import Image
import os


### USN ###
USN_camera = Camera(
    camera_pixel_size = 2.4e-6,
    raw_image_size = np.array([5496,3672]),
    float_type = np.float64
)
USN_lens = Lens(
    NA = 0.1,
    magnification = 4,
    effectiv_object_to_aperture_distance = (1+1/4)*7.6e-3,
    focal_length = 7.6e-3,
    working_distance = 9.5e-3,
    depth_of_field = None,
    max_FoV_sensor = None,
)


def setup_USN(
    lens: Lens,
    datadirpath,
    patch_offset,
    patch_size,
    pixel_scale_factor,
    threshold_value,
    noise_reduction_regions,
    calibration_parameters,
    max_array_size
):
    
    setup_parameters, preprocessed_data = setup_USN_global(lens,
                                                           datadirpath,
                                                           threshold_value,
                                                           noise_reduction_regions,
                                                           max_array_size
                                                          )
    

    imaging_system, data_patch, illumination_pattern = setup_USN_local(setup_parameters,
                                                                       preprocessed_data,
                                                                       patch_offset,
                                                                       patch_size,
                                                                       pixel_scale_factor,
                                                                       calibration_parameters,
                                                                       max_array_size
                                                                      )

    return setup_parameters, data_patch, imaging_system, illumination_pattern

# patch independent part of setup
def setup_USN_global(lens: Lens,
                     datadirpath,
                     threshold_value,
                     noise_reduction_regions,
                     max_array_size):
    
    array_size = 15
    LED_info: LED_infos = LED_infos(
        LED_pitch = 4e-3,
        wavelength = 520e-9,
        LED_array_size = [array_size, array_size],
        LED_offset = [0,0],
        center_indices = [8,8],
        exposure_times = np.ones(shape = (array_size + 1, array_size + 1))
    )

    setup_parameters: Setup_parameters = Setup_parameters(
        lens = lens,
        camera = USN_camera,
        LED_info = LED_info,
        image_format = ".tiff"
    )

    rawdata: Rawdata = get_rawdata_from_files_USN(
        datadirpath = datadirpath,
        image_format = setup_parameters.image_format,
        center_indices = LED_info.center_indices,
        array_size = array_size,
        max_array_size = max_array_size
        )

    preprocessed_data = Preprocessed_data(
        rawdata = rawdata,
        setup_parameters = setup_parameters,
        noise_reduction_regions = noise_reduction_regions, 
        threshold_value = threshold_value,
        )


    return setup_parameters, preprocessed_data


# patch dependent part of setup
def setup_USN_local(setup_parameters: Setup_parameters,
                    preprocessed_data: Preprocessed_data,
                    patch_offset,
                    patch_size,
                    pixel_scale_factor,
                    calibration_parameters,
                    max_array_size
                    ):

    data_patch = Data_patch(
        data = preprocessed_data,
        raw_image_size = setup_parameters.camera.raw_image_size,
        patch_offset = patch_offset,
        patch_size = patch_size
        )

    imaging_system = Imaging_system(
        setup_parameters = setup_parameters,
        pixel_scale_factor = pixel_scale_factor,
        patch_offset = patch_offset,
        patch_size = patch_size,
        calibration_parameters=calibration_parameters
        )

    illumination_pattern = Illumination_pattern(
        LED_indices = data_patch.LED_indices,
        imaging_system = imaging_system,
        setup_parameters = setup_parameters,
        max_array_size = max_array_size
    )

    return imaging_system, data_patch, illumination_pattern



def get_rawdata_from_files_USN(datadirpath, image_format, center_indices, array_size, max_array_size):
    LED_indices = []
    images = []
    file_nr = 0

    max_X = center_indices[0] + max_array_size//2
    min_X = center_indices[0] - max_array_size//2
    max_Y = center_indices[1] + max_array_size//2
    min_Y = center_indices[1] - max_array_size//2

    for Y in range(1,array_size+1):
        for X in range(1,array_size+1):
            file_nr+=1
            file = os.path.join(datadirpath, f"{file_nr}{image_format}")

            if (X<min_X or X>max_X ) or (Y<min_Y or Y>max_Y):
                continue
            
            image = np.array(Image.open(file))
            LED_indices.append([X,Y])
            images.append(image)
    

    return Rawdata(LED_indices=LED_indices, 
                   images=np.array(images), 
                   background_image=np.ones(shape=image.shape))


        
        





     

