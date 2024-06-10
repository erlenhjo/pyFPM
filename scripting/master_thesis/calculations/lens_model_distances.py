import numpy as np
import matplotlib.pyplot as plt

from pyFPM.NTNU_specific.components import TELECENTRIC_3X, COMPACT_2X_CALIBRATED

C_mount_extension_length_contribution = 17.5e-3
tube_length = 152.5e-3
extension_length = C_mount_extension_length_contribution + tube_length
total_length = 280e-3

def non_telecentric_distances(f_L, K):
    z_1 = f_L * (1+1/K)
    z_2 = f_L * (1+K)
    return z_1, z_2

def effective_object_to_aperture_distance(z_1, a_1):
    return (1/z_1 - a_1/z_1**2)**(-1)

def aperture_distance(z_1, z_q):
    return z_1 * (1 - z_1/z_q)

def telecentric_distances(f_L, K):
    z_1 = f_L * (1+1/K)
    z_2 = f_L * K
    return z_1, z_2

def compact_2X_calibrated():
    objective_size = 18e-3
    lens = COMPACT_2X_CALIBRATED
    focal_length = lens.focal_length
    magnification = lens.magnification
    calibrated_z_q = lens.effective_object_to_aperture_distance 
    working_distance = lens.working_distance
    
    z_1, z_2 = non_telecentric_distances(f_L=focal_length, K=magnification)
    a_1 = aperture_distance(z_1=z_1, z_q=calibrated_z_q)

    print("Compact 2X")
    print(f"z_1: {1000*z_1:.1f} mm")
    print(f"z_2: {1000*z_2:.1f} mm")
    print(f"WD: {1000*working_distance:.1f} mm")
    print(f"a_1: {1000*a_1:.1f} mm")
    print(f"objective_size: {1000*objective_size:.1f} mm")





def telecentric_3X():
    objective_size = 33e-3
    lens = TELECENTRIC_3X
    focal_length = lens.focal_length
    magnification = lens.magnification
    calibrated_z_q = lens.effective_object_to_aperture_distance 
    working_distance = lens.working_distance
        
    z_1, z_2 = telecentric_distances(f_L=focal_length, K=magnification)
    z_1_non_tele, z_2_non_tele = non_telecentric_distances(f_L=focal_length, K=magnification)

    print("Telecentric 3X")
    print(f"z_1: {1000*z_1:.1f} mm")
    print(f"z_2: {1000*z_2:.1f} mm")
    print(f"z_1 (non-tele): {1000*z_1_non_tele:.1f} mm")
    print(f"z_2 (non-tele): {1000*z_2_non_tele:.1f} mm")
    print(f"WD: {1000*working_distance:.1f} mm")
    print(f"a_1: {1000*focal_length:.1f} mm")
    print(f"objective_size: {1000*objective_size:.1f} mm")






if __name__=="__main__":
    compact_2X_calibrated()
    telecentric_3X()



