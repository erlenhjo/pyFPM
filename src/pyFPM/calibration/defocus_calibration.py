import numpy as np
import matplotlib.pyplot as plt

from pyFPM.pre_processing.Preprocessed_data import Preprocessed_data
from pyFPM.pre_processing.Illumination_pattern import Illumination_pattern
from pyFPM.setup.Imaging_system import Imaging_system
from pyFPM.recovery.utility.FPM_error import computeFPMerror


from pyFPM.recovery.algorithms.primitive_FP import primitive_fourier_ptychography_algorithm


def primitive_defocus_calibration(
        preprocessed_data: Preprocessed_data,
        imaging_system: Imaging_system,
        illumination_pattern: Illumination_pattern
    ):
    

    loops = 10
    defocus_range = np.arange(-200,201,20) * 1e-6

    errors = []

    for defocus in defocus_range:
        pupil = imaging_system.get_pupil(defocus = defocus)

        FP_results = primitive_fourier_ptychography_algorithm(
            preprocessed_data = preprocessed_data,
            imaging_system = imaging_system,
            illumination_pattern = illumination_pattern,
            pupil = pupil,
            loops = loops
        )
        
        sum_square_error = computeFPMerror(
            preprocessed_data=preprocessed_data,
            imaging_system=imaging_system,
            illumination_pattern=illumination_pattern,
            algorithm_result=FP_results
        )

        errors.append(sum_square_error)

        if abs(defocus) < 1e-6:
            plt.imshow(np.abs(FP_results.recovered_object)**2)
            plt.show()


    plt.scatter(defocus_range*1e6,errors)
    plt.title("Sum square error per defocus")
    plt.xlabel("Defocus [µm]")
    plt.ylabel("SSE [a.u.]")
    plt.tight_layout()
    plt.show()



        
