import pygame
import numpy as np
from opensimplex import OpenSimplex
import random
from PIL import Image
import matplotlib.pyplot as plt
from datetime import datetime

# 地图尺寸和地块大小
x, y = 800, 800
control = 2
tile_size = 1  # 每个地块的像素大小

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
    image_file_path = f"berlin图 {datetime.now().strftime('%H-%M-%S')}.png"
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
    color_map = np.zeros((800, 800, 4), dtype=np.uint8)
    colors = [
        (1, 173, 255, 255),
        (36, 255, 1, 255),
        (24, 173, 1, 255),
        (12, 86, 1, 255),
        (231, 255, 1, 255),
        (120, 132, 1, 255),
    ]
    for i in range(0, 800):
        for j in range(0, 800):
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
image_file_path = f"地图 {datetime.now().strftime('%H-%M-%S')}.png"
image.save(image_file_path)

# 初始化pygame
# pygame.init()
# 创建窗口
# window = pygame.display.set_mode((width, height))
# pygame.display.set_caption("Noise Map")


# # 游戏主循环
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     # 绘制地图
#     for x in range(width):
#         for y in range(height):
#             pygame.draw.rect(
#                 window,
#                 (map_data[x, y], map_data[x, y], map_data[x, y]),
#                 (x * tile_size, y * tile_size, tile_size, tile_size),
#             )

#     pygame.display.flip()

# pygame.quit()
