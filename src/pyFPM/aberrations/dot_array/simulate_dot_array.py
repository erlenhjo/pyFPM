from pyFPM.aberrations.dot_array.Dot_array import get_dot_array_image, Dot_array

def simulate_dot_array(dot_array: Dot_array, image_size, pixel_size, magnification, rotation=0):
    dot_radius = dot_array.diameter / 2 # m
    dot_spacing = dot_array.spacing # m

    dot_array_image, dot_blobs = get_dot_array_image(
                                        dot_radius=dot_radius, 
                                        dot_spacing=dot_spacing, 
                                        image_size=image_size,
                                        object_pixel_size=pixel_size/magnification,
                                        rotation = rotation
                                        )

    return dot_array_image, dot_blobs