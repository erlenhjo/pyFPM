class Camera(object):
    def __init__(self, ccd_pixel_size, image_size):
        self.ccd_pixel_size = ccd_pixel_size #m
        self.image_size = image_size # number of pixels in [x, y]
        #bitdepth?


HAMAMATSU = Camera(
    ccd_pixel_size = 6.5e-6,
    image_size = [2048, 2048]
)