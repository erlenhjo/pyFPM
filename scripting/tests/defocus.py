# FPM imports
from pyFPM.NTNU_specific.components import TELECENTRIC_3X
from pyFPM.setup.Imaging_system import LED_calibration_parameters
from pyFPM.setup.Setup_parameters import Setup_parameters, Lens, LED_infos
from pyFPM.setup.Imaging_system import Imaging_system, calculate_frequency_mesh_grids
from pyFPM.NTNU_specific.components import IDS_U3_31J0CP_REV_2_2, MAIN_LED_ARRAY
from pyFPM.aberrations.pupils.zernike_pupil import decompose_zernike_pupil

import matplotlib.pyplot as plt
import numpy as np
from skimage.restoration import unwrap_phase

def main():
    defocus_values = np.array([-500,-100,100,500])
    for defocus in defocus_values:
        imaging_system = setup_lens(lens = TELECENTRIC_3X)

        pixel_size = imaging_system.raw_object_pixel_size
        frequency = imaging_system.frequency
        image_region_size = imaging_system.patch_size

        fx_mesh, fy_mesh = calculate_frequency_mesh_grids(pixel_size=pixel_size, image_region_size=image_region_size)
        fz_mesh = np.emath.sqrt(frequency**2 - fx_mesh**2 - fy_mesh**2)
        print(frequency, np.max(fx_mesh))
        #pupil_phase = 2*np.pi*defocus*1e-6*np.real(fz_mesh)
        pupil_phase = 2*np.pi*defocus*np.real(fz_mesh)
        #pupil_phase = 2*np.pi*defocus*1e-6/(2*frequency)*(fx_mesh**2+fy_mesh**2)  
    
        plot_results(imaging_system, pupil_phase, defocus) 

    plt.show()



def setup_lens(
    lens: Lens
):
    pixel_scale_factor = 4
    calibration_parameters = LED_calibration_parameters(200e-3,0,0,0)
    patch_start = np.array([2856, 2848], dtype=int) // 2 - 256
    patch_size = [512, 512]

    camera = IDS_U3_31J0CP_REV_2_2
    dummy_LED_info: LED_infos = LED_infos( 
            LED_pitch = MAIN_LED_ARRAY.LED_pitch, 
            wavelength = MAIN_LED_ARRAY.green.wavelength, 
            LED_array_size = MAIN_LED_ARRAY.array_size,
            LED_offset = MAIN_LED_ARRAY.green.offset, 
            center_indices = [16,16], 
            exposure_times = 0
        )

    setup_parameters: Setup_parameters = Setup_parameters(
        lens=lens,
        LED_info=dummy_LED_info,
        camera=camera,
        image_format=""
    )
    imaging_system = Imaging_system(
        setup_parameters = setup_parameters,
        pixel_scale_factor = pixel_scale_factor,
        patch_start = patch_start,
        patch_size = patch_size,
        LED_calibration_parameters=calibration_parameters
    )

    return imaging_system


def plot_results(
        imaging_system: Imaging_system,
        pupil_phase,
        defocus
    ):
    fig, axes = plt.subplots(nrows=1, ncols=1, layout='constrained')

    axes.set_title(f"Recovered pupil angle")
    axes.matshow(pupil_phase * imaging_system.low_res_CTF)
    axes.axis("off")
    axes.margins(x=0, y=0)

    recovered_zernike_coefficients = decompose_zernike_pupil(imaging_system=imaging_system, pupil=np.exp(1j*pupil_phase), 
                                                             max_j=6)

    fig.suptitle(f"{defocus}, {recovered_zernike_coefficients[4]}")

    return fig


if __name__ == "__main__":
    main()