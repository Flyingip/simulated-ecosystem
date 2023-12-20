import pygame
import numpy as np
from opensimplex import OpenSimplex
import random

# 初始化pygame
pygame.init()

# 地图尺寸和地块大小
width, height = 800, 800
tile_size = 1  # 每个地块的像素大小

# 创建窗口
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Noise Map")

# 生成地图数据
scale = 100
octaves = 3
# thresholds = [0.2, 0.4, 0.6, 0.8]

seed = random.randint(0, 1000)
noise_gen = OpenSimplex(seed)

map_data = np.zeros((width, height))

for x in range(width):
    for y in range(height):
        n = noise_gen.noise2(x / scale, y / scale)
        map_data[x, y] = abs(n) * 100
        # for i, t in enumerate(thresholds):
        #     if n < t:
        #         map_data[x, y] = i
        #         break
        # else:
        #     map_data[x, y] = len(thresholds)

# 地块颜色
colors = [
    (255, 255, 255),  # 白色
    (0, 255, 0),  # 绿色
    (0, 0, 255),  # 蓝色
    (255, 0, 0),  # 红色
    (0, 0, 0),  # 黑色
]

# 游戏主循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 绘制地图
    for x in range(width):
        for y in range(height):
            pygame.draw.rect(
                window,
                (map_data[x, y], map_data[x, y], map_data[x, y]),
                (x * tile_size, y * tile_size, tile_size, tile_size),
            )

    pygame.display.flip()

pygame.quit()
