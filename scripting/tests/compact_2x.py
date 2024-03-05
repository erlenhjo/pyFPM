focal_length = 60.18e-3
magnification = 2
working_distance = 92e-3
total_length = 280e-3
objective_size = 18e-3
objective_to_detector = 170e-3



z_1 = focal_length*(1+1/magnification)
z_2 = z_1*magnification

print(z_1,z_2)



