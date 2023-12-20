from land import *
from landscape_test import *
import pygame
import random as rd

# init()

FPS = 10  # 帧率
clock = time.Clock()  # 时钟对象
clock.tick(FPS)

# 地图的大小

h=800
w=800

#地图

game_display=display.set_mode((h,w))
display.set_caption("simulated-ecosystem")
land_img = image.load("Land_v1_1.png")
game_display.blit(land_img, (0, 0))

# 地图数据 初始化

landscape = [[[] * 4] * 800] * 800
Land_map = [[Land(0) for _ in range(800)] for _ in range(800)]
landscape_index = np.zeros((800, 800))
water_index = np.zeros((800, 800))
for i in range(0, 800):
    for j in range(0, 800):
        landscape[i][j] = game_display.get_at((j, i))  # 获取像素点颜色
        Land_map[i][j] = Land(land_comp(landscape[i][j]))  # **创建索引 建立Land对象**
        landscape_index[i][j] = Land_map[i][j].index  # 获取索引用于画图
        water_index[i][j] = Land_map[i][j].orig_soil_H2O
#land_plot(landscape_index)  # plot land
#water_plot(water_index)

crashed=False

number_of_days = 10

air = Air()
plt.figure()
plt.ion()

# world
for day in range(number_of_days):
    # update display
    pygame.display.flip()
    
    water_plot(water_index)

    # environment change
    for i in range(800):
        for j in range(800):
            # carbon cycle
            photosyn(Land_map[i][j], air)
            respr(Land_map[i][j], air)
            falling(Land_map[i][j])
            decomp(Land_map[i][j], air)
            # water cycle
            evapo(Land_map[i][j], air)
            '''
            neighbors = np.array([[1, 1], [1, -1], [-1, 1], [-1, -1]])
            for orient in range(4):
                [i1, j1] = [i, j] + neighbors[orient]
                if i1==800 or i1<0 or j1==800 or j1<0:
                    flow_off(Land_map[i][j], air)
                else:
                    inter_flow(Land_map[i][j], Land_map[i1][j1])
            ''' #网格径流 运行时间长
            p = rd.random()
            if p > 0.333:
                rain(air, Land_map[i][j])
            water_index[i][j] = Land_map[i][j].orig_soil_H2O
            
    # creatures change

plt.ioff()
pygame.quit()