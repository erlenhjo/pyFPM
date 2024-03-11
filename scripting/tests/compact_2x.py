focal_length = 60.18e-3
magnification = 2
working_distance = 92e-3
total_length = 280e-3
objective_size = 18e-3
objective_to_detector = 170e-3



z_1 = focal_length*(1+1/magnification)
z_2 = z_1*magnification

print(z_1,z_2)


z_0 = 200e-3

dx = 6.5e-6/magnification
x_max = dx*1024

import numpy as np
import matplotlib.pyplot as plt

x_c = np.linspace(-x_max,x_max, 1000)

NA_scaled = 0.06*z_1

x_i = 0
f_xi = (x_c-x_i)*z_1/z_0 + x_c
x_i = 6e-3
f_xi_2 = (x_c-x_i)*z_1/z_0 + x_c

fx_mesh, fy_mesh = np.meshgrid(f_xi, f_xi)
plt.matshow(np.sqrt(fx_mesh**2+fy_mesh**2)<=NA_scaled)

fx_mesh, fy_mesh = np.meshgrid(f_xi_2, f_xi)
plt.matshow(np.sqrt(fx_mesh**2+fy_mesh**2)<=NA_scaled)

fx_mesh, fy_mesh = np.meshgrid(f_xi_2, f_xi_2)
plt.matshow(np.sqrt(fx_mesh**2+fy_mesh**2)<=NA_scaled)
plt.show()