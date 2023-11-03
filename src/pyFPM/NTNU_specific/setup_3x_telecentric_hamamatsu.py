from pyFPM.setup.Setup_parameters import Setup_parameters
from pyFPM.setup.Imaging_system import Imaging_system
from pyFPM.setup.Data import Preprocessed_data, Rawdata, Data_patch
from pyFPM.setup.Illumination_pattern import Illumination_pattern
from pyFPM.NTNU_specific.components import HAMAMATSU_C11440_42U30, TELECENTRIC_3X, MAIN_LED_ARRAY
from pyFPM.NTNU_specific.setup_from_file import setup_parameters_from_file
from pyFPM.NTNU_specific.rawdata_from_files import get_rawdata_from_files

def setup_3x_telecentric_hamamatsu(
    datadirpath,
    patch_start,
    patch_size,
    pixel_scale_factor
):
    camera = HAMAMATSU_C11440_42U30
    lens = TELECENTRIC_3X
    slide = None
    LED_array = MAIN_LED_ARRAY
    array_to_object_distance = 0.192  

    background_filename = "dark_image"
    image_format = "tiff"
    remove_background = False
    threshold_value = False

    setup_parameters: Setup_parameters = setup_parameters_from_file(
        datadirpath = datadirpath,
        lens = lens,
        camera = camera,
        slide = slide,
        LED_array = LED_array,
        array_to_object_distance = array_to_object_distance
        )

    rawdata: Rawdata = get_rawdata_from_files(
        datadirpath = datadirpath,
        background_filename = background_filename,
        image_format = image_format
        )

    preprocessed_data = Preprocessed_data(
        rawdata = rawdata,
        setup_parameters = setup_parameters,
        remove_background = remove_background, 
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
        patch_size = patch_size
        )

    illumination_pattern = Illumination_pattern(
        LED_indices = data_patch.LED_indices,
        imaging_system = imaging_system,
        setup_parameters = setup_parameters
    )

    return setup_parameters, data_patch, imaging_system, illumination_pattern