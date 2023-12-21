from creature_repo import *
from land import *
from landscape_test import *
import pygame


landscape = [[[] * 4] * 800] * 800
Land_map = [[Land(0) for _ in range(800)] for _ in range(800)]
landscape_index = np.zeros((800, 800))
water_index = np.zeros((800, 800))
resc_prodc = np.zeros((800, 800))
air = Air()
water = []  # 水源地块
for i in range(5, 10):
    for j in range(10, 20):
        water.append([i, j])

"""
"""
wolf = []
rabbit = []

wolf_1 = biology(2, 4, 1, 10, 5, 100, 100, [2, 1], rabbit, "none", wolf)
rabbit_1 = biology(
    3, 5, 2.5, 10, 5, 100, 100, [5, 60], "grass", wolf, rabbit
)  # 分别代表生物的运动能力，感知范围，年龄,寿命,幼年体重,初始体重，初始储存能量,初始位置，食物,天敌,族群
rabbit_2 = biology(3, 5, 2.5, 10, 5, 100, 100, [5, 59], "grass", wolf, rabbit)

rabbit_2.partner_is = 1
wolf.append(wolf_1)
rabbit.append(rabbit_1)
rabbit.append(rabbit_2)
rabbit_1.memory_data = [[7, 15]]  # 初始记忆地块


def environment_chage():
    for i in range(800):
        for j in range(800):
            # carbon cycle
            photosyn(Land_map[i][j], air)
            respr(Land_map[i][j], air)
            falling(Land_map[i][j])
            decomp(Land_map[i][j], air)
            # water cycle
            evapo(Land_map[i][j], air)
            #'''
            neighbors = np.array([[1, 1], [1, -1], [-1, 1], [-1, -1]])
            for orient in range(4):
                [i1, j1] = [i, j] + neighbors[orient]
                if i1 == 800 or i1 < 0 or j1 == 800 or j1 < 0:
                    flow_off(Land_map[i][j], air)
                else:
                    inter_flow(Land_map[i][j], Land_map[i1][j1])
            #''' #网格径流 运行时间长
            p = rd.random()
            if p > 0.333:
                rain(air, Land_map[i][j])
            water_index[i][j] = Land_map[i][j].orig_soil_H2O


def life():
    rabbit_1.energy_lose = 0  # 每个time损失的能量归零
    rabbit_1.timemaker()  # 年龄增长
    rabbit_1.partnership()  # 发情期判定
    print(rabbit_1.age)
    rabbit_1.age_energy_maker()  # 生长
    print(rabbit_1.energyweight, rabbit_1.energystorage)
    rabbit_1.enermy_is, rabbit_1.enermy_mem = rabbit_1.see(
        rabbit_1.enermy
    )  # 检索周围，是否有天敌
    print(rabbit_1.enermy_is, rabbit_1.enermy_mem.setting)
    if rabbit_1.enermy_is == 1:  # 如果有天敌，开始逃跑
        if (rabbit_1.bear >= 25) & (
            rabbit_1.enermy_mem.bear >= 25
        ):  # 如果双方都有耐力值剩余，两者以2倍速度展开追逐
            rabbit_1.no_is = rabbit_1.escape(
                rabbit_1.enermy_mem, 2 * rabbit_1.speed, 2 * rabbit_1.enermy_mem.speed
            )
            rabbit_1.bear_dec()
            rabbit_1.enermy_mem.bear_dec()
        elif (rabbit_1.bear < 25) & (rabbit_1.enermy_mem.bear >= 25):
            rabbit_1.no_is = rabbit_1.escape(
                rabbit_1.enermy_mem, rabbit_1.speed, 2 * rabbit_1.enermy_mem.speed
            )
            rabbit_1.enermy_mem.bear_dec()
        elif (rabbit_1.bear >= 25) & (rabbit_1.enermy_mem.bear < 25):
            rabbit_1.no_is = rabbit_1.escape(
                rabbit_1.enermy_mem, 2 * rabbit_1.speed, rabbit_1.enermy_mem.speed
            )
            rabbit_1.bear_dec()
        elif (rabbit_1.bear < 25) & (
            rabbit_1.enermy_mem.bear < 25
        ):  # 如果双方都没有耐力值剩余，两者以最大速度展开追逐
            rabbit_1.no_is = rabbit_1.escape(
                rabbit_1.enermy_mem, rabbit_1.speed, rabbit_1.enermy_mem.speed
            )
        rabbit_1.memory(water)  # 记忆可能遇到的水源
        print(
            rabbit_1.no_is,
            rabbit_1.energy_lose,
            rabbit_1.energystorage,
            rabbit_1.setting,
            rabbit_1.memory_data,
        )
    elif rabbit_1.energystorage <= 50:  # 如果储存的能量不足，开始觅食运动
        rabbit_1.hungry_is = 1
        rabbit_1.walk()  # 随机运动
        rabbit_1.memory(water)  # 记忆可能遇到的水源
        rabbit_1.eatgrass(resc_prodc)  # 获取地块上的全部能量
        print(
            rabbit_1.setting,
            rabbit_1.energystorage,
            rabbit_1.energy_lose,
            rabbit_1.memory_data,
        )
    elif rabbit_1.thirs <= 30:  # 如果水分不足，开始觅水
        target = rabbit_1.seekforwater()
        rabbit_1.runforwater(target)
        print(rabbit_1.setting, target, rabbit_1.thirs)
    elif rabbit_1.partner_is == 1:  # 如果处于发情期，开始寻找配偶
        rabbit_1.walk()  # 随机运动
        rabbit_1.memory(water)  # 记忆可能遇到的水源
        rabbit_1.part_is, rabbit_1.part_mem = rabbit_1.seeforpart_mem(
            rabbit
        )  # 寻找周围环境中可能存在的配偶
        rabbit_1.sex(rabbit_1.part_mem)
        print(
            rabbit_1.part_is,
            rabbit_1.part_mem.setting,
            rabbit_1.setting,
            rabbit_1.baby_is,
        )
    if rabbit_1.baby_is == 1:  # 如果怀孕，孩子的年龄孕期增加
        rabbit_1.babygrow()
        print(rabbit_1.baby_time)
    rabbit_1.thirsty()  # 每time结束，扣除一点渴觉
    if rabbit_1.thirs <= 0:
        rabbit_1.no_is = 0
    if rabbit_1.energystorage <= 0:
        rabbit_1.no_is = 0
    if rabbit_1.no_is == 0:
        rabbit.remove(rabbit_1)


def print_creatures(game_display):
    for creature in rabbit:
        creature.draw(game_display)
