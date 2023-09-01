import matplotlib.pyplot as plt

import pyFPM

camera = pyFPM.setup.components.cameras.HAMAMATSU
lens = pyFPM.setup.components.lenses.INFINITYCORRECTED_2X
slide = pyFPM.setup.components.slides.THIN_SLIDE
LED_array = pyFPM.setup.components.led_arrays.MAIN_LED_ARRAY
z_LED = 0.192

#datadirpath = "C:/Users/erlen/Documents/GitHub/pyFPM/data/20230825_USAFtarget"
datadirpath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\EHJ290823_USAF1951_infcorr2x_hamamatsu"

pixel_scale_factor = 4
patch_start = [949, 899] # [x, y]
patch_size = [64, 64] # [x, y]

setup_parameters = pyFPM.setup.Setup_parameters.Setup_parameters(
    datadirpath = datadirpath,
    lens = lens,
    camera = camera,
    slide = slide,
    LED_array = LED_array,
    z_LED = z_LED
    )

imaging_system = pyFPM.setup.Imaging_system.Imaging_system(
    setup_parameters = setup_parameters,
    pixel_scale_factor = pixel_scale_factor,
    patch_start = patch_start,
    patch_size = patch_size,
    rotation = 0
    )

rawdata = pyFPM.setup.Rawdata.Rawdata(
    datadirpath = datadirpath,
    image_format = setup_parameters.image_format,
    background_filename = "dark_image"
    )

plt.matshow(rawdata.array)
plt.show()
print(setup_parameters.LED_pattern)