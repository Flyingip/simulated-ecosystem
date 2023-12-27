from land import *
from landscape_test import *
import pygame
import random as rd
from creature import *
from events import *

init()


FPS = 5  # 帧率
clock = time.Clock()  # 时钟对象
clock.tick(FPS)

# 地图的大小

h = 800
w = 800

# 地图

game_display = display.set_mode((h, w))
display.set_caption("simulated-ecosystem")
land_img = image.load("Land_v1_1.png")

# 地图数据 初始化
river = []  # 水源地块
landscape = [[[] * 4] * 800] * 800
Land_map = [[Land(0) for _ in range(800)] for _ in range(800)]
landscape_index = np.zeros((800, 800))
water_index = np.zeros((800, 800))
resc_prodc = np.zeros((800, 800))
# river = []  # 水源地块
for i in range(0, 800):
    for j in range(0, 800):
        landscape[i][j] = game_display.get_at((j, i))  # 获取像素点颜色
        Land_map[i][j] = Land(land_comp(landscape[i][j]))  # **创建索引 建立Land对象**
        landscape_index[i][j] = Land_map[i][j].index  # 获取索引用于画图
        water_index[i][j] = Land_map[i][j].orig_soil_H2O  # 地块含水量的二维地图
        resc_prodc[i][j] = Land_map[i][j].orig_plant_C  # 地块植物碳的二维地图
        if Land_map[i][j].index == 0:
            river.append([i, j])
# land_plot(landscape_index)  # plot land
# water_plot(water_index)
# print(river)
# 调试用食草动物对象

# init_world()

crashed = False

number_of_days = 10000

# plt.figure()
# plt.ion()


# world
for day in range(number_of_days):
    while not crashed:
        for i in event.get():
            if i.type == KEYDOWN:
                if i.unicode == "q":
                    crashed = True
        if crashed:
            exit()

        pygame.display.flip()
        clock.tick(60)
        # environment_chage(Land_map)
        game_display.blit(land_img, (0, 0))

        for creature in wolf:
            neuron(creature, Land_map, river)
        for creature in rabbit:
            neuron(creature, Land_map, river)

        # life()
        # game_display.fill((255, 255, 255))
        print_creatures(game_display)
        print(len(rabbit))

# plt.ioff()
pygame.quit()
