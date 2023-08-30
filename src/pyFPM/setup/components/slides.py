class Slide(object):
    def __init__(self, thickness, refractive_index):
        self.thickness = thickness #m
        self.refractive_index = refractive_index


THIN_SLIDE = Slide(
    thickness = 0,
    refractive_index = 1
    )

DUMMY_THICK_SLIDE = Slide(
    thickness = 5e-3,
    refractive_index = 1.46
)