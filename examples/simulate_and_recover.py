# FPM imports
from pyFPM.NTNU_specific.simulate_images.simulate_2x import simulate_2x
from pyFPM.simulation.image_simulator import simulate_angled_imaging
from pyFPM.recovery.algorithms.run_algorithm import recover, Method
from pyFPM.recovery.algorithms.Step_description import get_constant_step_description, get_standard_adaptive_step_description
from pyFPM.setup.Data import Data_patch, Simulated_data

# import plotting
from plotting.plot_simulation_results import plot_simulation_results
from plotting.plot_illumination import plot_bright_field_images

import numpy as np
import skimage

def main():
    method = Method.Pseudo_Fresnel_4f
    simulate_spherical_illumination = True

    max_j = 25

    #zernike_coefficients = (np.random.random(max_j+1)*2 - 1) * 0.2
    zernike_coefficients = [ 0.0490545,  -0.06489815, -0.05771678, -0.02830205, -0.03818069,  0.01629342,
                             0.03223081,  0.07773553, -0.01409983,  0.00772039, -0.05556964,  0.07741695,
                            -0.07330059, -0.01082829,  0.06798477, -0.06677369,  0.07063081,  0.06726429,
                            -0.02042763, -0.00730338, -0.00196811, -0.01209849,  0.06464902, -0.04933082,
                             0.07865441,  0.06238114]
    zernike_coefficients = np.array(zernike_coefficients)
    
    zernike_coefficients[0] = 0

    amplitude_image = skimage.data.eagle()[512:1024,512:1024]
    phase_image = np.zeros(shape=amplitude_image.shape)
    high_res_complex_object = amplitude_image * np.exp(1j*phase_image)

    setup_parameters, data_patch, imaging_system, illumination_pattern, applied_pupil, _\
        = simulate_2x(high_res_complex_object, noise_fraction=0, zernike_coefficients=zernike_coefficients, spherical_illumination=simulate_spherical_illumination)
    step_description = get_standard_adaptive_step_description(illumination_pattern, max_iterations=100)

    plot_bright_field_images(data_patch=data_patch, setup_parameters=setup_parameters, array_size=5)

    # define pupil guess
    pupil_guess = applied_pupil * 0 + 1

    algorithm_result = recover(
        method=method,
        data_patch=data_patch,
        imaging_system=imaging_system,
        illumination_pattern=illumination_pattern,
        pupil_guess=pupil_guess,
        step_description=step_description
    )



    recovered_low_res_images \
        = simulate_angled_imaging(
            algorithm_result.recovered_object_fourier_transform,
            algorithm_result.pupil,
            data_patch.LED_indices,
            imaging_system)
    
    recovered_low_res_data = Simulated_data(LED_indices=data_patch.LED_indices, amplitude_images=recovered_low_res_images)

    recovered_data_patch = Data_patch(data = recovered_low_res_data, patch_start=[0, 0], patch_size=recovered_low_res_images[0].shape)
    
    plot_bright_field_images(data_patch=recovered_data_patch, setup_parameters=setup_parameters, array_size=5)

    plot_simulation_results(data_patch, illumination_pattern, imaging_system, algorithm_result, 
                            original_zernike_coefficients=zernike_coefficients, original_pupil=applied_pupil)



def profile_main():
    import cProfile
    import pstats

    with cProfile.Profile() as pr:
        main()
    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.dump_stats(filename=r"profiling_data\simulate_and_recover.prof")

if __name__ == "__main__":
    #profile_main()
    main()