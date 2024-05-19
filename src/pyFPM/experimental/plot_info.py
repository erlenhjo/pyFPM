from dataclasses import dataclass
from aenum import MultiValueEnum

@dataclass
class Plot_types:
    overview: bool
    object_overview: bool
    raw_image_with_zoom: bool
    recovered_intensity_with_zoom: bool
    recovered_intensity_zoom_only: bool
    recovered_phase: bool
    recovered_phase_with_zoom: bool
    recovered_phase_zoom_only: bool
    recovered_pupil_amplitude: bool
    recovered_pupil_phase: bool
    recovered_pupil_coefficients: bool
    recovered_pupil_overview: bool
    recovered_spectrum: bool

class Zoom_location(MultiValueEnum):
    _init_ = "value coordinates"
    left = 1,  (-1.05, 0)
    right = 2, (1.05, 0)
    above = 3, (0, 1.05)
    below = 4, (0, -1.05)

@dataclass
class Plot_parameters:
    format: str
    zernike_coefficient_max: float
    zernike_coefficient_min: float
    max_zernike_j: int
    low_res_intensity_zoom_location: Zoom_location
    recovered_intensity_zoom_location: Zoom_location
    recovered_phase_zoom_location: Zoom_location
    zoom_ratio: float