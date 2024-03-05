import numpy as np
import matplotlib.pyplot as plt

def test_1():
    focal_length = 36e-3
    extension_lengths = [100e-3, 5.6e-3, 2e-3]
    z_2 = sum(extension_lengths)
    z_1 = 1/(1/focal_length-1/z_2)
    magnification = z_2/z_1


    print(focal_length)
    print(z_2)
    print(z_1)
    print(magnification)

    wavelength=587.6e-9
    diameter = 6e-3

    NA = diameter/(2*z_1)
    print(NA)

def test_1_2():
    focal_length = 60.33e-3
    magnification = 2
    z_2 = (1+magnification)*focal_length
    z_1 = (1+1/magnification)*focal_length

    print(focal_length)
    print(z_2)
    print(z_1)
    print(magnification)

    wavelength=587.6e-9
    diameter = 11e-3

    NA = diameter/(2*z_1)
    print(NA)



def test_2():
    wavelength = 520e-9
    f_0 = 1 /wavelength
    magnification = 2
    pixel_size = 6.5e-6/magnification
    NA = 0.055
    cutoff_frequency = NA*f_0
    M = 256

    max_f = 1 / (2 * pixel_size)
    spatial_frequencies_x = np.linspace(start = -max_f, stop = max_f, num = M, endpoint = True)  
    spatial_frequencies_y = np.linspace(start = -max_f, stop = max_f, num = M, endpoint = True)

    fx_mesh, fy_mesh = np.meshgrid(spatial_frequencies_x, spatial_frequencies_y)

    print(spatial_frequencies_x[1]-spatial_frequencies_x[0])
    print(1/(M*pixel_size))
    CTF = fx_mesh**2 + fy_mesh**2 < cutoff_frequency**2

    plt.matshow(CTF)
    plt.show()

def test_3():
    wavelength = 520e-9
    magnification = 4
    image_pixel_size = 2.5e-6
    z_1 = 12.5e-3
    lens_diameter = 2.4e-3
    M = 512
    
    lens_pixel_size = wavelength * z_1 * magnification / (M*image_pixel_size)


    lens_x = np.arange(start = -M//2, stop = M//2) * lens_pixel_size  
    lens_y = np.arange(start = -M//2, stop = M//2) * lens_pixel_size

    lens_x_mesh, lens_y_mesh = np.meshgrid(lens_x, lens_y)

    CTF = lens_x_mesh**2 + lens_y_mesh**2 < (lens_diameter/2)**2

    plt.pcolor(lens_x*1000, lens_y*1000, CTF)
    plt.show()


if __name__=="__main__":
    test_2()
    #test_3()
    #test_1_2()
