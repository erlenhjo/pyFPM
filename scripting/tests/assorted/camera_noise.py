from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

hammamatsu_background_file = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\Fourier_Ptychography\telecentric_3x_dotarray\dark_image.tiff"
IDS_U3_background_file = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\Master_thesis\defocus_190124\telecentric_dot_focused_5\dark_image.png"
hammamatsu_image_file = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\Fourier_Ptychography\telecentric_3x_dotarray\0_18-16_16.tiff"
IDS_U3_image_file = r"C:\Users\erlen\Documents\GitHub\pyFPM\data\Master_thesis\defocus_190124\telecentric_dot_focused_5\0_12-16_16.png"

hammamatsu_background = np.array(Image.open(hammamatsu_background_file))
hammamatsu_image = np.array(Image.open(hammamatsu_image_file))
IDS_U3_background = np.array(Image.open(IDS_U3_background_file))
IDS_U3_image = np.array(Image.open(IDS_U3_image_file))

plt.matshow(hammamatsu_background)
plt.colorbar()
plt.matshow(hammamatsu_image)
plt.colorbar()
plt.matshow(IDS_U3_background)
plt.colorbar()
plt.matshow(IDS_U3_image)
plt.colorbar()
plt.show()