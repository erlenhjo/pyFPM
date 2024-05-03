from pyFPM.NTNU_specific.components import COMPACT_2X

focal_length = COMPACT_2X.focal_length
magnification = COMPACT_2X.magnification
working_distance = COMPACT_2X.working_distance
total_length = 280e-3
objective_size = 18e-3
objective_to_detector = 170e-3

z_1 = focal_length*(1+1/magnification)
z_2 = focal_length*(1+magnification)

print(z_1,z_2, z_1+z_2+objective_size)

