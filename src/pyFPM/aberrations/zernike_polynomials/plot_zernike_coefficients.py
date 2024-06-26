import matplotlib.pyplot as plt
import numpy as np
from typing import List


def plot_zernike_coefficients(ax: plt.Axes, zernike_coefficients: np.ndarray, title = "Zernike coefficients"):
    mode_number = np.arange(len(zernike_coefficients)).astype(int)[2:]

    max_deviation = np.max(np.abs(zernike_coefficients[2:]))
    y_max = max_deviation * 1.2

    positive_values = zernike_coefficients[2:].copy()
    positive_values[positive_values < 0] = 0
    negative_values = zernike_coefficients[2:].copy()
    negative_values[negative_values > 0] = 0

    color = "b"
    ax.bar(mode_number, positive_values, width=0.9, color=color)
    ax.bar(mode_number, negative_values, width=0.9, color=color)
    ax.grid(visible=True, which="major", axis="y")
    ax.set_axisbelow(True)
    ax.set_ylim([-y_max, y_max])
    ax.set_ylabel("Amplitude")
    ax.set_xlabel("Mode number")

    if title is not None:
        ax.set_title(title)

def plot_zernike_coefficients_comparative(ax: plt.Axes, zernike_coefficients_list: List[np.ndarray], colors, labels):
    width = 0.9/len(zernike_coefficients_list)
    for n, (coefficients, color, label) in enumerate(zip(zernike_coefficients_list, colors, labels)):
        mode_number = np.arange(len(coefficients)).astype(int)[2:]

        max_deviation = np.max(np.abs(coefficients[2:]))
        y_max = max_deviation * 1.2

        positive_values = coefficients[2:].copy()
        positive_values[positive_values < 0] = 0
        negative_values = coefficients[2:].copy()
        negative_values[negative_values > 0] = 0

        ax.bar(mode_number+(n-1/2)*width, positive_values, width=width, color=color, label=label)
        ax.bar(mode_number+(n-1/2)*width, negative_values, width=width, color=color)
        ax.grid(visible=True, which="major", axis="y")
        ax.set_axisbelow(True)
        ax.set_ylim([-y_max, y_max])
        ax.set_ylabel("Amplitude")
        ax.set_xlabel("Mode number")
        ax.set_xticks(np.arange(0, max(mode_number)+1, 4))
    
    ax.legend(loc="lower right")




def main():
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    plot_zernike_coefficients(ax, np.array([0,0.1,1,4,-4,3,-2,4,-6, 0.5,-0.3,0.1]))
    plt.show()

if __name__ == "__main__":
    main()