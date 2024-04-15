from pyFPM.NTNU_specific.simulate_images.only_illumination import simulate_illumination
from pyFPM.NTNU_specific.components import (IDS_U3_31J0CP_REV_2_2, MAIN_LED_ARRAY, INFINITYCORRECTED_2X,
                                            HAMAMATSU_C11440_42U30, TELECENTRIC_3X, DOUBLE_CONVEX, COMPACT_2X)
from pyFPM.setup.Imaging_system import LED_calibration_parameters
from pyFPM.recovery.calibration.non_linear_BFL import non_linear_BFL, calculate_BF_edge_circle, Calibration_parameters
from pyFPM.NTNU_specific.simulate_images.simulate_setup import simulate_setup_parameters
from pyFPM.setup.Data import Simulated_data, Data_patch
    
import time
import numpy as np

def locate_bright_field_from_simulation():
    lens = INFINITYCORRECTED_2X
    spherical = True
    Fresnel = False
    arraysize = 5
    simulation_parameters = LED_calibration_parameters(LED_distance = 201e-3,
                                                       LED_x_offset = 50e-6,
                                                       LED_y_offset = 50e-6,
                                                       LED_rotation = 5)
    
    assumed_parameters = LED_calibration_parameters(LED_distance = 200e-3,
                                                    LED_x_offset = 0e-6,
                                                    LED_y_offset = 0e-6,
                                                    LED_rotation = 0)

    start = time.perf_counter()
    setup_parameters, data_patch, imaging_system, illumination_pattern, applied_pupil, high_res_complex_object\
       = simulate_illumination(lens = lens, 
                               correct_spherical_wave_illumination = spherical, 
                               correct_Fresnel_propagation = Fresnel,
                               arraysize = arraysize,
                               calibration_parameters = simulation_parameters,
                               patch_offset = [0,0])
    end = time.perf_counter()
    print("Simulation:", end-start)
    
    start = time.perf_counter()
    calibration_parameters = non_linear_BFL(data = data_patch, setup_parameters = setup_parameters, 
                                            assumed_calibration_parameters=assumed_parameters)

    end = time.perf_counter()
    print("Bright field localization:", end-start)

    

def test_BFL():
    lens = INFINITYCORRECTED_2X


    simulation_parameters = Calibration_parameters(delta_x = 50e-6,
                                                   delta_y = 50e-6,
                                                   LED_distance = 201e-3,
                                                   alpha = 0.03,
                                                   beta = 0.02,
                                                   gamma = -0.01)
    
    assumed_parameters = LED_calibration_parameters(LED_distance = 200e-3,
                                                    LED_x_offset = 0e-6,
                                                    LED_y_offset = 0e-6,
                                                    LED_rotation = 0)

    start = time.perf_counter()
    camera = HAMAMATSU_C11440_42U30
    LED_array = MAIN_LED_ARRAY


    setup_parameters = simulate_setup_parameters(
        lens = lens,
        camera = camera,
        LED_array = LED_array
        )
    
    nm_range = np.arange(-2,3)
    N, M = np.meshgrid(nm_range, nm_range)
    n_vals = N.flatten()
    m_vals = M.flatten()

    LED_indices = np.array([n_vals, m_vals]).transpose() + np.array(setup_parameters.LED_info.center_indices)
    
    x_range = np.arange(1, setup_parameters.camera.raw_image_size[0]+1)
    y_range = np.arange(1, setup_parameters.camera.raw_image_size[1]+1)
    X, Y = np.meshgrid(x_range, y_range)


    images = []
    for n, m in zip(n_vals, m_vals):
        center, radius = calculate_BF_edge_circle(setup_parameters = setup_parameters,
                                                  calibration_parameters = simulation_parameters,
                                                  inverse_object_to_lens_distance = 0,
                                                  numerical_aperture = setup_parameters.lens.NA,
                                                  LED_n = n,
                                                  LED_m = m
                                                  )
        image = ((X-center[0])**2 + (Y-center[1])**2 < radius**2)
        images.append(image)        
        
    simulated_data = Simulated_data(LED_indices=LED_indices, amplitude_images=np.array(images))
    data_patch = Data_patch(simulated_data,
                            raw_image_size = setup_parameters.camera.raw_image_size,
                            patch_offset = [0,0],
                            patch_size = setup_parameters.camera.raw_image_size
                            )

    end = time.perf_counter()
    print("Simulation:", end-start)
    
    start = time.perf_counter()
    calibration_parameters = non_linear_BFL(data = data_patch, setup_parameters = setup_parameters, 
                                            assumed_calibration_parameters=assumed_parameters)

    end = time.perf_counter()
    print("Bright field localization:", end-start)


