import numpy as np
from opensimplex import OpenSimplex
import random
from PIL import Image
from datetime import datetime
import os

current_file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file_path)
os.chdir(current_dir)

# 地图尺寸和地块大小
x, y = 800, 800
control = 2

map_data = np.zeros((x, y, control))


def berlin(data, scale):
    seed = random.randint(0, 1000)
    noise_gen = OpenSimplex(seed)
    for i in range(x):
        for j in range(y):
            n = noise_gen.noise2(i / scale, j / scale)
            data[i, j] = abs(n)
    image = Image.fromarray(
        np.uint8((data - np.min(data)) / (np.max(data) - np.min(data)) * 255), "L"
    )
    image_file_path = f"maps/berlin {datetime.now().strftime('%H-%M-%S')}.png"
    image.save(image_file_path)
    return data


def generate_landscape(noise1, noise2, river, ground, hill, peak):
    index = np.zeros((x, y))
    besideriver = 4 * river
    for i in range(x):
        for j in range(y):
            if noise1[i, j] <= river:
                index[i, j] = 0
            elif noise1[i, j] > river and noise1[i, j] <= besideriver:
                index[i, j] = 1
            elif noise1[i, j] > ground and noise1[i, j] <= hill:
                index[i, j] = 3
            elif noise1[i, j] > hill and noise1[i, j] <= peak:
                index[i, j] = 4
            elif noise1[i, j] > peak and noise2[i, j] < 0.3:
                index[i, j] = 4
            elif noise1[i, j] > peak:
                index[i, j] = 5
            else:
                index[i, j] = 2
    return index


def land_plot(landscape_index):
    color_map = np.zeros((x, y, 4), dtype=np.uint8)
    colors = [
        (1, 173, 255, 255),
        (36, 255, 1, 255),
        (24, 173, 1, 255),
        (12, 86, 1, 255),
        (231, 255, 1, 255),
        (120, 132, 1, 255),
    ]
    for i in range(0, x):
        for j in range(0, y):
            color_map[i, j, :] = colors[int(landscape_index[i, j])]
    return color_map


noise1 = map_data[:, :, 0]
height = berlin(noise1, 200)

noise2 = map_data[:, :, 1]
noise2 = berlin(noise2, 400)

index = generate_landscape(noise1, noise2, 0.05, 0.4, 0.6, 0.7)
# index[:] = 3
map = land_plot(index)

image = Image.fromarray(map)

# Save the image
image_file_path = f"maps/map {datetime.now().strftime('%H-%M-%S')}.png"
image.save(image_file_path)
