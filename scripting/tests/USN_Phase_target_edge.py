import numpy as np
from numpy.fft import fft2, ifft2, fftshift, ifftshift
import matplotlib.pyplot as plt
from PIL import Image
import os
from scipy.ndimage import zoom

# simple script aiming to replicate the function
# of the "Exp_Recover_Frsn_Spiral_Good.m" matlab script
# for the "Basler_PhaseTarget2" data from Nadeem at USN
datadirpath = r"C:\Users\erlen\Documents\GitHub\USN-FPM\Basler_PhaseTarget2\Images"
image_extension = ".tiff"

wavelength = 0.520e-6
k0=2*np.pi/wavelength

arraysize=15
LED_gap = 4e-3 # 4 mm
z_LED = 83e-3 # distance from LED array to object
magnification = 4
upscaling = 6
pixel_size_detector = 2.4e-6 # 2.4 um
numerical_aperture = 0.1
object_to_lens_distance = 9.5e-3 # 9.5 mm
noise_threshold = 1800

pixel_offset_x = 0
pixel_offset_y = -750

radius_of_LED_circle = 10
center_LED_x = 7
center_LED_y = 7
low_res_image_size_x, low_res_image_size_y = 512, 512

possible_x_indices = np.arange(arraysize) - center_LED_x
possible_y_indices = np.arange(arraysize) - center_LED_y
mesh_x, mesh_y = np.meshgrid(possible_x_indices, possible_y_indices)

available_LEDs = mesh_x**2 + mesh_y**2 < radius_of_LED_circle**2
number_of_LEDs = np.sum(available_LEDs)

x_location_axis = possible_x_indices * LED_gap
y_location_axis = possible_y_indices * LED_gap
mesh_x_locations, mesh_y_locations = np.meshgrid(x_location_axis, y_location_axis)
kx_LED = -k0 * (mesh_x_locations/np.sqrt(mesh_x_locations**2+mesh_y_locations**2+z_LED**2))
ky_LED = -k0 * (mesh_y_locations/np.sqrt(mesh_x_locations**2+mesh_y_locations**2+z_LED**2))

pixel_size_object_raw = pixel_size_detector/magnification
pixel_size_object_recovered = pixel_size_object_raw/upscaling
lens_to_detector_distance = object_to_lens_distance*magnification
#lens_diameter = 2*np.tan(np.arcsin(numerical_aperture))*object_to_lens_distance
lens_diameter = 0.00195 # overwrite, aprox the same
cutoff_wavevector = numerical_aperture*k0

#### Image imports ####

