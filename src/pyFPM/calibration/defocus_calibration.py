import numpy as np
import matplotlib.pyplot as plt

from pyFPM.pre_processing.Preprocessed_data import Preprocessed_data
from pyFPM.pre_processing.Illumination_pattern import Illumination_pattern
from pyFPM.setup.Setup_parameters import Setup_parameters
from pyFPM.setup.Imaging_system import Imaging_system
from pyFPM.recovery.algorithms.Algorithm_result import Algorithm_result

from pyFPM.recovery.algorithms.primitive_FP import primitive_fourier_ptychography_algorithm


def primitive_defocus_calibration(
        preprocessed_data: Preprocessed_data,
        imaging_system: Imaging_system,
        illumination_pattern: Illumination_pattern
    ):
    

    loops = 10
    defocus_range = np.arange(-200,201,20) * 1e-6

    for defocus in defocus_range:
        pupil = imaging_system.get_pupil(defocus = defocus)

        FP_results = primitive_fourier_ptychography_algorithm(
            preprocessed_data = preprocessed_data,
            imaging_system = imaging_system,
            illumination_pattern = illumination_pattern,
            pupil = pupil,
            loops = loops
        )
        
        weighted_obj = (np.mean(preprocessed_data.amplitude_images[illumination_pattern.update_order[0]]) \
                       /  np.mean(abs(FP_results))) * FP_results   

        # % Simulate imaging with weighted object
        # simu_im_seq = recovery.utility.get_im_seq(weighted_obj, im_sys, defocus);

        # sse_per_angle(:) = sum(sum((abs(simu_im_seq)-amplitude_im_seq).^2));
        # % remove the ones ignored from ignore_list
        # ss_error(nr) = sum(sse_per_angle .*(1-ignore_list));



        
        plt.matshow(np.angle(FP_results))
        plt.title(f"defocus = {defocus*1e6:.3f} um")
    plt.show()