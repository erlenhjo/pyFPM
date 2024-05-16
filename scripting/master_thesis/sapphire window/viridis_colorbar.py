import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from pathlib import Path

main_result_folder = Path.cwd() / "results" / "master_thesis" / "window"
main_result_folder.mkdir(parents=True, exist_ok=True)

fig_phase, (ax_amp, ax_phase) = plt.subplots(1,2,figsize=(10,0.5), width_ratios=[1,1])
phase_limits = [-0.86, 0.86]
amp_limits = [0.2, 1.4]
ax_amp.set_title("Pupil amplitude")
ax_phase.set_title("Pupil phase")

cb_phase = mpl.colorbar.ColorbarBase(ax_phase, 
                                     orientation='horizontal', 
                                     cmap='viridis',
                                     norm=mpl.colors.Normalize(phase_limits[0], phase_limits[1]),  # vmax and vmin
                                     location="top",
                                     ticklocation="bottom"
                                    )

cb_amp = mpl.colorbar.ColorbarBase(ax_amp, 
                                   orientation='horizontal', 
                                   cmap='viridis',
                                   norm=mpl.colors.Normalize(amp_limits[0], amp_limits[1]),  # vmax and vmin
                                   location="top",
                                   ticklocation="bottom"
                                  )

fig_phase.savefig(main_result_folder / "pupil_colorbar_viridis.pdf", bbox_inches='tight')






