from sympy import (symbols, factorial, Sum, sqrt,
                  cos, sin, simplify, atan, lambdify,
                  expand_trig)
import numpy as np
from functools import cache

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

def sympy_convert_zernike_polynomial_to_xy(zernike_polynomial, x, y, rho, theta):
    zernike_polynomial = expand_trig(zernike_polynomial)
    
    rho_conversion = sqrt(x**2 + y**2)
    theta_conversion = atan(y/x)
    zernike_polynomial_xy = zernike_polynomial.subs({rho:rho_conversion, theta:theta_conversion})

    return simplify(zernike_polynomial_xy)

@cache
def get_xy_zernike_polynomial_function(j):
    rho = symbols("ρ", real=True, positive=True)
    theta = symbols("θ", real = True)  
    x, y = symbols("x y", real = True, positive = True) # not true that x and y is positive, but yields correct conversion/simplification :)

    zernike_polynomial = sympy_zernike_polynomial(rho, theta, j)
    zernike_polynomial_xy = sympy_convert_zernike_polynomial_to_xy(zernike_polynomial, x, y, rho, theta)
    
    lambda_function = lambdify((x, y), zernike_polynomial_xy, "numpy")

    return np.vectorize(lambda_function)    

