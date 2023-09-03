class Camera(object):
    def __init__(self, ccd_pixel_size, raw_image_size, bit_depth):
        self.ccd_pixel_size = ccd_pixel_size #m
        self.raw_image_size = raw_image_size # number of pixels in [x, y]
        self.bit_depth = bit_depth


HAMAMATSU = Camera(
    ccd_pixel_size = 6.5e-6,
    raw_image_size = [2048, 2048],
    bit_depth = int(2**16 - 1)
    )