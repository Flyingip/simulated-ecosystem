from pygame import *
from land import *
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

#地图数据
landscape = [[[] * 4] * 800] * 800
for i in range(0, 800):
    for j in range(0, 800):
        landscape[i][j] = game_display.get_at((i, j))

crashed=False

number_of_days = 5000

# world

for day in range(0,number_of_days):
    display.flip()
