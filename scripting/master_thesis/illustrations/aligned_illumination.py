from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

datapath = Path.cwd() / "data" / "Assorted" / "Aligned_telecentric.tif"

main_result_folder = Path.cwd() / "results" / "master_thesis"
illustration_folder = main_result_folder / "illustrations"
illustration_folder.mkdir(parents=True, exist_ok=True)

image = np.array(Image.open(datapath))

fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(2.5,2.5), constrained_layout = True)
ax.matshow(image)
ax.set_axis_off()

fig.savefig(illustration_folder / "illustrate_alignment.png")
fig.savefig(illustration_folder / "illustrate_alignment.pdf")
