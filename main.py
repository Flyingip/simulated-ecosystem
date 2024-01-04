from land import *
from landscape_test import *
import random as rd
from creature import *
from events import *
import os
import pygame

# 目录相关

current_file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file_path)
os.chdir(current_dir)

map_path = "maps/map 16-17-13.png"

# 视频相关

frame_number = 0

# 地图数据相关

h = 800
w = 800
land_img = image.load(map_path)

river = []  # 水源地块
landscape = [[[] * 4] * h] * w
Land_map = [[Land(0) for _ in range(h)] for _ in range(w)]
landscape_index = np.zeros((h, w))
water_index = np.zeros((h, w))
resc_prodc = np.zeros((h, w))

# pygame界面与可视化相关

display.set_caption("simulated-ecosystem")

game_display = display.set_mode((h, w))  # 主画面
game_display.blit(land_img, (0, 0))

transparent_surface = pygame.Surface((h, w), pygame.SRCALPHA)  # 透明画面，用于实现感知圈
transparent_surface.fill((0, 0, 0, 0))

# 根据pygame界面授予地图数据

for i in range(0, h):
    for j in range(0, w):
        landscape[i][j] = game_display.get_at((i, j))  # 获取像素点颜色
        Land_map[i][j] = Land(land_comp(landscape[i][j]))  # **创建索引 建立Land对象**
        landscape_index[i][j] = Land_map[i][j].index  # 获取索引用于画图
        water_index[i][j] = Land_map[i][j].orig_soil_H2O  # 地块含水量的二维地图
        resc_prodc[i][j] = Land_map[i][j].orig_plant_C  # 地块植物碳的二维地图
        if Land_map[i][j].index == 0:
            river.append([i, j])
# land_plot(landscape_index)
# water_plot(water_index)

# 生成生物

rabbit = []
wolf = []
rabbit, wolf = spwan(rabbit, wolf, river)

# 程序运行主循环

crashed = False
while not crashed:
    pygame.display.flip()

    # environment_chage(Land_map)

    # 渲染与刷新可视化界面

    game_display.blit(land_img, (0, 0))
    transparent_surface.fill((0, 0, 0, 0))

    # 生物行为逻辑

    for creature in wolf:
        Land_map = neuron(creature, Land_map, river)
    for creature in rabbit:
        Land_map = neuron(creature, Land_map, river)

    # 可视化生物

    # draw_plant(game_display, resc_prodc)
    print_creatures(rabbit, wolf, game_display, transparent_surface)
    game_display.blit(transparent_surface, (0, 0))

    # 绘制图表

    plot_stats(rabbit, wolf)

    pygame.image.save(game_display, f"snapshots/frame_{frame_number}.jpg")
    frame_number += 1

pygame.quit()
