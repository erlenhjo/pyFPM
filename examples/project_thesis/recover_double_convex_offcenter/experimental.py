import matplotlib.pyplot as plt

from recover_double_convex import recover_double_convex
savefolder = r"C:\Users\erlen\Documents\GitHub\pyFPM\examples\project_thesis\results\recover_double_convex"

def original():
    title = "Original"
    fig = recover_double_convex(aperture=False, fresnel=False, 
                                illumination=False, epry = False, title=title)
    fig.savefig(savefolder+r"\phase_"+title+".pdf")

def original_aperture():
    title = "Aperture"
    fig = recover_double_convex(aperture=True, fresnel=False, illumination=False, epry = False, title=title)
    fig.savefig(savefolder+r"\phase_"+title+".pdf")

def illumination():
    title = "Illumination"
    fig = recover_double_convex(aperture=False, fresnel=False, illumination=True, epry = False, title=title)
    fig.savefig(savefolder+r"\phase_"+title+".pdf")

def illumination_aperture():
    title = "Illumination + Aperture"
    fig = recover_double_convex(aperture=True, fresnel=False, illumination=True, epry = False, title=title)
    fig.savefig(savefolder+r"\phase_"+title+".pdf")

def fresnel_illumination():
    title = "Illumination + Fresnel"
    fig = recover_double_convex(aperture=False, fresnel=True, illumination=True, epry = False, title=title)
    fig.savefig(savefolder+r"\phase_"+title+".pdf")

def fresnel_illumination_aperture():
    title = "Illumination + Fresnel + Aperture"
    fig = recover_double_convex(aperture=True, fresnel=True, illumination=True, epry = False, title=title)
    fig.savefig(savefolder+r"\phase_"+title+".pdf")


if __name__ == "__main__":
    original()
    #original_aperture()
    #illumination()
    #illumination_aperture()
    #fresnel_illumination()
    #fresnel_illumination_aperture()
    # plt.show()
