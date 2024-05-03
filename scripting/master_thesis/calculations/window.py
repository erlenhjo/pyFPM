from pyFPM.aberrations.pupils.defocus_and_window import spherical_aberration_from_window_zernike_coefficient
from pyFPM.NTNU_specific.components import INFINITYCORRECTED_10X, INFINITYCORRECTED_2X, INFINITYCORRECTED_50X, TELECENTRIC_3X
from pyFPM.aberrations.zernike_polynomials.fast_synthesis import evaluate_zernike_polynomial

import numpy as np
import matplotlib.pyplot as plt

def get_spherical_zernike_aberration(coefficient):
    points = 1001
    x = np.linspace(-1,1,points, endpoint=True)
    y = np.linspace(-1,1,points, endpoint=True)
    x_mesh, y_mesh = np.meshgrid(x,y)
    
    unit_disk = x_mesh**2 + y_mesh**2 <= 1
    zernike_mode = evaluate_zernike_polynomial(x_mesh, y_mesh, 11) * unit_disk * coefficient

    return zernike_mode


zernike_coefficient = spherical_aberration_from_window_zernike_coefficient(
    refractive_index = 1.77,
    thickness = 5e-3,
    numerical_aperture = INFINITYCORRECTED_2X.NA,
    frequency = 1/520e-9
)
zernike_pupil = get_spherical_zernike_aberration(zernike_coefficient)
print(zernike_coefficient)
plt.matshow((zernike_pupil + np.pi) % (2 *np.pi) - np.pi, vmin=-np.pi, vmax=np.pi)

zernike_coefficient = spherical_aberration_from_window_zernike_coefficient(
    refractive_index = 1.77,
    thickness = 5e-3,
    numerical_aperture = TELECENTRIC_3X.NA,
    frequency = 1/520e-9
)
zernike_pupil = get_spherical_zernike_aberration(zernike_coefficient)
print(zernike_coefficient)
plt.matshow((zernike_pupil + np.pi) % (2 *np.pi) - np.pi, vmin=-np.pi, vmax=np.pi)

zernike_coefficient = spherical_aberration_from_window_zernike_coefficient(
    refractive_index = 1.77,
    thickness = 5e-3,
    numerical_aperture = INFINITYCORRECTED_10X.NA,
    frequency = 1/520e-9
)
zernike_pupil = get_spherical_zernike_aberration(zernike_coefficient)
print(zernike_coefficient)
plt.matshow((zernike_pupil + np.pi) % (2 *np.pi) - np.pi, vmin=-np.pi, vmax=np.pi)

zernike_coefficient = spherical_aberration_from_window_zernike_coefficient(
    refractive_index = 1.77,
    thickness = 5e-3,
    numerical_aperture = INFINITYCORRECTED_50X.NA,
    frequency = 1/520e-9
)
zernike_pupil = get_spherical_zernike_aberration(zernike_coefficient)
print(zernike_coefficient)
plt.matshow((zernike_pupil + np.pi) % (2 *np.pi) - np.pi, vmin=-np.pi, vmax=np.pi)


n = np.linspace(1,3, 1000)
N = (n**2-1)/(n**3)
plt.figure()
plt.plot(n,N)

plt.show()