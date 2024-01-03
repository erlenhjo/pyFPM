import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

fig = plt.figure()
ax = fig.add_axes([0.05, 0.80, 0.9, 0.1])

cb = mpl.colorbar.ColorbarBase(ax, orientation='horizontal', 
                               cmap='viridis',
                               norm=mpl.colors.Normalize(-np.pi, np.pi),  # vmax and vmin
                               label='Recovered phase'
                               )

plt.savefig(r'C:\Users\erlen\Documents\GitHub\pyFPM\examples\project_thesis\results\illustrations\phase_colorbar_viridis', bbox_inches='tight')