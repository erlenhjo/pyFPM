import numpy as np
from numba import njit

@njit(cache=True)
def factorial(n):
    res = 1
    for i in range(2, n+1):
        res *= i
    return res

@njit(cache=True)
def get_Noll_indices(j):
    n = np.floor((np.sqrt(2*j-1)+0.5)-1)

    if n % 2 == 0:
        m = 2 * np.floor((2*j+1-n*(n+1)) / 4)
    elif n % 2 == 1:
        m = 2 * np.floor((2*(j+1)-n*(n+1)) / 4) - 1

    return int(n), int(m)

@njit(cache=True)
def evaluate_radial_polynomial(rho, n, m):
    sum = rho * 0
    for s in range((n-m)//2 + 1):
        sum += (((-1)**s * factorial(n-s))/(factorial(s) * factorial((n+m)//2 - s) * factorial((n-m)//2 - s))) * rho**(n-2*s)
    return sum

@njit(cache=True)
def evaluate_zernike_polynomial(x, y, j):
    rho = np.sqrt(x**2 + y**2)
    theta = np.angle(x+1j*y)
    n, m = get_Noll_indices(j)
    radial_polynomial = evaluate_radial_polynomial(rho, n, m)

    if m == 0:
        zernike_polynomial = np.sqrt(n+1) * radial_polynomial
    elif j % 2 == 0:
        zernike_polynomial = np.sqrt(2*(n+1)) * radial_polynomial * np.cos(m * theta)
    elif j % 2 == 1:
        zernike_polynomial = np.sqrt(2*(n+1)) * radial_polynomial * np.sin(m * theta)

    return zernike_polynomial
