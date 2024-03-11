import matplotlib.pyplot as plt
import numpy as np

from pyFPM.visualization.plot_illumination import plot_bright_field_images
from pyFPM.NTNU_specific.setup_from_file import setup_parameters_from_file
from pyFPM.NTNU_specific.rawdata_from_files import get_rawdata_from_files
from pyFPM.NTNU_specific.components import IDS_U3_31J0CP_REV_2_2, MAIN_LED_ARRAY
from pyFPM.setup.Setup_parameters import Setup_parameters
from pyFPM.setup.Data import Data_patch, Rawdata, Preprocessed_data


def illustrate_dataset_from_setup(datadirpath, lens, array_size):
    patch_start = [0, 0] # [x, y]
    patch_size = [2048, 2048] # [x, y]

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
    import matplotlib.pyplot as plt
    for image in rawdata.images:
        plt.matshow(image)
        plt.show()

    preprocessed_data = Preprocessed_data(
        rawdata = rawdata,
        setup_parameters = setup_parameters,
        remove_background = False,
        noise_reduction_regions = None, 
        threshold_value = False
        )
    
    data_patch = Data_patch(
        data = preprocessed_data,
        patch_start = patch_start,
        patch_size = patch_size
        )

    fig = plot_bright_field_images(data_patch=data_patch, setup_parameters=setup_parameters, array_size=array_size)
    return fig
