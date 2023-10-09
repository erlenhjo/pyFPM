from sympy import symbols
import matplotlib.pyplot as plt
from matplotlib import patches
import numpy as np
import time

from pyFPM.aberration_detection.zernike_polynomials.synthesise_zernike_polynomials import (sympy_convert_zernike_polynomial_to_xy, 
                                                                                sympy_zernike_polynomial, 
                                                                                get_Noll_indices, 
                                                                                get_xy_zernike_polynomial_function)

def print_zernike_polynomials():
    rho = symbols("ρ", real=True, positive=True)
    theta = symbols("θ", real = True)  
    x, y = symbols("x y", real = True, positive = True) # not true that x and y is positive, but yields correct conversion/simplification :)

    for j in range(16, 38):
        print(j, get_Noll_indices(j), end = "\t")
        zernike_polynomial = sympy_zernike_polynomial(rho, theta, j)
        #print(zernike_polynomial, end="\t")
        zernike_polynomial_xy = sympy_convert_zernike_polynomial_to_xy(zernike_polynomial, x, y, rho, theta)
        print(zernike_polynomial_xy)
    
def get_image_of_zernike_polynomial(j):
    points = 1001
    x = np.linspace(-1,1,points, endpoint=True)
    y = np.linspace(-1,1,points, endpoint=True)
    x_mesh, y_mesh = np.meshgrid(x,y)
    
    unit_disk = x_mesh**2 + y_mesh**2 <= 1
    zernike_polynomial_function = get_xy_zernike_polynomial_function(j)
    zernike_mode = zernike_polynomial_function(x_mesh, y_mesh) * unit_disk

    return zernike_mode


def plot_zernike_pyramid():
    j_range = np.arange(1, 22)
    n_vals, m_vals = zip(*[get_Noll_indices(j) for j in j_range])
    n_min, n_max, m_max = min(n_vals), max(n_vals), max(m_vals) 

    subplot_size = 9
    subplot_spacing = 3
    fig_size_x = subplot_size * (n_max - n_min + 1)
    fig_size_y = (subplot_size) * (m_max + 1)  + subplot_spacing * m_max

    fig = plt.figure()
    fig.suptitle("Zernike modes")
    gs = fig.add_gridspec(fig_size_x, fig_size_y)

    for j in j_range:
        n, m = get_Noll_indices(j)
        x_start = n * subplot_size
        x_stop = x_start + subplot_size

        if j % 2 == 0:
            cosine = True
        else:
            cosine = False  # it is a sine
        m_eff = (2*cosine-1) * m # +m for cosine, -m for sine

        y_start = (m_max+m_eff)//2 * subplot_size + (m_max+m_eff)//2 * subplot_spacing + (subplot_size+subplot_spacing)//2 * ((n_max - n) % 2)
        y_stop = y_start + subplot_size
        ax = plt.subplot(gs[x_start:x_stop ,y_start:y_stop])

        zernike_mode_image = get_image_of_zernike_polynomial(j)
        im_size = zernike_mode_image.shape[0]
        image = ax.imshow(zernike_mode_image)
        clip_circle = patches.Circle(xy=(im_size//2, im_size//2), radius = im_size//2-im_size//100, transform=ax.transData)
        image.set_clip_path(clip_circle)
        ax.axis("off")

    plt.show()

def time_function_creation():
    total_time_start = time.perf_counter()
    J=50
    for j in range(1, J+1):
        start = time.perf_counter() 
        get_xy_zernike_polynomial_function(j)
        end = time.perf_counter()
        print(f"Time for j={j} was {end-start} s")

    total_time_end = time.perf_counter()
    print(f"Time for all j between {1} and {J} was {total_time_end-total_time_start} s")

if __name__ == "__main__":
    plot_zernike_pyramid()
    #time_function_creation()
    #time_function_creation()