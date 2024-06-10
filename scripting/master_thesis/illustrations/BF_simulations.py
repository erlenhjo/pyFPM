
from pyFPM.NTNU_specific.simulate_images.only_illumination import simulate_illumination
from pyFPM.setup.Setup_parameters import Lens
from pyFPM.setup.Imaging_system import LED_calibration_parameters
from pyFPM.setup.Setup_parameters import Setup_parameters
from pyFPM.setup.Data import Data_patch
from pyFPM.NTNU_specific.components import IDS_U3_31J0CP_REV_2_2

from pathlib import Path
import pickle

lens = Lens(
    NA = 0.05,
    magnification = 2,
    focal_length = 60e-3,
    effectiv_object_to_aperture_distance = 90e-3,
    working_distance = None,
    depth_of_field = None,
    max_FoV_sensor = None
)
camera = IDS_U3_31J0CP_REV_2_2
arraysize = 5


sim_data_path_200 = Path.cwd() / "scripting" / "master_thesis" / "illustrations" / "simulated_BF_data_200mm.obj"
sim_setup_path_200 = Path.cwd() / "scripting" / "master_thesis" / "illustrations" / "simulated_BF_setup_200mm.obj"
sim_data_path_175 = Path.cwd() / "scripting" / "master_thesis" / "illustrations" / "simulated_BF_data_175mm.obj"
sim_setup_path_175 = Path.cwd() / "scripting" / "master_thesis" / "illustrations" / "simulated_BF_setup_175mm.obj"
sim_data_path_150 = Path.cwd() / "scripting" / "master_thesis" / "illustrations" / "simulated_BF_data_150mm.obj"
sim_setup_path_150 = Path.cwd() / "scripting" / "master_thesis" / "illustrations" / "simulated_BF_setup_150mm.obj"

def simulate_200():
    calibration_parameters = LED_calibration_parameters(200e-3,0,0,0)
    setup_parameters, data_patch, imaging_system, illumination_pattern, applied_pupil, high_res_complex_object\
       = simulate_illumination(lens = lens, 
                               camera = camera,
                               correct_spherical_wave_illumination = True, 
                               correct_Fresnel_propagation = True,
                               arraysize = arraysize,
                               calibration_parameters = calibration_parameters,
                               patch_offset = [0,0])

    with open(sim_data_path_200, "wb") as file:
        pickle.dump(data_patch, file)
    with open(sim_setup_path_200, "wb") as file:
        pickle.dump(setup_parameters, file)

def simulate_175():
    calibration_parameters = LED_calibration_parameters(175e-3,0,0,0)
    setup_parameters, data_patch, imaging_system, illumination_pattern, applied_pupil, high_res_complex_object\
       = simulate_illumination(lens = lens, 
                               camera = camera,
                               correct_spherical_wave_illumination = True, 
                               correct_Fresnel_propagation = True,
                               arraysize = arraysize,
                               calibration_parameters = calibration_parameters,
                               patch_offset = [0,0])

    with open(sim_data_path_175, "wb") as file:
        pickle.dump(data_patch, file)
    with open(sim_setup_path_175, "wb") as file:
        pickle.dump(setup_parameters, file)


def simulate_150():
    calibration_parameters = LED_calibration_parameters(150e-3,0,0,0)
    setup_parameters, data_patch, imaging_system, illumination_pattern, applied_pupil, high_res_complex_object\
       = simulate_illumination(lens = lens, 
                               camera = camera,
                               correct_spherical_wave_illumination = True, 
                               correct_Fresnel_propagation = True,
                               arraysize = arraysize,
                               calibration_parameters = calibration_parameters,
                               patch_offset = [0,0])

    with open(sim_data_path_150, "wb") as file:
        pickle.dump(data_patch, file)
    with open(sim_setup_path_150, "wb") as file:
        pickle.dump(setup_parameters, file)

def get_200() -> tuple[Data_patch, Setup_parameters, LED_calibration_parameters]:
    calibration_parameters = LED_calibration_parameters(200e-3,0,0,0)
    with open(sim_data_path_200, "rb") as file:
        data_patch = pickle.load(file)
    with open(sim_setup_path_200, "rb") as file:
        setup_parameters = pickle.load(file)

    return data_patch, setup_parameters, calibration_parameters

def get_175() -> tuple[Data_patch, Setup_parameters, LED_calibration_parameters]:
    calibration_parameters = LED_calibration_parameters(175e-3,0,0,0)
    with open(sim_data_path_175, "rb") as file:
        data_patch = pickle.load(file)
    with open(sim_setup_path_175, "rb") as file:
        setup_parameters = pickle.load(file)

    return data_patch, setup_parameters, calibration_parameters

def get_150() -> tuple[Data_patch, Setup_parameters, LED_calibration_parameters]:
    calibration_parameters = LED_calibration_parameters(150e-3,0,0,0)
    with open(sim_data_path_150, "rb") as file:
        data_patch = pickle.load(file)
    with open(sim_setup_path_150, "rb") as file:
        setup_parameters = pickle.load(file)

    return data_patch, setup_parameters, calibration_parameters

if __name__ == "__main__":
    simulate_150()
    simulate_175()
    simulate_200()