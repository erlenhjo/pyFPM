import numpy as np

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

