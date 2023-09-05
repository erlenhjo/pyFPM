class Algorithm_result(object):
    def __init__(self, recovered_object, recovered_object_fourier_transform, pupil, convergence_index):
        self.recovered_object = recovered_object
        self.recovered_object_fourier_transform = recovered_object_fourier_transform
        self.pupil = pupil
        self.convergence_index = convergence_index