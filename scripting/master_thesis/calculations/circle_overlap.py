import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-3,3, 10000)
X, Y = np.meshgrid(x,x)

R = 1
d = 1.07 * R

circle_1 = (X**2 + Y**2) <= R**2
circle_2 = ((X-d)**2 + Y**2) <= R**2

A1 = np.sum(circle_1)
A2 = np.sum(circle_2)
A_overlap = np.sum(circle_1 & circle_2)

print(A_overlap/A1)

def get_overlap(z_0, d, NA):    
    Q = d / 2 / z_0 / NA
    return 2/np.pi * (np.arccos(Q) - Q * np.sqrt(1-(Q)**2))

d = 6e-3
z_0 = np.linspace(0e-3, 250e-3, 1000)

plt.plot(z_0*1e3, get_overlap(z_0, d, NA=0.06))
plt.plot(z_0*1e3, get_overlap(z_0, d, NA=0.09))
plt.plot(z_0*1e3, get_overlap(z_0, d, NA=0.28))
plt.show()