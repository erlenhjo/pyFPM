import matplotlib.pyplot as plt

import pyFPM

camera = pyFPM.setup.components.Camera.HAMAMATSU
lens = pyFPM.setup.components.Lens.INFINITYCORRECTED_2X
slide = pyFPM.setup.components.Slide.THIN_SLIDE
LED_array = pyFPM.setup.components.Led_array.MAIN_LED_ARRAY
array_to_object_distance = 0.192

datadirpath = "C:/Users/erlen/Documents/GitHub/pyFPM/data/20230825_USAFtarget"
#datadirpath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\EHJ290823_USAF1951_infcorr2x_hamamatsu"

pixel_scale_factor = 4
patch_start = [949, 979] # [x, y]
patch_size = [64, 64] # [x, y]

background_filename = "dark_image"
image_format = "tiff"
rotation = False
remove_background = False
threshold_value = False

setup_parameters: pyFPM.setup.Setup_parameters.Setup_parameters \
    = pyFPM.setup.Setup_parameters.setup_parameters_from_file(
    datadirpath = datadirpath,
    lens = lens,
    camera = camera,
    slide = slide,
    LED_array = LED_array,
    array_to_object_distance = array_to_object_distance
    )

rawdata = pyFPM.setup.Rawdata.Rawdata(
    datadirpath = datadirpath,
    background_filename = background_filename,
    image_format = image_format,
    patch_start = patch_start,
    patch_size = patch_size
    )

preprocessed_data = pyFPM.pre_processing.Preprocessed_data.Preprocessed_data(
    rawdata = rawdata,
    setup_parameters = setup_parameters,
    remove_background = remove_background, 
    threshold_value = threshold_value, 
    )

imaging_system = pyFPM.setup.Imaging_system.Imaging_system(
    setup_parameters = setup_parameters,
    pixel_scale_factor = pixel_scale_factor,
    patch_start = patch_start,
    patch_size = patch_size,
    rotation = rotation
    )

illumination_pattern = pyFPM.pre_processing.Illumination_pattern.Illumination_pattern(
    LED_indices = preprocessed_data.LED_indices,
    imaging_system = imaging_system,
    setup_parameters = setup_parameters
)

pyFPM.calibration.defocus_calibration.primitive_defocus_calibration(
    preprocessed_data = preprocessed_data,
    imaging_system = imaging_system,
    illumination_pattern = illumination_pattern
)


plt.imshow(rawdata.images[illumination_pattern.update_order[0]])
plt.show()