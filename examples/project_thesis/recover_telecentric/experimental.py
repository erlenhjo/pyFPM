import matplotlib.pyplot as plt

from recover_telecentric import recover_telecentric

savefolder = r"C:\Users\erlen\Documents\GitHub\pyFPM\examples\project_thesis\results\recover_telecentric"
def noisy_original():
    title = "noisy"
    fig = recover_telecentric(noise_reduction=False, adaptive=False, epry=False, aperture=False, title=title)
    fig.savefig(savefolder+r"\phase_"+title+".pdf")

def original():
    title = "original"
    fig = recover_telecentric(noise_reduction=True, adaptive=False, epry=False, aperture=False, title=title)
    fig.savefig(savefolder+r"\phase_"+title+".pdf")

def original_adaptive():
    title = "adaptive"
    fig = recover_telecentric(noise_reduction=True, adaptive=True, epry=False, aperture=False, title=title)
    fig.savefig(savefolder+r"\phase_"+title+".pdf")

def epry():
    title = "epry"
    fig = recover_telecentric(noise_reduction=True, adaptive=False, epry=True, aperture=False, title=title)
    fig.savefig(savefolder+r"\phase_"+title+".pdf")

def epry_adaptive():
    title = "epry + adaptive"
    fig = recover_telecentric(noise_reduction=True, adaptive=True, epry=True, aperture=False, title=title)
    fig.savefig(savefolder+r"\phase_"+title+".pdf")

def original_adaptive_aperture():
    title = "adaptive + aperture"
    fig = recover_telecentric(noise_reduction=True, adaptive=True, epry=False, aperture=True, title=title)
    fig.savefig(savefolder+r"\phase_"+title+".pdf")

def epry_adaptive_aperture():
    title = "adaptive + epry + aperture"
    fig = recover_telecentric(noise_reduction=True, adaptive=True, epry=True, aperture=True, title=title)
    fig.savefig(savefolder+r"\phase_"+title+".pdf")



if __name__ == "__main__":
    noisy_original()
    original()
    original_adaptive()
    original_adaptive_aperture()
    epry()
    epry_adaptive()
    epry_adaptive_aperture()
    # plt.show()
