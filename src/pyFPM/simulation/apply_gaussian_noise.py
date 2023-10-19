import numpy as np

def apply_gaussian_noise(low_res_images, noise_fraction, relative_NAs, LED_indices):

    darkfield_mean = _calculate_darkfield_mean(low_res_images=low_res_images,
                                                LED_indices=LED_indices,
                                                relative_NAs=relative_NAs)
    
    noise_level = noise_fraction * darkfield_mean
    original = low_res_images.copy()
    image_shape = low_res_images[0].shape
    
    for image_nr in range(len(low_res_images)):
        low_res_images[image_nr] += gaussian_noise(mean = noise_level,
                                                   variance = noise_level,
                                                   image_shape = image_shape)
        
    noise_mean = _calculate_darkfield_mean(low_res_images=low_res_images,
                                                LED_indices=LED_indices,
                                                relative_NAs=relative_NAs)
        
    return low_res_images


def _calculate_darkfield_mean(low_res_images, LED_indices, relative_NAs):
    darkfield_means = []

    for image_nr in range(len(low_res_images)):
        LED_index_x = LED_indices[image_nr][0]
        LED_index_y = LED_indices[image_nr][1]

        low_res_image = low_res_images[image_nr]
        relative_NA = relative_NAs[LED_index_y, LED_index_x]

        if relative_NA > 1.05:
            darkfield_means.append(np.mean(low_res_image))

    darkfield_mean = np.mean(np.array(darkfield_means))

    return darkfield_mean


def gaussian_noise(mean, variance, image_shape):
    return np.random.default_rng().normal(mean, variance, size=image_shape)