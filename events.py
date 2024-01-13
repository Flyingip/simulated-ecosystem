from creature import *
from land import *
from landscape_test import *
import pygame

air = Air()
h, w = 800, 800


def environment_chage(Land_map, water_index, resc_prodc):
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

            p = rd.random()
            if p > 0.333:
                rain(air, Land_map[i][j])
            water_index[i][j] = Land_map[i][j].orig_soil_H2O
    # water_plot(water_index)
    # C_plot(resc_prodc)


# rabbit = []
# wolf = []


def spwan(rabbit, wolf, river):
    # 群体
    for i in range(20):
        a = np.random.randint(0, 800)
        b = np.random.randint(0, 800)
        c = biology(
            10,
            np.random.randint(10, 120),
            2.5,
            10,
            5,
            100,
            100,
            [a, b],
            "grass",
            wolf,
            rabbit,
        )
        c.memory_data.append(river[np.random.randint(26163)])
        rabbit.append(c)
    for j in range(10):
        a = np.random.randint(0, 800)
        b = np.random.randint(0, 800)
        c = biology(20, 100, 2.5, 10, 5, 100, 100, [a, b], rabbit, "none", wolf)
        c.memory_data.append(river[np.random.randint(26163)])
        wolf.append(c)
    return rabbit, wolf


def neuron(creature, Land_map, river):
    creature.energy_lose = 0  # 每个time损失的能量归零
    creature.timemaker()  # 年龄增长
    creature.partnership()  # 发情期判定
    creature.age_energy_maker()  # 生长
    if creature.energystorage > 70:  # 如果储存的能量不足，开始觅食运动
        creature.hungry_is = 0
    if creature.enermy != "none":
        creature.enermy_is, creature.enermy_mem = creature.see(
            creature.enermy
        )  # 检索周围，是否有天敌
    if creature.enermy_is == 1:  # 如果有天敌，开始逃跑
        if (creature.bear >= 25) & (
            creature.enermy_mem.bear >= 25
        ):  # 如果双方都有耐力值剩余，两者以2倍速度展开追逐
            creature.no_is = creature.escape(
                creature.enermy_mem, 2 * creature.speed, 2 * creature.enermy_mem.speed
            )
            creature.bear_dec()
            creature.enermy_mem.bear_dec()
        elif (creature.bear < 25) & (creature.enermy_mem.bear >= 25):
            creature.no_is = creature.escape(
                creature.enermy_mem, creature.speed, 2 * creature.enermy_mem.speed
            )
            creature.enermy_mem.bear_dec()
        elif (creature.bear >= 25) & (creature.enermy_mem.bear < 25):
            creature.no_is = creature.escape(
                creature.enermy_mem, 2 * creature.speed, creature.enermy_mem.speed
            )
            creature.bear_dec()
        elif (creature.bear < 25) & (
            creature.enermy_mem.bear < 25
        ):  # 如果双方都没有耐力值剩余，两者以最大速度展开追逐
            creature.no_is = creature.escape(
                creature.enermy_mem, creature.speed, creature.enermy_mem.speed
            )
        # creature.memory(river)  # 记忆可能遇到的水源,天敌追逐不要记了逃命重要
    elif creature.energystorage <= 70:  # 如果储存的能量不足，开始觅食运动
        creature.hungry_is = 1
        if creature.food == "grass":
            creature.walk()  # 随机运动
            creature.memory(river)  # 记忆可能遇到的水源
            Land_map = creature.eatgrass(Land_map)  # 获取地块上的全部能量
        else:
            creature.food_is, creature.food_mem = creature.see(creature.food)
            if creature.food_mem.food != "none":
                creature.predation(
                    creature.food_mem, creature.speed, creature.food_mem.speed
                )
            else:
                creature.walk()
            creature.memory(river)  # 记忆可能遇到的水源
    elif creature.thirs <= 60:  # 如果水分不足，开始觅水
        target = creature.seekforwater()
        creature.runforwater(target)
        creature.memory(river)
    elif creature.partner_is == 1:  # 如果处于发情期，开始寻找配偶
        creature.walk()  # 随机运动
        creature.memory(river)  # 记忆可能遇到的水源
        creature.part_is, creature.part_mem = creature.seeforpart_mem(
            creature.bio
        )  # 寻找周围环境中可能存在的配偶
        creature.sex(creature.part_mem)
    else:  # 在没有任何行为目的的情况下，开始自由运动
        creature.walk()
        creature.memory(river)  # 记忆可能遇到的水源
    if creature.baby_is == 1:  # 如果怀孕，孩子的年龄孕期增加
        creature.babygrow()
    creature.thirsty()  # 每time结束，扣除一点渴觉
    if creature.thirs <= 0:
        creature.no_is = 0
        Land_map[creature.setting[0]][
            creature.setting[1]
        ].orig_soil_C += creature.energystorage
        Land_map[creature.setting[0]][
            creature.setting[1]
        ].orig_soil_C += creature.energyweight
    if creature.energystorage <= 0:
        creature.no_is = 0
        if creature.setting[0] < 0:
            creature.setting[0] += 800
        if creature.setting[1] < 0:
            creature.setting[1] += 800
        if creature.setting[0] > 799:
            creature.setting[0] -= 800
        if creature.setting[1] > 799:
            creature.setting[1] -= 800
        Land_map[creature.setting[0]][
            creature.setting[1]
        ].orig_soil_C += creature.energystorage
        Land_map[creature.setting[0]][
            creature.setting[1]
        ].orig_soil_C += creature.energyweight
    if creature.no_is == 0:
        creature.bio.remove(creature)
    return Land_map


