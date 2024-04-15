import numpy as np
import matplotlib.pyplot as plt



def all_three_rotations(roll, yaw, pitch):
    yaw, pitch, roll = yaw * np.pi/180, pitch * np.pi/180, roll * np.pi/180

    a, b, c = roll, yaw, pitch

    x = np.arange(-2,3)
    y = np.arange(-2,3)
    xx, yy = np.meshgrid(x,y)
    xyz = np.array([xx.flatten(), yy.flatten(), np.zeros(shape=xx.shape).flatten()])






    rotated_points = get_Rzyx(a,b,c) @ xyz
    rotated_points_2 = get_Rz(a) @ get_Ry(b) @ get_Rx(c) @ xyz

    print(rotated_points-rotated_points_2)

    fig = plt.figure()
    ax: plt.Axes = fig.add_subplot(projection= "3d")
    ax.scatter(xyz[0], xyz[1], xyz[2], c="r")
    ax.scatter(rotated_points[0], rotated_points[1], rotated_points[2], c="b")



def get_Rx(angle):
    return np.array([
        [
            1,
            0,
            0
        ],
        [
            0,
            np.cos(angle),
            -np.sin(angle)
        ],
        [
            0,
            np.sin(angle),
            np.cos(angle)
        ]
    ])

def get_Ry(angle):
    return np.array([
        [
            np.cos(angle),
            0,
            np.sin(angle)
        ],
        [
            0,
            1,
            0
        ],
        [
            -np.sin(angle),
            0,
            np.cos(angle)
        ]
    ])

def get_Rz(angle):
    return np.array([
        [
            np.cos(angle),
            -np.sin(angle),
            0
        ],
        [
            np.sin(angle),
            np.cos(angle),
            0
        ],
        [
            0,
            0,
            1
        ]
    ])


def get_Rzyx(a, b, c):
    r_xx = np.cos(a)*np.cos(b)
    r_xy = np.cos(a)*np.sin(b)*np.sin(c) - np.sin(a)*np.cos(c)
    r_xz = np.cos(a)*np.sin(b)*np.cos(c) + np.sin(a)*np.sin(c)

    r_yx = np.sin(a)*np.cos(b)
    r_yy = np.sin(a)*np.sin(b)*np.sin(c) + np.cos(a)*np.cos(c)
    r_yz = np.sin(a)*np.sin(b)*np.cos(c) - np.cos(a)*np.sin(c)

    r_zx = -np.sin(b)
    r_zy = np.cos(b)*np.sin(c)
    r_zz = np.cos(b)*np.cos(c)

    return np.array([
        [
            r_xx,
            r_xy,
            r_xz
        ],
        [
            r_yx,
            r_yy,
            r_yz
        ],
        [
            r_zx,
            r_zy,
            r_zz
        ]
    ])



if __name__ == "__main__":
    all_three_rotations(roll=3, yaw=0, pitch=0)
    all_three_rotations(roll=0, yaw=3, pitch=0)
    all_three_rotations(roll=0, yaw=0, pitch=3)

    plt.show()



  

