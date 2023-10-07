import numpy as np
import matplotlib.pyplot as plt

from pyFPM.setup.Data import Data_patch
from pyFPM.setup.Illumination_pattern import Illumination_pattern
from pyFPM.setup.Imaging_system import Imaging_system
from pyFPM.recovery.error_measures.sum_square_error import compute_sum_square_error


from pyFPM.recovery.algorithms.primitive_algorithm import primitive_fourier_ptychography_algorithm


def primitive_defocus_calibration(
        data_patch: Data_patch,
        imaging_system: Imaging_system,
        illumination_pattern: Illumination_pattern,
        use_epry = False,
        use_gradient_descent = False
    ):
    
    loops = 10
    defocus_range = np.arange(-200,201,20) * 1e-6

    best_image = None
    best_image_defocus = None
    errors = []

    for defocus in defocus_range:
        pupil = imaging_system.get_pupil(defocus = defocus)

        algorithm_results = primitive_fourier_ptychography_algorithm(
            data_patch = data_patch,
            imaging_system = imaging_system,
            illumination_pattern = illumination_pattern,
            pupil = pupil,
            loops = loops,
            use_epry = use_epry,
            use_gradient_descent = use_gradient_descent        )
        
        sum_square_error = compute_sum_square_error(
            data_patch = data_patch,
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
    plt.imshow(data_patch.amplitude_images[illumination_pattern.update_order[0]]**2)
    plt.axis("off")
    plt.show()


        
