from pyFPM.setup.Setup_parameters import Setup_parameters, setup_parameters_from_file
from pyFPM.setup.Imaging_system import Imaging_system
from pyFPM.setup.Rawdata import Rawdata
from pyFPM.setup.Preprocessed_data import Preprocessed_data
from pyFPM.setup.Illumination_pattern import Illumination_pattern
from pyFPM.setup.components import Camera, Lens, Led_array, Slide


def simulate_2x_hamamatsu(
    datadirpath,
    patch_start,
    patch_size,
    pixel_scale_factor
):
    camera = Camera.HAMAMATSU
    lens = Lens.INFINITYCORRECTED_2X
    slide = Slide.THIN_SLIDE
    LED_array = Led_array.MAIN_LED_ARRAY
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





if __name__ == "__main__":
    dot_radius = 62.5e-6 / 2 # m
    dot_spacing = 125e-6 # m
    pixel_number = 8192
    nr_of_dots = 4

    dot_array_image = dot_array(dot_radius=dot_radius, 
                                dot_spacing=dot_spacing, 
                                pixel_number=pixel_number,
                                nr_of_dots=nr_of_dots)