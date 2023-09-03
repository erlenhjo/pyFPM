class Algorithm_result(object):
    def __init__(self, object, object_fourier_transform, pupil, loop_error):
        self.object = object
        self.object_fourier_transform = object_fourier_transform
        self.pupil = pupil
        self.loop_error = loop_error