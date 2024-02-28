from pyFPM.setup.Setup_parameters import Setup_parameters, Lens
from pyFPM.setup.Imaging_system import Imaging_system
from pyFPM.setup.Data import Preprocessed_data, Rawdata, Data_patch
from pyFPM.setup.Illumination_pattern import Illumination_pattern
from pyFPM.NTNU_specific.components import IDS_U3_31J0CP_REV_2_2, MAIN_LED_ARRAY
from pyFPM.NTNU_specific.setup_from_file import setup_parameters_from_file
from pyFPM.NTNU_specific.rawdata_from_files import get_rawdata_from_files

def setup_IDS_U3(
    lens: Lens,
    datadirpath,
    patch_start,
    patch_size,
    pixel_scale_factor,
    remove_background,
    threshold_value,
    noise_reduction_regions,
    calibration_parameters,
    max_array_size
):
    camera = IDS_U3_31J0CP_REV_2_2
    LED_array = MAIN_LED_ARRAY

    setup_parameters: Setup_parameters = setup_parameters_from_file(
        datadirpath = datadirpath,
        lens = lens,
        camera = camera,
        LED_array = LED_array
        )

    rawdata: Rawdata = get_rawdata_from_files(
        datadirpath = datadirpath,
        image_format = setup_parameters.image_format
        )

    preprocessed_data = Preprocessed_data(
        rawdata = rawdata,
        setup_parameters = setup_parameters,
        remove_background = remove_background,
        noise_reduction_regions=noise_reduction_regions, 
        threshold_value = threshold_value, 
        )
    
    data_patch = Data_patch(
        data = preprocessed_data,
        patch_start = patch_start,
        patch_size = patch_size
        )

    imaging_system = Imaging_system(
        setup_parameters = setup_parameters,
        pixel_scale_factor = pixel_scale_factor,
        patch_start = patch_start,
        patch_size = patch_size,
        LED_calibration_parameters=calibration_parameters
        )

    illumination_pattern = Illumination_pattern(
        LED_indices = data_patch.LED_indices,
        imaging_system = imaging_system,
        setup_parameters = setup_parameters,
        max_array_size = max_array_size
    )

    return setup_parameters, data_patch, imaging_system, illumination_pattern