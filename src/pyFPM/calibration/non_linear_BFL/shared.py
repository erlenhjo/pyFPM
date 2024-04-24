import numpy as np
from dataclasses import dataclass

@dataclass
class Calibration_parameters:
    delta_x: float
    delta_y: float
    rotation: float
    numerical_aperture_times_LED_distance: float
    distance_ratio: float



def evaluate_circle_score_non_linear(edges_per_image, centers_x_per_image,
                                    centers_y_per_image, radius):
    score = 0
    for edges, center_x, center_y in zip(edges_per_image, centers_x_per_image, centers_y_per_image):
        distance_from_center = np.sqrt((edges[:,0]-center_x)**2 + (edges[:,1]-center_y)**2)
        score += np.sum(np.abs(distance_from_center-radius)**2)/len(distance_from_center)
    return score



def calculate_centers_and_radius(LED_n, LED_m, LED_pitch, pixel_size,
                                 delta_x, delta_y, rotation,
                                 numerical_aperture_times_LED_distance,
                                 distance_ratio
                                ):
    r_xx = np.cos(rotation)
    r_xy = np.sin(rotation)
    r_yx = -np.sin(rotation)
    r_yy = np.cos(rotation)
    
    if (1+distance_ratio) == 0:
        distance_ratio -= 1e-6

    LEDs_x = LED_pitch*LED_n*r_xx + LED_pitch*LED_m*r_xy
    LEDs_y = LED_pitch*LED_n*r_yx + LED_pitch*LED_m*r_yy

    radius = numerical_aperture_times_LED_distance / pixel_size / (1 + distance_ratio)
    centers_x = (LEDs_x + delta_x) / pixel_size \
                / (1 + distance_ratio)
    centers_y = (LEDs_y + delta_y) / pixel_size \
                / (1 + distance_ratio)
    
    return centers_x, centers_y, radius


