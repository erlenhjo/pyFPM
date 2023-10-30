import matplotlib.pyplot as plt
import numpy as np

from plotting.plot_illumination import plot_bright_field_images

from pyFPM.NTNU_specific.simulate_images.cameraman import simulate_cameraman_2x

# FPM imports
from pyFPM.NTNU_specific.setup_2x_hamamatsu import setup_2x_hamamatsu

def illustrate_simulation():
    setup_parameters, data_patch, imaging_system, illumination_pattern, applied_pupil, _\
       = simulate_cameraman_2x(noise_fraction=0, zernike_coefficients=np.array([0,0,0]))

    plot_bright_field_images(data_patch=data_patch, illumination_pattern=illumination_pattern, setup_parameters=setup_parameters, array_size=5)
    plt.show()

def illustrate_from_setup():
    #datadirpath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\20230825_USAFtarget"
    #datadirpath = r"c:\Users\erlen\Documents\GitHub\pyFPM\data\EHJ20230915_dotarray_2x_inf"
    #datadirpath = r"c:\Users\erlen\Documents\GitHub\pyFPM\data\dotarray_2x_dark_no_object"
    #datadirpath = r"c:\Users\erlen\Documents\GitHub\pyFPM\data\dotarray_2x_dark_object"
    datadirpath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\dotarray_telecentric3x_dark"
    #datadirpath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\dotarray_telecentric3x_dark_no_object"

    array_size = 7

    pixel_scale_factor = 4
    patch_start = [0, 0] # [x, y]
    patch_size = [2048, 2048] # [x, y]

    setup_parameters, data_patch, imaging_system, illumination_pattern = setup_2x_hamamatsu(
        datadirpath = datadirpath,
        patch_start = patch_start,
        patch_size = patch_size,
        pixel_scale_factor = pixel_scale_factor
    )

    plot_bright_field_images(data_patch=data_patch, illumination_pattern=illumination_pattern, setup_parameters=setup_parameters, array_size=array_size)
    plt.show()

if __name__ == "__main__":
    illustrate_from_setup()
    #illustrate_simulation()

    

    
