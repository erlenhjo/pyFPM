# pyFPM imports
from pyFPM.NTNU_specific.setup_2x_hamamatsu import setup_2x_hamamatsu
from pyFPM.recovery.calibration.primitive_calibration import primitive_calibration, Parameter
from pyFPM.recovery.algorithms.run_algorithm import Method
from pyFPM.aberrations.pupils.defocused_pupil import get_defocused_pupil
from pyFPM.setup.Imaging_system import LED_calibration_parameters

datadirpath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\USAF_centered_infcor2x"
# datadirpath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\20230825_USAFtarget"
# datadirpath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\EHJ290823_USAF1951_infcorr2x_hamamatsu"
# datadirpath = r"c:\Users\erlen\Documents\GitHub\FPM\data\EHJ20230915_dotarray_2x_inf"

pixel_scale_factor = 4
patch_start = [1000, 100] # [x, y]
patch_size = [64, 64] # [x, y]

setup_parameters, data_patch, imaging_system, illumination_pattern = setup_2x_hamamatsu(
    datadirpath = datadirpath,
    patch_start = patch_start,
    patch_size = patch_size,
    pixel_scale_factor = pixel_scale_factor,
    remove_background = True,
    threshold_value = 0.001,
    calibration_parameters= LED_calibration_parameters(2e-6,0,0,0)
)

defocus_guess = 0e-6
rotation_guess = 0
distance_offset_guess = 200e-3
LED_x_offset_guess = 0e-3
LED_y_offset_guess = 0e-3

parameter_to_calibrate = Parameter.LED_z
number_of_steps = 10

primitive_calibration(
    data_patch,
    setup_parameters,
    illumination_pattern,
    defocus_guess,
    rotation_guess,
    distance_offset_guess,
    LED_x_offset_guess,
    LED_y_offset_guess,
    patch_start,
    patch_size,
    pixel_scale_factor,
    parameter_to_calibrate,
    number_of_steps
)






