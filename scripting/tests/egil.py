import numpy as np
import matplotlib.pyplot as plt

v = np.arange(100)/50
size = np.arange(100)/(-20)

v_reduced = v[np.argwhere((v>0.5) & (v<1.5))]
size_reduced = size[np.argwhere((v>0.5) & (v<1.5))]

plt.scatter(v, size)
plt.scatter(v_reduced, size_reduced)
plt.show()