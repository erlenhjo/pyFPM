from enum import Enum

# setup imports
from setup_2x_hamamatsu import setup_2x_hamamatsu

# calibration imports
from pyFPM.calibration.defocus_calibration import primitive_defocus_calibration

class Method(Enum):
    Primitive = 1
    Epry = 2
    Epry_Gradient_Descent = 3
    Fresnel = 4
    Fresnel_Epry = 5

#datadirpath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\20230825_USAFtarget"
#datadirpath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\EHJ290823_USAF1951_infcorr2x_hamamatsu"
datadirpath = r"c:\Users\erlen\Documents\GitHub\FPM\data\EHJ20230915_dotarray_2x_inf"

pixel_scale_factor = 4
patch_start = [949, 979] # [x, y]
patch_size = [64, 64] # [x, y]

method = Method.Epry_Gradient_Descent

setup_parameters, rawdata, preprocessed_data, imaging_system, illumination_pattern = setup_2x_hamamatsu(
    datadirpath = datadirpath,
    patch_start = patch_start,
    patch_size = patch_size,
    pixel_scale_factor = pixel_scale_factor
)

if method == Method.Primitive:
    primitive_defocus_calibration(
        preprocessed_data = preprocessed_data,
        imaging_system = imaging_system,
        illumination_pattern = illumination_pattern
    )
elif method == Method.Epry:
    primitive_defocus_calibration(
        preprocessed_data = preprocessed_data,
        imaging_system = imaging_system,
        illumination_pattern = illumination_pattern,
        use_epry = True,
        use_gradient_descent = False
    )
elif method == Method.Epry_Gradient_Descent:
    primitive_defocus_calibration(
        preprocessed_data = preprocessed_data,
        imaging_system = imaging_system,
        illumination_pattern = illumination_pattern,
        use_epry = True,
        use_gradient_descent = True
    )
        
else:
    raise "Calibration for specified method not implemented"





