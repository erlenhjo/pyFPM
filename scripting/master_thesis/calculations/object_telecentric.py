focal_length = 58.51e-3
magnification = 3
working_distance = 77e-3
total_length = 280e-3
objective_size = 33e-3
objective_to_detector = 170e-3

z_2=magnification*focal_length

print(z_2)

z_1 = focal_length + focal_length**2/z_2

print(z_1)

print(z_1+z_2+focal_length)

print(focal_length*(1+1/magnification))