print("Loading images")
number_of_images = arraysize**2
images = []
image_backgrounds = []
file_nr = 0
for Y in range(arraysize):
    for X in range(arraysize):
        if available_LEDs[Y,X]:
            file_nr += 1
        file = os.path.join(datadirpath, f"{file_nr}{image_extension}")
        image = np.array(Image.open(file))
        total_image_size_y, total_image_size_x = image.shape
        print(image.shape)
        image = image[total_image_size_y//2-low_res_image_size_y//2 -1+pixel_offset_y:\
                      total_image_size_y//2+low_res_image_size_y//2 -1+pixel_offset_y,\
                      total_image_size_x//2-low_res_image_size_x//2 -1+pixel_offset_x:\
                      total_image_size_x//2+low_res_image_size_x//2 -1+pixel_offset_x]

        background_mean_region_1 = np.mean(image[40-1:90,175-1:225])
        background_mean_region_2 = np.mean(image[465-1:495,455-1:490])
        image_background = np.mean([background_mean_region_1, background_mean_region_2])
        
        if image_background > noise_threshold:
            if len(image_backgrounds)==0:
                image_background = 0
            else:
                image_background = image_backgrounds[-1]
        image = image - image_background
        image[image<0] = 0
        images.append(np.sqrt(image))
        image_backgrounds.append(image_background)

print("Finished loading images")

#### Object plane #####
high_res_image_size_x = low_res_image_size_x * upscaling
high_res_image_size_y = low_res_image_size_y * upscaling

object_x_size = high_res_image_size_x * pixel_size_object_recovered
object_y_size = high_res_image_size_y * pixel_size_object_recovered

object_x_axis = (np.arange(high_res_image_size_x) - high_res_image_size_x/2) * pixel_size_object_recovered
object_y_axis = (np.arange(high_res_image_size_y) - high_res_image_size_y/2) * pixel_size_object_recovered

object_x_values, object_y_values = np.meshgrid(object_x_axis, object_y_axis)

offset_x = pixel_offset_x * pixel_size_object_raw
offset_y = pixel_offset_y * pixel_size_object_raw

#### Aperture frequency plane #####
dkx = 2*np.pi/(pixel_size_object_recovered*(high_res_image_size_x))
dky = 2*np.pi/(pixel_size_object_recovered*(high_res_image_size_y))
kmax = np.pi/pixel_size_object_raw

kx_axis = dkx * (np.arange(low_res_image_size_x) - low_res_image_size_x/2)
ky_axis = dky * (np.arange(low_res_image_size_y) - low_res_image_size_y/2)
kx_values, ky_values = np.meshgrid(kx_axis, ky_axis)
CTF = (kx_values**2+ky_values**2) <= cutoff_wavevector**2

high_res_kx_axis = dkx * (np.arange(high_res_image_size_x) - high_res_image_size_x/2)
high_res_ky_axis = dkx * (np.arange(high_res_image_size_y) - high_res_image_size_y/2)
high_res_kx_values, high_res_ky_values = np.meshgrid(high_res_kx_axis, high_res_ky_axis)
high_res_CTF = (high_res_kx_values**2 + high_res_ky_values**2) <= cutoff_wavevector**2

#### Aperture coordinate plane #####
lens_scaling = object_to_lens_distance/k0
Ldx = dkx*lens_scaling
Ldy = dkx*lens_scaling

high_res_lens_pupil = (high_res_kx_values**2 + high_res_ky_values**2) <= (lens_diameter/2/lens_scaling)**2
lens_pupil = (kx_values**2+ky_values**2) <= (lens_diameter/2/lens_scaling)**2

#### Object guess ####
quadratic_object_phase_term = np.exp(1j * (k0/(2*object_to_lens_distance)*(object_x_values**2+object_y_values**2)))

object_guess = zoom(input=images[112], zoom=upscaling) # NOT IDENTICAL AS MATLAB :(
object_guess = ifft2(ifftshift(fftshift(fft2(object_guess)) * high_res_CTF))
# object_spectrum_guess = fftshift(fft2(object_guess*quadratic_object_phase_term)) # NOT THIS APPARENTLY, WHY?
object_spectrum_guess = ifftshift(fft2(fftshift(object_guess*quadratic_object_phase_term)))


#### Shift ####
shift_x_mesh = ((mesh_x_locations-offset_x)/z_LED*object_to_lens_distance-offset_x)/Ldx
shift_y_mesh = ((mesh_y_locations-offset_y)/z_LED*object_to_lens_distance-offset_y)/Ldy


#### Linearize image info arrays ####
available = []

k_shifts = []

for Y in range(arraysize):
    for X in range(arraysize):
        kx_center = int(np.round(high_res_image_size_x/2+shift_x_mesh[Y,X]))
        ky_center = int(np.round(high_res_image_size_y/2+shift_y_mesh[Y,X]))
        kx_low = int(np.round(kx_center-low_res_image_size_x/2))
        kx_high = int(np.round(kx_center+low_res_image_size_x/2))
        ky_low = int(np.round(ky_center-low_res_image_size_y/2))
        ky_high = int(np.round(ky_center+low_res_image_size_y/2))
        k_shifts.append([kx_low, kx_high, ky_low, ky_high])
        available.append(available_LEDs[Y,X])



# from MATLAB for now
spiral_order = -1+np.array([113,128,127,112,97,98,99,114,129,144,143,142,141,126,111,96,81,82,83,84,85,100,115,130,145,160,159,158,157,156,155,140,125,110,95,80,65,66,67,68,69,70,71,86,101,116,131,146,161,176,175,174,173,172,171,170,169,154,139,124,109,94,79,64,49,50,51,52,53,54,55,56,57,72,87,102,117,132,147,162,177,192,191,190,189,188,187,186,185,184,183,168,153,138,123,108,93,78,63,48,33,34,35,36,37,38,39,40,41,42,43,58,73,88,103,118,133,148,163,178,193,208,207,206,205,204,203,202,201,200,199,198,197,182,167,152,137,122,107,92,77,62,47,32,17,18,19,20,21,22,23,24,25,26,27,28,29,44,59,74,89,104,119,134,149,164,179,194,209,224,223,222,221,220,219,218,217,216,215,214,213,212,211,196,181,166,151,136,121,106,91,76,61,46,31,16,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,30,45,60,75,90,105,120,135,150,165,180,195,210,225])

#### Spectrum mask #### What is this? Except for being a mask which removes unwanted frequencies
spectrum_mask = np.zeros((high_res_image_size_y, high_res_image_size_x), dtype=bool)
for LED_number in spiral_order:
    if not available[LED_number]:
        continue
    kx_low, kx_high, ky_low, ky_high = k_shifts[LED_number]
    
    spectrum_mask[ky_low:ky_high, kx_low:kx_high] = spectrum_mask[ky_low:ky_high, kx_low:kx_high]*(1-lens_pupil) + lens_pupil

#### Initialization
recovered_spectrum = object_spectrum_guess*spectrum_mask
recovered_pupil = lens_pupil.astype(np.complex128)

#### Main recovery loop ####
for loop in range(10):
    for LED_number in spiral_order:
        if not available[LED_number]:
            continue
        
        kx_low, kx_high, ky_low, ky_high = k_shifts[LED_number]
        scale = upscaling**2
        current_spectrum = recovered_spectrum[ky_low:ky_high,kx_low:kx_high].copy()    

        current_lens_spectrum = recovered_pupil * lens_pupil * current_spectrum
        projected_image = fftshift(ifft2(ifftshift(current_lens_spectrum)))
        raw_image = images[LED_number]
        updated_image = raw_image * np.exp(1j*np.angle(projected_image))
        
        
        updated_lens_spectrum=scale*ifftshift(fft2(fftshift(updated_image)))
        
        spectrum_update = np.abs(recovered_pupil) * np.conj(recovered_pupil) \
                          * (updated_lens_spectrum-current_lens_spectrum) \
                          / np.max(np.abs(recovered_pupil)) / (np.abs(recovered_pupil)**2 + 1.0)
        
        pupil_update = np.abs(current_spectrum) * np.conj(current_spectrum) \
                       * (updated_lens_spectrum-current_lens_spectrum) \
                       / np.max(np.abs(current_spectrum)) / (np.abs(current_spectrum)**2 + 1000)
        
        recovered_spectrum[ky_low:ky_high,kx_low:kx_high] += spectrum_update*lens_pupil
        recovered_pupil += pupil_update*lens_pupil

recovered_object = np.conj(quadratic_object_phase_term) * fftshift(ifft2(ifftshift(recovered_spectrum)))

recovered_object_FT=fftshift(fft2(recovered_object)) * spectrum_mask

plt.matshow(np.log(np.abs(recovered_object_FT)))
plt.matshow(np.abs(recovered_object))
plt.matshow(np.angle(recovered_object))
plt.matshow(np.abs(recovered_pupil))
plt.matshow(np.angle(recovered_pupil))
plt.show()