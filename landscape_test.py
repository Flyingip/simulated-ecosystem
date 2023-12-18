from pygame import *
from land import *
import matplotlib.pyplot as plt

def land_comp(rgb):
    r = [(1, 173, 255, 255),
         (24, 173, 1, 255),
         (36, 255, 1, 255),
         (12, 86, 1, 255),
         (231, 255, 1, 255),
         (120, 132, 1, 255)]
    if rgb == (1, 173, 255, 255):
        type = 0
    elif rgb == (24, 173, 1, 255):
        type = 1
    elif rgb == (36, 255, 1, 255):
        type = 2
    elif rgb == (12, 86, 1, 255):
        type = 3
    elif rgb == (231, 255, 1, 255):
        type = 4
    elif rgb == (120, 132, 1, 255):
        type = 5
    else:
        err = [0, 0, 0, 0, 0, 0]
        for i in range(6):
            for j in range(2):
                err[i] = (rgb[j] - r[i][j]) ** 2 + err[i]
        min_err = min(err)
        type = err.index(min_err)
    return type

def land_plot(landscape_index):
    color_map = np.zeros((800, 800, 4), dtype=np.uint8)
    colors = [(1, 173, 255, 255),
              (24, 173, 1, 255),
              (36, 255, 1, 255),
              (12, 86, 1, 255),
              (231, 255, 1, 255),
              (120, 132, 1, 255)]
    for i in range(0, 800):
        for j in range(0, 800):
            color_map[i, j, :] = colors[int(landscape_index[j, i])]
    plt.imshow(color_map)
    plt.axis('off')
    plt.show()

def water_plot(landscape_index):
    color_map = np.zeros((800, 800, 4), dtype=np.uint8)
    colors = [(1, 173, 255, 255),
              (24, 173, 1, 255),
              (36, 255, 1, 255),
              (12, 86, 1, 255),
              (231, 255, 1, 255),
              (120, 132, 1, 255)]
    for i in range(0, 800):
        for j in range(0, 800):
            color_map[i, j, :] = colors[int(landscape_index[j, i])]
    plt.imshow(color_map)
    plt.axis('off')
    plt.show()
