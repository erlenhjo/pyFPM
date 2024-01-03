from PIL import Image
import matplotlib.pyplot as plt
import numpy as np


filepath = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\Assorted\Aligned_telecentric.tif"

image = np.array(Image.open(filepath))

fig_0, axes_0 = plt.subplots(nrows=1, ncols=1, figsize=(2.5,2.5), constrained_layout = True)
axes_0.matshow(image)
axes_0.set_axis_off()

fig_0.savefig(r"C:\Users\erlen\Documents\GitHub\pyFPM\examples\project_thesis\results\illustrations"+r"\alignment.png")