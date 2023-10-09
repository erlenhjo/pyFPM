import numpy as np


def calculate_k_vector_range(k_x, k_y, dk_x, dk_y, 
                             size_low_res_x, size_low_res_y, size_high_res_x, size_high_res_y,
                             LED_indices, index 
                            ):
    LED_index_x = LED_indices[index][0]
    LED_index_y = LED_indices[index][1]

    # calculate which wavevector-values are present in the current low res image
    k_center_x = np.round((size_high_res_x - 1)/2 - k_x[LED_index_y, LED_index_x]/dk_x)
    k_center_y = np.round((size_high_res_y - 1)/2 - k_y[LED_index_y, LED_index_x]/dk_y)
    k_min_x = int(np.floor(k_center_x - (size_low_res_x - 1) / 2))
    k_max_x = int(np.floor(k_center_x + (size_low_res_x - 1) / 2))
    k_min_y = int(np.floor(k_center_y - (size_low_res_y - 1) / 2))
    k_max_y = int(np.floor(k_center_y + (size_low_res_y - 1) / 2))

    return k_min_x, k_max_x, k_min_y, k_max_y


def calculate_recovered_CTF(update_order, LED_indices, k_x, k_y, dk_x, dk_y, size_low_res_x, size_low_res_y, size_high_res_x, size_high_res_y, low_res_CTF):
    low_res_CTF = low_res_CTF.astype(bool)
    recovered_CTF = np.zeros(shape=(size_high_res_y, size_high_res_x), dtype=bool)

    for index in update_order:
        k_min_x, k_max_x, k_min_y, k_max_y = calculate_k_vector_range(k_x, k_y, dk_x, dk_y, size_low_res_x, size_low_res_y,
                                                                        size_high_res_x, size_high_res_y, LED_indices, index)

        recovered_CTF[k_min_y:k_max_y+1, k_min_x:k_max_x+1] += low_res_CTF
                                            
    return recovered_CTF
