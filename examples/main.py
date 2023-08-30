import pyFPM

camera = pyFPM.setup.components.cameras.HAMAMATSU
lens = pyFPM.setup.components.lenses.INFINITYCORRECTED_2X
LED_array = pyFPM.setup.components.led_arrays.MAIN_LED_ARRAY
z_LED = 0

datadirpath = "C:/Users/erlen/Documents/GitHub/pyFPM/data/20230825_USAFtarget"

setup_params = pyFPM.setup.Setup_parameters.Setup_parameters(
    datadirpath = datadirpath,
    lens = lens,
    camera = camera,
    LED_array= LED_array,
    z_LED = z_LED
    )
