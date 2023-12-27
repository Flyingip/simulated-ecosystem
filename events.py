from creature import *
from land import *
from landscape_test import *

# def environment_chage(Land_map):
#     for i in range(800):
#         for j in range(800):
#             # carbon cycle
#             photosyn(Land_map[i][j], air)
#             respr(Land_map[i][j], air)
#             falling(Land_map[i][j])
#             decomp(Land_map[i][j], air)
#             # water cycle
#             evapo(Land_map[i][j], air)
#             #'''
#             neighbors = np.array([[1, 1], [1, -1], [-1, 1], [-1, -1]])
#             for orient in range(4):
#                 [i1, j1] = [i, j] + neighbors[orient]
#                 if i1 == 800 or i1 < 0 or j1 == 800 or j1 < 0:
#                     flow_off(Land_map[i][j], air)
#                 else:
#                     inter_flow(Land_map[i][j], Land_map[i1][j1])
#             #''' #网格径流 运行时间长
#             p = rd.random()
#             if p > 0.333:
#                 rain(air, Land_map[i][j])
#             water_index[i][j] = Land_map[i][j].orig_soil_H2O
river = []  ###

rabbit = []
wolf = []
# 群体
for i in range(20):
    a = np.random.randint(0, 800)
    b = np.random.randint(0, 800)
    rabbit.append(biology(3, 5, 2.5, 10, 5, 100, 100, [a, b], "grass", wolf, rabbit))
for j in range(10):
    a = np.random.randint(0, 800)
    b = np.random.randint(0, 800)
    wolf.append(biology(2, 4, 1, 10, 5, 100, 100, [a, b], rabbit, "none", wolf))


# 食肉系动物
# 输出1：年龄改变+返回值 （年龄增长）
# 输出2：体重，储存能量   （生长）
# 输出3：是否有天敌  最近的天敌位置   （危险察觉）
# 输出4.1：存活情况 能量消耗 能量储存  位置  记忆地块（察觉到危险后逃跑）
# 输出4.2：位置   能量储存  能量消耗    记忆地块（没有危险，饥饿时的摄食行为）
# 输出4.3：位置，目标，渴度
# 输出4.4：是否有对象  对象位置  位置  是否怀孕（寻找配偶）
# 输出5：怀孕时间
def neuron(creature, Land_map):
    creature.energy_lose = 0  # 每个time损失的能量归零
    creature.timemaker()  # 年龄增长
    creature.partnership()  # 发情期判定
    creature.age_energy_maker()  # 生长
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
        creature.memory(river)  # 记忆可能遇到的水源
    elif creature.energystorage <= 50:  # 如果储存的能量不足，开始觅食运动
        creature.hungry_is = 1
        if creature.food == "grass":
            creature.walk()  # 随机运动
            creature.memory(river)  # 记忆可能遇到的水源
            creature.eatgrass(Land_map)  # 获取地块上的全部能量
        else:
            creature.food_is, creature.food_mem = creature.see(creature.food)
            creature.predation(
                creature.food_mem, creature.speed, creature.food_mem.speed
            )
            creature.memory(river)  # 记忆可能遇到的水源
    elif creature.thirs <= 30:  # 如果水分不足，开始觅水
        target = creature.seekforwater()
        creature.runforwater(target)
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
    if creature.energystorage <= 0:
        creature.no_is = 0
    if creature.no_is == 0:
        creature.bio.remove(creature)


def print_creatures(game_display):
    for creature in rabbit:
        creature.draw(game_display)


# def clear_creatures(game_display):
#     for creature in rabbit:
#         creature.draw(game_display)
