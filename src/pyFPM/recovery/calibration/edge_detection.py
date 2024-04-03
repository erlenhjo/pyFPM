import numpy as np
from skimage.feature import canny
from skimage.filters import threshold_otsu
from numba.typed import List
import matplotlib.pyplot as plt


def detect_edges_per_image(images, canny_sigma, LED_indices, center_indices, 
                           downsample_image: int = 1, downsample_edges: int = 1):
    n_values = []
    m_values = []
    edges_per_image = List()

    images = images[:,::downsample_image, ::downsample_image]

    image_center = np.flip(images[0].shape) // 2
    threshold = threshold_otsu(images) # global threshold appears best, less outliers, slight difference
    #threshold = 4e9
    #threshold = 0.5

    for image, image_indices in zip(images, np.array(LED_indices)):
        binary = (image <= threshold)
        edge_image = canny(binary, sigma=canny_sigma)
        #edge_image = canny(image=image, sigma=canny_sigma) # finds many other edges and not the desired 
        edge_points = np.flip(np.transpose(edge_image.nonzero()), axis=1) # points as an array of (x,y)

        # fig, axes = plt.subplots()
        # axes.matshow(image)
        # axes.scatter(edge_points[:,0], edge_points[:,1], color="orange")
        # plt.show()
        
        if edge_points.shape[0]==0:
            continue
        edge_points = edge_points[np.where(edge_points[:,0]>3)]
        edge_points = edge_points[np.where(edge_points[:,1]>3)]
        edge_points = edge_points[np.where(edge_points[:,0]<image.shape[1]-4)]
        edge_points = edge_points[np.where(edge_points[:,1]<image.shape[0]-4)]

        # fig, axes = plt.subplots()
        # axes.matshow(image)
        # axes.scatter(edge_points[:,0], edge_points[:,1], color="orange")
        # plt.show()


        n, m = image_indices - center_indices

        n_values.append(n)
        m_values.append(m)
        edges_per_image.append(((edge_points-image_center)*downsample_image)[::downsample_edges,:])

    

    return edges_per_image, np.array(n_values), np.array(m_values)