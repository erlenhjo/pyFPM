import numpy as np
from pyFPM.recovery.calibration.positional_calibration import calculate_shifts, simplified_non_linear_error_factory

def non_linear_regression_test_truth(m_vals, n_vals):
    delta_x = -1e-3
    delta_y = 1e-3
    z_LED = 204e-3
    rotation = 2
    patch_x = 0
    patch_y = 0
    frequency = 1923076.923076923
    df_x = 1201.923076923077
    df_y = 1201.923076923077
    LED_pitch = 6e-3

    return calculate_shifts(m_vals, n_vals, delta_x, delta_y, z_LED, rotation, patch_x, patch_y, frequency, df_x, df_y, LED_pitch)

def non_linear_regression_test_guess(m_vals, n_vals):
    delta_x = 0e-3
    delta_y = 0e-3
    z_LED = 200e-3
    rotation = 0
    patch_x = 0
    patch_y = 0
    frequency = 1923076.923076923
    df_x = 1201.923076923077
    df_y = 1201.923076923077
    LED_pitch = 6e-3

    return calculate_shifts(m_vals, n_vals, delta_x, delta_y, z_LED, rotation, patch_x, patch_y, frequency, df_x, df_y, LED_pitch)

def non_linear_regression_test_mn_vals():
    m_vals = np.empty(25)
    n_vals = np.empty(25)
    index=0
    for m in range(-2,3):
        for n in range(-2,3):
            m_vals[index] = m
            n_vals[index] = n
            index += 1

    return m_vals, n_vals

def non_linear_regression_test():
    delta_x = 0e-3
    delta_y = 0e-3
    z_LED = 200e-3
    rotation = 0
    patch_x = 0
    patch_y = 0
    frequency = 1923076.923076923
    df_x = 1201.923076923077
    df_y = 1201.923076923077
    LED_pitch = 6e-3

    m_vals, n_vals = non_linear_regression_test_mn_vals() 

    truth_x, truth_y = non_linear_regression_test_truth(m_vals, n_vals)
    guess_x, guess_y = non_linear_regression_test_guess(m_vals, n_vals)

    error_function = simplified_non_linear_error_factory(truth_x, truth_y, m_vals, n_vals, patch_x, patch_y, frequency, df_x, df_y, LED_pitch)

    from scipy.optimize import minimize

    results = minimize(error_function,x0=[delta_x, delta_y, z_LED, rotation])
    
    delta_x, delta_y, z_LED, rotation = results.x

    minimized_x, minimized_y = calculate_shifts(m_vals, n_vals, delta_x, delta_y, z_LED, rotation, patch_x, patch_y, frequency, df_x, df_y, LED_pitch)


    print(results)


    import matplotlib.pyplot as plt
    plt.scatter(truth_x, truth_y,marker="o",alpha=0.8)
    plt.scatter(guess_x, guess_y, marker="s",alpha=0.8)
    plt.scatter(minimized_x, minimized_y, marker="x",alpha=0.8)
    plt.show()


if __name__ == "__main__":
    non_linear_regression_test()
