from land import *
from landscape_test import *
import pygame

# init()

clock=time.Clock()

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
for i in range(0, 800):
    for j in range(0, 800):
        landscape[i][j] = game_display.get_at((i, j))  # get pixels
        Land_map[i][j] = Land(land_comp(landscape[i][j]))  # store as indexes
        landscape_index[i][j] = Land_map[i][j].index
land_plot(landscape_index)  # plot land


crashed=False

number_of_days = 1000

# world
while True:
    # update display
    for day in range(0, number_of_days):
        display.flip()
    # environment change

    # creatures change

    pygame.quit()