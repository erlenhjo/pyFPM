import numpy as np


def calculate_low_res_index_range(shifts_x, shifts_y, size_low_res_x, size_low_res_y, 
                                  size_high_res_x, size_high_res_y, LED_indices, index 
                                ):
    LED_index_x = LED_indices[index][0]
    LED_index_y = LED_indices[index][1]
    
    shift_x = shifts_x[LED_index_y, LED_index_x]
    shift_y = shifts_y[LED_index_y, LED_index_x]

    # calculate which wavevector-values are present in the current low res image
    center_x = (size_high_res_x - 1)/2 + shift_x
    center_y = (size_high_res_y - 1)/2 + shift_y
    min_x = int(np.round(center_x - (size_low_res_x - 1) / 2))
    max_x = int(np.round(center_x + (size_low_res_x - 1) / 2))
    min_y = int(np.round(center_y - (size_low_res_y - 1) / 2))
    max_y = int(np.round(center_y + (size_low_res_y - 1) / 2))

    return min_x, max_x, min_y, max_y


def calculate_recovered_CTF(update_order, LED_indices, shifts_x, shifts_y, size_low_res_x, size_low_res_y, size_high_res_x, size_high_res_y, low_res_CTF):
    low_res_CTF = low_res_CTF.astype(bool)
    recovered_CTF = np.zeros(shape=(size_high_res_y, size_high_res_x), dtype=bool)

    for index in update_order:
        min_x, max_x, min_y, max_y = calculate_low_res_index_range(shifts_x, shifts_y, size_low_res_x, size_low_res_y,
                                                                        size_high_res_x, size_high_res_y, LED_indices, index)

        recovered_CTF[min_y:max_y+1, min_x:max_x+1] += low_res_CTF
                                            
    return recovered_CTF
