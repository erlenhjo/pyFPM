from sympy import (symbols, factorial, Sum, sqrt,
                  cos, sin, simplify, atan, lambdify,
                  expand_trig)

import matplotlib.pyplot as plt
from matplotlib import patches
import numpy as np


def get_Noll_indices(j):
    n = np.floor((np.sqrt(2*j-1)+0.5)-1)

    if n % 2 == 0:
        m = 2 * np.floor((2*j+1-n*(n+1)) / 4)
    elif n % 2 == 1:
        m = 2 * np.floor((2*(j+1)-n*(n+1)) / 4) - 1

    return int(n), int(m)

def sympy_radial_polynomial_term(rho, s, n, m):
    a = factorial(n-s)
    numerator = (-1)**s * a
    b = factorial(s)
    c = factorial((n+m)//2 - s)
    d = factorial((n-m)//2 - s)
    denominator = b * c * d
    return numerator/denominator * rho**(n-2*s)

def sympy_radial_polynomial(rho, n, m):
    s = symbols("s", interger = True)
    
    term = sympy_radial_polynomial_term(rho, s, n, m)
    return Sum(term, (s, 0, (n-m)//2))

def sympy_zernike_polynomial(rho, theta, j_val):
    n, m = symbols("n m", integer=True)
    radial_polynomial = sympy_radial_polynomial(rho, n, m)

    n_val, m_val = get_Noll_indices(j_val)
    radial_polynomial = radial_polynomial.subs(n, n_val).subs(m, m_val).doit()

    if m_val == 0:
        zernike_polynomial = sqrt(n_val+1) * radial_polynomial
    elif j_val % 2 == 0:
        zernike_polynomial = sqrt(2*(n_val+1)) * radial_polynomial * cos(m_val * theta)
    elif j_val % 2 == 1:
        zernike_polynomial = sqrt(2*(n_val+1)) * radial_polynomial * sin(m_val * theta)

    return simplify(zernike_polynomial)

def convert_zernike_polynomial_to_xy(zernike_polynomial, x, y, rho, theta):
    zernike_polynomial = expand_trig(zernike_polynomial)
    
    rho_conversion = sqrt(x**2 + y**2)
    theta_conversion = atan(y/x)
    zernike_polynomial_xy = zernike_polynomial.subs({rho:rho_conversion, theta:theta_conversion})

    return simplify(zernike_polynomial_xy)

def get_xy_zernike_polynomial_function(j):
    rho = symbols("ρ", real=True, positive=True)
    theta = symbols("θ", real = True)  
    x, y = symbols("x y", real = True, positive = True) # not true that x and y is positive, but yields correct conversion/simplification :)

    zernike_polynomial = sympy_zernike_polynomial(rho, theta, j)
    zernike_polynomial_xy = convert_zernike_polynomial_to_xy(zernike_polynomial, x, y, rho, theta)
    
    lambda_function = lambdify((x, y), zernike_polynomial_xy, "numpy")

    return lambda_function    

def print_zernike_polynomials():
    rho = symbols("ρ", real=True, positive=True)
    theta = symbols("θ", real = True)  
    x, y = symbols("x y", real = True, positive = True) # not true that x and y is positive, but yields correct conversion/simplification :)

    for j in range(16, 38):
        print(j, get_Noll_indices(j), end = "\t")
        zernike_polynomial = sympy_zernike_polynomial(rho, theta, j)
        #print(zernike_polynomial, end="\t")
        zernike_polynomial_xy = convert_zernike_polynomial_to_xy(zernike_polynomial, x, y, rho, theta)
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
        clip_circle = patches.Circle(xy=(im_size//2, im_size//2), radius = im_size//2-3, transform=ax.transData)
        image.set_clip_path(clip_circle)
        ax.axis("off")



if __name__ == "__main__":
    plot_zernike_pyramid()
    fig, ax = plt.subplots()
    zernike_mode_image = get_image_of_zernike_polynomial(1)
    im_size = zernike_mode_image.shape[0]
    image = ax.imshow(zernike_mode_image)
    clip_circle = patches.Circle(xy=(im_size//2, im_size//2), radius = im_size//2-3, transform=ax.transData)
    image.set_clip_path(clip_circle)
    ax.axis("off")
    plt.show()

