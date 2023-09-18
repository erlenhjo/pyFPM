import matplotlib.pyplot as plt
import numpy as np

# setup imports
from pyFPM.setup.Illumination_pattern import Illumination_pattern
from pyFPM.setup.Preprocessed_data import Preprocessed_data

# recovery method imports
from pyFPM.recovery.algorithms.Algorithm_result import Algorithm_result

def plot_results(
        preprocessed_data: Preprocessed_data, 
        illumination_pattern: Illumination_pattern, 
        algorithm_result: Algorithm_result
    ):
    plt.figure()
    plt.title(f"Final image")
    plt.imshow(np.abs(algorithm_result.recovered_object)**2)
    plt.axis("off")

    plt.figure()
    plt.title(f"Preprocessed image")
    plt.imshow(preprocessed_data.amplitude_images[illumination_pattern.update_order[0]]**2)
    plt.axis("off")

    plt.figure()
    plt.title(f"Pupil")
    plt.imshow(np.angle(algorithm_result.pupil))
    plt.axis("off")
    plt.show()
