import os

from PIL import Image
import numpy as np


class Rawdata(object):
    def __init__(self, datadirpath, image_format, background_filename):

        files_in_dataset = os.listdir(datadirpath)

        self.array = np.zeros(shape = (33,33))
 
        for file in files_in_dataset:
            if file.endswith(image_format):
                if file == f"{background_filename}.{image_format}":
                    continue
                im = Image.open(os.path.join(datadirpath, file))
                #im.show()
                x, y = indices_from_image_title(file)

                self.array[y,x] = 1
        
        



def indices_from_image_title(filename: str):
    filename = filename.split(".")[0]
    filename = filename.split("-")[1]
    filename = filename.split("_")

    x_index = int(filename[0])
    y_index = int(filename[1])

    return x_index, y_index
    