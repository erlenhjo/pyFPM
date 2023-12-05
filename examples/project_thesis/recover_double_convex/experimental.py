import matplotlib.pyplot as plt

from recover_double_convex import recover_double_convex

def original():
    recover_double_convex(aperture=False, fresnel=False, illumination=False, epry = False)

def original_aperture():
    recover_double_convex(aperture=True, fresnel=False, illumination=False, epry = False)

def illumination():
    recover_double_convex(aperture=False, fresnel=False, illumination=True, epry = False)

def illumination_aperture():
    recover_double_convex(aperture=True, fresnel=False, illumination=True, epry = False)

def fresnel_illumination():
    recover_double_convex(aperture=False, fresnel=True, illumination=True, epry = False)

def fresnel_illumination_aperture():
    recover_double_convex(aperture=True, fresnel=True, illumination=True, epry = False)


if __name__ == "__main__":
    original()
    original_aperture()
    illumination()
    illumination_aperture()
    fresnel_illumination()
    fresnel_illumination_aperture()
    plt.show()
