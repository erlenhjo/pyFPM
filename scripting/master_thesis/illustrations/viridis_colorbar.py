import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from pathlib import Path

main_result_folder = Path.cwd() / "results" / "master_thesis"
illustration_folder = main_result_folder / "illustrations"
illustration_folder.mkdir(parents=True, exist_ok=True)

fig = plt.figure()
ax = fig.add_axes([0.05, 0.80, 0.9, 0.1])

cb = mpl.colorbar.ColorbarBase(ax, orientation='horizontal', 
                               cmap='viridis',
                               norm=mpl.colors.Normalize(-np.pi, np.pi),  # vmax and vmin
                               label='Recovered phase'
                               )

fig.savefig(illustration_folder / "phase_colorbar_viridis.pdf", bbox_inches='tight')
fig.savefig(illustration_folder / "phase_colorbar_viridis.png", bbox_inches='tight')




