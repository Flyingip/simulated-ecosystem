from land import *
from landscape_test import *
import random as rd
from creature import *
from events import *
import os
import pygame

# 改变目录
current_file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file_path)
os.chdir(current_dir)

FPS = 20  # 帧率
clock = pygame.time.Clock()  # 时钟对象
clock.tick(FPS)

# 地图的大小
h = 800
w = 800

# 地图
game_display = display.set_mode((h, w))
display.set_caption("simulated-ecosystem")
land_img = image.load("maps/map 16-17-13.png")
# land_img = image.load("Land_v1_1.png")

transparent_surface = pygame.Surface((800, 800), pygame.SRCALPHA)
transparent_surface.fill((0, 0, 0, 0))  # 填充完全透明的颜色


# 地图数据 初始化
river = []  # 水源地块
landscape = [[[] * 4] * 800] * 800
Land_map = [[Land(0) for _ in range(800)] for _ in range(800)]
landscape_index = np.zeros((800, 800))
water_index = np.zeros((800, 800))
resc_prodc = np.zeros((800, 800))

game_display.blit(land_img, (0, 0))

for i in range(0, 800):
    for j in range(0, 800):
        landscape[i][j] = game_display.get_at((i, j))  # 获取像素点颜色
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


def draw_plant(gameDisplay, resc_prodc):
    for i in range(h):
        for j in range(w):
            if resc_prodc[i][j] != 0:
                draw.circle(gameDisplay, (0, 0, 0), (i, j), 0.5 * resc_prodc[i][j])


# plt.figure()
# plt.ion()

spwan(river)
pre_num = []
pra_num = []
daylist = []
ave_rab_sig = []
# world
crashed = False
while not crashed:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.unicode == "q":
                crashed = True
    if crashed:
        exit()

    pygame.display.flip()

    # environment_chage(Land_map)

    game_display.blit(land_img, (0, 0))

    # 将透明表面绘制到主显示表面上
    transparent_surface.fill((0, 0, 0, 0))  # 填充完全透明的颜色

    for creature in wolf:
        Land_map = neuron(creature, Land_map, river)
    for creature in rabbit:
        Land_map = neuron(creature, Land_map, river)

    draw_plant(game_display, resc_prodc)
    print_creatures(game_display, transparent_surface)
    game_display.blit(transparent_surface, (0, 0))
    # print(len(river))

    pre_num.append(len(rabbit))
    pra_num.append(len(wolf))

    average = []
    for r in rabbit:
        average.append(r.visibility)

    if len(rabbit) != 0:
        ave_rab_sig.append(sum(average) / len(rabbit))
    else:
        ave_rab_sig = 0
    plot_stats(pre_num, pra_num, ave_rab_sig)

    clock.tick(FPS)

pygame.quit()
