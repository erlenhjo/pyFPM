import matplotlib.pyplot as plt

from recover_telecentric import recover_telecentric


def noisy_original():
    recover_telecentric(noise_reduction=False, adaptive=False, epry=False, aperture=False)

def original():
    recover_telecentric(noise_reduction=True, adaptive=False, epry=False, aperture=False)

def original_adaptive():
    recover_telecentric(noise_reduction=True, adaptive=True, epry=False, aperture=False)

def epry():
    recover_telecentric(noise_reduction=True, adaptive=False, epry=True, aperture=False)

def epry_adaptive():
    recover_telecentric(noise_reduction=True, adaptive=True, epry=True, aperture=False)

def original_adaptive_aperture():
    recover_telecentric(noise_reduction=True, adaptive=True, epry=False, aperture=True)

def epry_adaptive_aperture():
    recover_telecentric(noise_reduction=True, adaptive=True, epry=True, aperture=True)


if __name__ == "__main__":
    #noisy_original()
    #original()
    #original_adaptive()
    #original_adaptive_aperture()
    #epry()
    epry_adaptive()
    epry_adaptive_aperture()
    plt.show()
