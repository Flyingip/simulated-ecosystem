# todo
'''
根据单个生物的位置返回可视化内容

地图生成，根据坐标，单元格

画格子，主函数
'''
from pygame import *
# from land import *

# init()

clock=time.Clock()

# 地图的大小

h=800
w=800

game_display=display.set_mode((h,w))
display.set_caption("simulated-ecosystem")

crashed=False

number_of_days =1000

# world

for day in range(0,number_of_days):
    game_display.fill((255,255,255))
    # 自然运动，生物的运动，打印

