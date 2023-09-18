import numpy as np
import matplotlib.pyplot as plt

from pyFPM.setup.Preprocessed_data import Preprocessed_data
from pyFPM.setup.Illumination_pattern import Illumination_pattern
from pyFPM.setup.Imaging_system import Imaging_system
from pyFPM.recovery.utility.FPM_error import computeFPMerror


from pyFPM.recovery.algorithms.primitive_algorithm import primitive_fourier_ptychography_algorithm


def primitive_defocus_calibration(
        preprocessed_data: Preprocessed_data,
        imaging_system: Imaging_system,
        illumination_pattern: Illumination_pattern
    ):
    

    loops = 10
    defocus_range = np.arange(-200,201,20) * 1e-6

    best_image = None
    best_image_defocus = None
    errors = []

    for defocus in defocus_range:
        pupil = imaging_system.get_pupil(defocus = defocus)

        algorithm_results = primitive_fourier_ptychography_algorithm(
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
            algorithm_result=algorithm_results
        )

        if best_image is None:
            best_image = np.abs(algorithm_results.recovered_object)**2
            best_image_defocus = defocus
        elif sum_square_error < min(errors):
            best_image = np.abs(algorithm_results.recovered_object)**2
            best_image_defocus = defocus
        
        errors.append(sum_square_error)

    plt.figure()
    plt.title(f"Defocus {best_image_defocus*1e6:.1f} um")
    plt.imshow(best_image)
    plt.axis("off")

    plt.figure()
    plt.scatter(defocus_range*1e6,errors)
    plt.title("Sum square error per defocus")
    plt.xlabel("Defocus [µm]")
    plt.ylabel("SSE [a.u.]")

    plt.figure()
    plt.title(f"Preprocessed image")
    plt.imshow(preprocessed_data.amplitude_images[illumination_pattern.update_order[0]]**2)
    plt.axis("off")
    plt.show()


        
