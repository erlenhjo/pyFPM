from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from matplotlib.patches import ConnectionPatch


main_data_folder = Path.cwd() / "data" / "Master_thesis" / "fujinon"
main_result_folder = Path.cwd() / "results" / "master_thesis"
fujinon_result_folder = main_result_folder / "fujinon"
fujinon_result_folder.mkdir(parents=True, exist_ok=True)

image_1p8 = np.array(Image.open(main_data_folder / "BF_region_fnr_1,8.png"))
image_4 = np.array(Image.open(main_data_folder / "BF_region_fnr_4.png"))
image_8 = np.array(Image.open(main_data_folder / "BF_region_fnr_8.png"))
image_16 = np.array(Image.open(main_data_folder / "BF_region_fnr_16.png"))
images = [image_1p8, image_4, image_8, image_16]
titles = ["f#=1.8", "f#=4" , "f#=8", "f#=16"]


fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8,4), constrained_layout = True)

vmin = np.min(images)
vmax = np.max(images)


ax.imshow(image_1p8)
ax.set_axis_off()
for im in ax.get_images():
    im.set_clim(vmin=vmin, vmax=vmax)

x, y, size = (1395, 1395, 450)
start_x = x - size//2
stop_x = x + size//2
start_y = y - size//2
stop_y = y + size//2

inset_axes_size = [0.43, 0.43] # width, height
inset_axes_pos = [
    [1.05, 0.52],
    [1.05, 0],
    [1.55, 0.52],
    [1.55, 0]
]

border_thickness = 1
border_color = "black"
inset_line_color = "red"

for n, (inset_axes_position, image, title) in enumerate(zip(inset_axes_pos, images, titles)):    
    subimage = image[start_y:stop_y, start_x:stop_x]

    axin = ax.inset_axes(
        inset_axes_position + inset_axes_size,
        xlim = (start_x, stop_x),
        ylim = (start_y, stop_y)
    )
    axin.set_title(title)

    if n == 0:
        _, connector_lines = ax.indicate_inset_zoom(axin, edgecolor=inset_line_color)
        for line in connector_lines:
            line: ConnectionPatch = line
            line.set_visible(True)

    axin.set_xlim(auto=True)
    axin.set_ylim(auto=True)
    axin.imshow(subimage)
    axin.set_xticks([])
    axin.set_yticks([])

    axin.spines['bottom'].set_color(border_color)
    axin.spines['bottom'].set_linewidth(border_thickness)
    axin.spines['top'].set_color(border_color) 
    axin.spines['top'].set_linewidth(border_thickness) 
    axin.spines['right'].set_color(border_color)
    axin.spines['right'].set_linewidth(border_thickness)
    axin.spines['left'].set_color(border_color)
    axin.spines['left'].set_linewidth(border_thickness)


    for im in axin.get_images():
        im.set_clim(vmin=np.min(image), vmax=np.max(image))




fig.savefig(fujinon_result_folder / "fujinon_fnumber.png")
fig.savefig(fujinon_result_folder / "fujinon_fnumber.pdf")



plt.show()

            