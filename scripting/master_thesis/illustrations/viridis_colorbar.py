import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from pathlib import Path

main_result_folder = Path.cwd() / "results" / "master_thesis"
illustration_folder = main_result_folder / "illustrations"
illustration_folder.mkdir(parents=True, exist_ok=True)

fig, ax = plt.subplots(1,1,figsize=(0.5,3))

cb = mpl.colorbar.ColorbarBase(ax, orientation='vertical', 
                               cmap='viridis',
                               norm=mpl.colors.Normalize(-np.pi, np.pi),  # vmax and vmin
                               label='Phase'
                               )

fig.savefig(illustration_folder / "phase_colorbar_viridis.pdf", bbox_inches='tight')





