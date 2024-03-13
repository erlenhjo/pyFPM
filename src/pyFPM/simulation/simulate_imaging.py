from pyFPM.setup.Imaging_system import Imaging_system, LED_calibration_parameters
from pyFPM.setup.Data import Simulated_data, Data_patch
from pyFPM.setup.Illumination_pattern import Illumination_pattern
from pyFPM.setup.Setup_parameters import Setup_parameters
from pyFPM.simulation.image_simulator import simulate_angled_imaging
from pyFPM.aberrations.pupils.zernike_pupil import get_zernike_pupil
from pyFPM.simulation.apply_gaussian_noise import apply_gaussian_noise

import numpy as np
from numpy.fft import fft2, ifftshift, fftshift


def simulate_imaging(
    high_res_complex_object,
    zernike_coefficients,
    noise_fraction,
    setup_parameters,
    arraysize,
    pixel_scale_factor,
    Fresnel_correction,
    spherical_illumination_correction,
    patch_offset,
    use_aperture_shift,
    calibration_parameters: LED_calibration_parameters
):
      
    # Define simulated data set
    center_LED = setup_parameters.LED_info.center_indices
    x_start = center_LED[0] - arraysize//2
    y_start = center_LED[1] - arraysize//2
    x_stop = x_start + arraysize
    y_stop = y_start + arraysize

    LED_indices = [[x, y] for x in range(x_start, x_stop) for y in range(y_start, y_stop)]

    full_image_imaging_system = Imaging_system(
        setup_parameters = setup_parameters,
        pixel_scale_factor = pixel_scale_factor,
        patch_offset = patch_offset,
        patch_size = setup_parameters.camera.raw_image_size,
        calibration_parameters = calibration_parameters
        )
    
    pupil = get_zernike_pupil(full_image_imaging_system, zernike_coefficients)

    object_plane_phase_shift_correction = 1
    if Fresnel_correction:
        object_plane_phase_shift_correction *= full_image_imaging_system.high_res_Fresnel_correction
    if spherical_illumination_correction: 
        object_plane_phase_shift_correction *= full_image_imaging_system.high_res_spherical_illumination_correction

    high_res_fourier_transform = fftshift(fft2(ifftshift(high_res_complex_object * object_plane_phase_shift_correction)))


    low_res_images \
        = simulate_angled_imaging(
            high_res_fourier_transform,
            pupil,
            LED_indices,
            full_image_imaging_system,
            use_aperture_shift=use_aperture_shift)
    
    
    # for n in range(low_res_images.shape[0]):   # may be used to simulate LED intensity fluctuations temporarily
    #     low_res_images[n] *= np.random.normal(1,0.3)

    illumination_pattern = Illumination_pattern(LED_indices=LED_indices,
                                                imaging_system=full_image_imaging_system,
                                                setup_parameters=setup_parameters,
                                                max_array_size=arraysize) 
    if noise_fraction:
        low_res_images = apply_gaussian_noise(low_res_images = low_res_images, #might not work for arraysize = 1 ? or something?
                                            noise_fraction = noise_fraction, 
                                            relative_NAs = illumination_pattern.relative_NAs, 
                                            LED_indices = LED_indices)


    simulated_data = Simulated_data(LED_indices=LED_indices, amplitude_images=low_res_images)
    
    return simulated_data, pupil, full_image_imaging_system.low_res_CTF

def finalize_simulation_setup(
    setup_parameters: Setup_parameters,
    simulated_data,
    patch_offset,
    patch_size,
    pixel_scale_factor,
    calibration_parameters,
    arraysize
):
    # Adapt simulated dataset for further use

    imaging_system = Imaging_system(
        setup_parameters = setup_parameters,
        pixel_scale_factor = pixel_scale_factor,
        patch_offset = patch_offset,
        patch_size = patch_size,
        calibration_parameters = calibration_parameters
        )

    data_patch = Data_patch(data = simulated_data,
                            raw_image_size = setup_parameters.camera.raw_image_size,
                            patch_offset = [0,0],
                            patch_size = patch_size)

    illumination_pattern = Illumination_pattern(
        LED_indices = simulated_data.LED_indices,
        imaging_system = imaging_system,
        setup_parameters = setup_parameters,
        max_array_size=arraysize
    )

    return data_patch, imaging_system, illumination_pattern





