from pyFPM.setup.Setup_parameters import Setup_parameters, Lens
from pyFPM.setup.Imaging_system import Imaging_system
from pyFPM.setup.Data import Preprocessed_data, Rawdata, Data_patch
from pyFPM.setup.Illumination_pattern import Illumination_pattern
from pyFPM.NTNU_specific.components import IDS_U3_31J0CP_REV_2_2, MAIN_LED_ARRAY
from pyFPM.NTNU_specific.setup_from_file import setup_parameters_from_file
from pyFPM.NTNU_specific.rawdata_from_files import get_rawdata_from_files

import numpy as np

def setup_IDS_U3(
    lens: Lens,
    datadirpath,
    patch_offset,
    patch_size,
    pixel_scale_factor,
    threshold_value,
    noise_reduction_regions,
    calibration_parameters,
    max_array_size,
    binning_factor
):
    
    setup_parameters, preprocessed_data = setup_IDS_U3_global(lens,
                                                              datadirpath,
                                                              threshold_value,
                                                              noise_reduction_regions,
                                                              max_array_size,
                                                              binning_factor
                                                              )
    

    imaging_system, data_patch, illumination_pattern = setup_IDS_U3_local(setup_parameters,
                                                                          preprocessed_data,
                                                                          patch_offset,
                                                                          patch_size,
                                                                          pixel_scale_factor,
                                                                          calibration_parameters,
                                                                          max_array_size
                                                                          )

    return setup_parameters, data_patch, imaging_system, illumination_pattern

# patch independent part of setup
def setup_IDS_U3_global(lens: Lens,
                        datadirpath,
                        threshold_value,
                        noise_reduction_regions,
                        max_array_size,
                        binning_factor,
                        limited_import_patch = None,
                        limited_import_shift = np.array([0,0])):
    
    camera = IDS_U3_31J0CP_REV_2_2
    LED_array = MAIN_LED_ARRAY

    setup_parameters: Setup_parameters = setup_parameters_from_file(
        datadirpath = datadirpath,
        lens = lens,
        camera = camera,
        LED_array = LED_array,
        binning_factor = binning_factor
        )

    rawdata: Rawdata = get_rawdata_from_files(
        datadirpath = datadirpath,
        image_format = setup_parameters.image_format,
        center_indices = setup_parameters.LED_info.center_indices,
        max_array_size = max_array_size,
        float_type = setup_parameters.camera.float_type,
        binning_factor = binning_factor,
        limited_import_patch = limited_import_patch,
        limited_import_shift = limited_import_shift
        )

    preprocessed_data = Preprocessed_data(
        rawdata = rawdata,
        setup_parameters = setup_parameters,
        noise_reduction_regions=noise_reduction_regions, 
        threshold_value = threshold_value, 
        )

    return setup_parameters, preprocessed_data


# patch dependent part of setup
def setup_IDS_U3_local(setup_parameters: Setup_parameters,
                       preprocessed_data: Preprocessed_data,
                       patch_offset,
                       patch_size,
                       pixel_scale_factor,
                       calibration_parameters,
                       max_array_size,
                       binned_limited_import_shift
                       ):

    binned_image_size = [preprocessed_data.amplitude_images[0].shape[1], 
                         preprocessed_data.amplitude_images[0].shape[0]]

    data_patch = Data_patch(
        data = preprocessed_data,
        patch_offset = patch_offset,
        patch_size = patch_size,
        binned_image_size = binned_image_size,
        binned_limited_import_shift = binned_limited_import_shift
        )

    imaging_system = Imaging_system(
        setup_parameters = setup_parameters,
        pixel_scale_factor = pixel_scale_factor,
        patch_offset = patch_offset,
        patch_size = patch_size,
        calibration_parameters=calibration_parameters,
        binned_image_size = binned_image_size
        )

    illumination_pattern = Illumination_pattern(
        LED_indices = data_patch.LED_indices,
        imaging_system = imaging_system,
        setup_parameters = setup_parameters,
        max_array_size = max_array_size
    )

    return imaging_system, data_patch, illumination_pattern