def print_creatures(rabbit, wolf, game_display, transparent_surface):
    for creature in rabbit:
        creature.draw_transparent(transparent_surface, (255, 255, 255, 64))  # 感知圈
        if creature.energystorage <= 10:  # 濒死
            creature.draw(game_display, (255, 125, 255), 4)
        elif creature.hungry_is == 1:
            creature.draw(game_display, (255, 255, 0), 4)
        else:
            creature.draw(game_display, (0, 255, 255), 4)

        # game_display.blit(image_rabbit, creature.getpos())
        # creature.draw(game_display, rabbit)
    for creature in wolf:
        creature.draw_transparent(transparent_surface, (255, 255, 255, 64))  # 感知圈
        if creature.energystorage <= 10:  # 濒死
            creature.draw(game_display, (255, 0, 255), 5)
            creature.draw(game_display, (0, 0, 0), 3)
        elif creature.hungry_is == 1:
            creature.draw(game_display, (255, 0, 0), 5)
            creature.draw(game_display, (0, 0, 0), 3)
        else:
            creature.draw(game_display, (0, 0, 255), 5)
            creature.draw(game_display, (0, 0, 0), 3)


def draw_plant(gameDisplay, resc_prodc):
    for i in range(h):
        for j in range(w):
            if resc_prodc[i][j] != 0:
                draw.circle(gameDisplay, (0, 0, 0), (i, j), 1 * resc_prodc[i][j])


r_num = []
w_num = []

aver = []


def plot_stats(rabbit, wolf):
    global r_num, w_num, aver
    sight = []
    num_rabbit = len(rabbit)
    num_wolf = len(wolf)
    r_num.append(num_rabbit)
    w_num.append(num_wolf)

    for r in rabbit:
        sight.append(r.visibility)

    if num_rabbit != 0:
        aver.append(sum(sight) / num_rabbit)
    else:
        aver = 0

    fig, (ax1, ax2) = plt.subplots(1, 2)

    ax1.plot(r_num, label="Rabbit")
    ax1.plot(w_num, label="Wolf")
    ax2.plot(aver, label="average_sight")

    ax1.legend()
    ax1.grid(True)
    ax2.legend()
    ax2.grid(True)
    plt.savefig("results.pdf")
    plt.close(fig)
