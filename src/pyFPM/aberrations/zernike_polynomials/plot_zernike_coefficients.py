import matplotlib.pyplot as plt
import numpy as np

def plot_zernike_coefficients(ax: plt.Axes, zernike_coefficients: np.ndarray):
    mode_number = np.arange(len(zernike_coefficients)).astype(int)[1:]

    max_deviation = np.max(np.abs(zernike_coefficients))
    y_max = max(max_deviation, 1) + 0.5

    positive_values = zernike_coefficients[1:].copy()
    positive_values[positive_values < 0] = 0
    negative_values = zernike_coefficients[1:].copy()
    negative_values[negative_values > 0] = 0

    color = "b"
    ax.bar(mode_number, positive_values, width=0.9, color=color)
    ax.bar(mode_number, negative_values, width=0.9, color=color)
    ax.grid(visible=True, which="major", axis="y")
    ax.set_axisbelow(True)
    ax.set_ylim([-y_max, y_max])
    ax.set_title("Zernike coefficients")
    ax.set_ylabel("Amplitude")
    ax.set_xlabel("Mode number")
    


def main():
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    plot_zernike_coefficients(ax, np.array([0,0.1,1,4,-4,3,-2,4,-6, 0.5,-0.3,0.1]))
    plt.show()

if __name__ == "__main__":
    main()