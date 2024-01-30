import matplotlib.pyplot as plt

from recover_compact import recover_compact



def compact():
    patch_start = [896, 896] # [x, y]
    patch_size = [512, 512] # [x, y]
    defocus_guess = 0
    max_array_size = 9
    title = "Compact"
    datadirpath = ""
    fig = recover_compact(title=title)






if __name__ == "__main__":
    #compact()
    telecentric()
    plt.show()
