from pyFPM.setup.Setup_parameters import Setup_parameters
from pyFPM.setup.Imaging_system import Imaging_system
from pyFPM.setup.Rawdata import Rawdata
from pyFPM.setup.Preprocessed_data import Preprocessed_data
from pyFPM.setup.Illumination_pattern import Illumination_pattern
from .components import HAMAMATSU, INFINITYCORRECTED_2X, MAIN_LED_ARRAY
from .setup_from_file import setup_parameters_from_file

def setup_2x_hamamatsu(
    datadirpath,
    patch_start,
    patch_size,
    pixel_scale_factor
):
    camera = HAMAMATSU
    lens = INFINITYCORRECTED_2X
    slide = None
    LED_array = MAIN_LED_ARRAY
    array_to_object_distance = 0.192  

    background_filename = "dark_image"
    image_format = "tiff"
    rotation = False
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

    rawdata = Rawdata(
        datadirpath = datadirpath,
        background_filename = background_filename,
        image_format = image_format,
        patch_start = patch_start,
        patch_size = patch_size
        )

    preprocessed_data = Preprocessed_data(
        rawdata = rawdata,
        setup_parameters = setup_parameters,
        remove_background = remove_background, 
        threshold_value = threshold_value, 
        )

    imaging_system = Imaging_system(
        setup_parameters = setup_parameters,
        pixel_scale_factor = pixel_scale_factor,
        patch_start = patch_start,
        patch_size = patch_size,
        rotation = rotation
        )

    illumination_pattern = Illumination_pattern(
        LED_indices = preprocessed_data.LED_indices,
        imaging_system = imaging_system,
        setup_parameters = setup_parameters
    )

    return setup_parameters, rawdata, preprocessed_data, imaging_system, illumination_pattern