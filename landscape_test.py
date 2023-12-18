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

#地图数据 初始化
landscape = [[[] * 4] * 800] * 800
Land_map = [[Land(0) for _ in range(800)] for _ in range(800)]
for i in range(0, 800):
    for j in range(0, 800):
        landscape[i][j] = game_display.get_at((i, j))
        if landscape[i][j] == (1, 173, 255, 255):
            Land_map[i][j] = Land(0)
        elif landscape[i][j] == (24, 173, 1, 255):
            Land_map[i][j] = Land(1)
        elif landscape[i][j] == (36, 255, 1, 255):
            Land_map[i][j] = Land(2)
        elif landscape[i][j] == (12, 86, 1, 255):
            Land_map[i][j] = Land(3)
        elif landscape[i][j] == (231, 255, 1, 255):
            Land_map[i][j] = Land(4)
        elif landscape[i][j] == (120, 132, 1, 255):
            Land_map[i][j] = Land(5)
        else:
            Land_map[i][j] = Land(2)
            

crashed=False

number_of_days = 5000

# world

for day in range(0,number_of_days):
    display.flip()
