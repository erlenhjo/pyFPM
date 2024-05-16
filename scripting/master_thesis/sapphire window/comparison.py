from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from matplotlib.patches import ConnectionPatch


main_data_folder = Path.cwd() / "data" / "Master_thesis" / "sapphire window" / "saphire_window_defocus"
main_result_folder = Path.cwd() / "results" / "master_thesis"
window_result_folder = main_result_folder / "window"
window_result_folder.mkdir(parents=True, exist_ok=True)

lens_names = [
    "comp2x",
    "tele3x",
    "inf10x"
]
image_type_names = [
    "best_focus",
    "window_original_focus",
    "window_best_focus"
]

plot_central_region = [1024,1024]

images = []
for lens_name in lens_names:
    for image_type_name in image_type_names:
        file_name = f"{lens_name}_usaf_{image_type_name}.png"
        image = np.array(Image.open(main_data_folder / file_name))
        images.append(image)

vmin = np.min(images)
vmax = np.max(images)

for n, lens_name in enumerate(lens_names):

    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(8,3), constrained_layout = True)

    for m, ax in enumerate(axes):
        ax: plt.Axes = ax
        ax.imshow(images[3*n+m])
        ax.set_axis_off()
        if m == 0:
            ax.set_title("No window")
        if m == 1:
            ax.set_title("Window")
        if m == 2:
            ax.set_title("Window (refocused)")



    fig.savefig(window_result_folder / f"{lens_name}_comparison.png")
    fig.savefig(window_result_folder / f"{lens_name}_comparison.pdf")



plt.show()

            