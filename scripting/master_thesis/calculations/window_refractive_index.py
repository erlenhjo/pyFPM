import matplotlib.pyplot as plt
import numpy as np

def N(n):
    return (n**2-1)/(n**3)

n = np.linspace(1,3, 1000)
N_val = N(n)
# plt.figure()
# plt.plot(n,N_val)

print(np.max(N_val), N(1.5)/np.max(N_val), N(2.1)/np.max(N_val))
print(np.max(N_val), N(1.4)/np.max(N_val), N(2.4)/np.max(N_val))



# plt.show()

