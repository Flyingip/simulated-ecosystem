from land import *
from landscape_test import *
import pygame
import random as rd
from creature_repo import *
from events import *

# init()

FPS = 10  # 帧率
clock = time.Clock()  # 时钟对象
clock.tick(FPS)

# 地图的大小

h = 800
w = 800

# 地图

game_display = display.set_mode((h, w))
display.set_caption("simulated-ecosystem")
land_img = image.load("Land_v1_1.png")
game_display.blit(land_img, (0, 0))

# 地图数据 初始化
for i in range(0, 800):
    for j in range(0, 800):
        landscape[i][j] = game_display.get_at((j, i))  # 获取像素点颜色
        Land_map[i][j] = Land(land_comp(landscape[i][j]))  # **创建索引 建立Land对象**
        landscape_index[i][j] = Land_map[i][j].index  # 获取索引用于画图
        water_index[i][j] = Land_map[i][j].orig_soil_H2O  # 地块含水量的二维地图
        resc_prodc[i][j] = Land_map[i][j].orig_plant_C  # 地块植物碳的二维地图


# land_plot(landscape_index)  # plot land
# water_plot(water_index)

# 生物


# 调试用食草动物对象


crashed = False

number_of_days = 10

# plt.figure()
# plt.ion()


# world
for day in range(number_of_days):
    # while not crashed:
    #     for i in event.get():
    #         if i.type == KEYDOWN:
    #             if i.unicode == "q":
    #                 crashed = True
    #         if crashed:
    #             exit()

    pygame.display.flip()

    environment_chage()
    life()
    print_creatures(game_display)

    clock.tick(60)

# plt.ioff()
pygame.quit()
