import numpy as np
import math
from pygame import *


class biology:
    def __init__(
        self,
        speed,
        visibility,
        age,
        ageaverage,
        authenweight,
        energyweight,
        energystorage,
        setting,
        food,
        enermy,
        bio,
    ):  # 分别代表生物的运动能力，感知范围，年龄,寿命,幼年体重,
        # ，初始体重，初始储存能量,初始位置，食物,天敌,族群
        self.no_is = 1  # 存活判定
        self.speed = speed
        self.visibility = visibility
        self.age = float(age)
        self.ageaverage = ageaverage
        self.authenweight = authenweight
        self.energyweight = energyweight
        self.energystorage = energystorage
        self.setting = setting
        self.food = food
        self.enermy = enermy
        self.memory_data = []
        self.thirs = 100  # 渴值
        self.hungry_is = 1  # 是否饥饿
        self.seekis = 0  # 是否开始寻找
        self.enermy_is = 0  # 周围是否有天敌
        self.enermy_mem = 0  # 最近的天敌
        self.food_is = 0  # 周围是否有食物
        self.food_mem = 0  # 最近的食物
        self.energy_lose = 0  # 每个time损失的能量
        self.bear = 100  # 耐力值
        self.partner_is = 0  # 发情期判定
        self.part_is = 0  # 周围是否有配偶目标
        self.part_mem = 0  # 最近的配偶目标
        self.baby_is = 0  # 怀孕判定
        self.baby_time = 0  # 怀孕时间
        self.bio = bio

        self.color = (0, 0, 0)
        self.size = 5

    def draw(self, gameDisplay):
        draw.circle(gameDisplay, self.color, self.setting, self.size)

    def timemaker(self):
        self.time = self.age * 100
        self.time = self.time + 1
        self.age = self.time / 100
        return 1

    def age_energy_maker(self):  # 生长过程
        if self.age <= self.ageaverage * 0.3:
            weightaverage = (
                -500 / (9 * (self.ageaverage**2)) * (self.age**2)
                + 100 / (3 * self.ageaverage) * self.age
                + 1
            ) * self.authenweight
        elif (self.age > self.ageaverage * 0.3) & (self.age < self.ageaverage):
            weightaverage = (
                -500 / (49 * (self.ageaverage**2)) * (self.age**2)
                + 300 / (49 * self.ageaverage) * self.age
                + 249 / 49
            ) * self.authenweight
        else:
            self.no_is = 0
            weightaverage = self.authenweight
        result = np.random.normal(weightaverage, 0.25 * self.authenweight, 1)
        a = self.energyweight
        self.energyweight = result[0]
        self.energystorage = self.energystorage - (self.energyweight - a)
        if self.energystorage == 0:
            self.no_is = 0

    def walk(self):  # 饱食状态下的运动过程
        b = []
        for i in range(self.setting[0] - self.speed, self.setting[0] + self.speed + 1):
            for j in range(
                self.setting[1] - self.speed, self.setting[1] + self.speed + 1
            ):
                a = ((i - self.setting[0]) ** 2 + (j - self.setting[1]) ** 2) ** (0.5)
                if a <= self.speed:
                    b.append([i, j])
        c = np.random.randint(0, len(b))
        self.setting = b[c]
        self.energy_lose += self.speed
        self.energystorage -= self.speed

    def seekfor(self):  # 刚开始饥饿运动时，要先确定寻找的方向
        pass

    def seek(self):  # 饥饿状态下的觅食运动
        if (self.hungry == 1) & (self.seekis == 0):
            self.x, self.y = self.seekfor()
            seekis = 1
        self.setting[0] += self.x
        self.setting[1] += self.y

    def see(self, cate):  # 搜索函数
        b = []
        no = biology(0, 0, 0, 0, 0, 0, 0, [0, 0], "none", "none", "none")
        for i in range(
            self.setting[0] - self.visibility, self.setting[0] + self.visibility + 1
        ):
            for j in range(
                self.setting[1] - self.visibility, self.setting[1] + self.visibility + 1
            ):
                a = ((i - self.setting[0]) ** 2 + (j - self.setting[1]) ** 2) ** (0.5)
                if a <= self.visibility:
                    b.append([i, j])
        c = []
        for m in cate:
            for n in b:
                if (m.setting == n) & (m != self):
                    c.append(m)
        if c == []:
            return 0, no
        else:
            d = c[0]
            for i in c:
                x = (
                    (i.setting[0] - self.setting[0]) ** 2
                    + (i.setting[1] - self.setting[1]) ** 2
                ) ** 0.5
                y = (
                    (d.setting[0] - self.setting[0]) ** 2
                    + (d.setting[1] - self.setting[1]) ** 2
                ) ** 0.5
                if x <= y:
                    d = i
            return 1, d

    def seeforpart_mem(self, cate):  # 搜索函数
        b = []
        no = biology(0, 0, 0, 0, 0, 0, 0, [0, 0], "none", "none", "none")
        for i in range(
            self.setting[0] - self.visibility, self.setting[0] + self.visibility + 1
        ):
            for j in range(
                self.setting[1] - self.visibility, self.setting[1] + self.visibility + 1
            ):
                a = ((i - self.setting[0]) ** 2 + (j - self.setting[1]) ** 2) ** (0.5)
                if a <= self.visibility:
                    b.append([i, j])
        c = []
        for m in cate:
            for n in b:
                if (m.setting == n) & (m != self) & (m.partner_is == 1):
                    c.append(m)
        if c == []:
            return 0, no
        else:
            d = c[0]
            for i in c:
                x = (
                    (i.setting[0] - self.setting[0]) ** 2
                    + (i.setting[1] - self.setting[1]) ** 2
                ) ** 0.5
                y = (
                    (d.setting[0] - self.setting[0]) ** 2
                    + (d.setting[1] - self.setting[1]) ** 2
                ) ** 0.5
                if x <= y:
                    d = i
            return 1, d

    def memory(self, water):
        for i in water:
            a = 1
            for j in self.memory_data:
                if i == j:
                    a = 0
            if (a == 1) & (self.setting == i):
                self.memory_data.append(i)

    def bear_get(self):  # 耐力值获取系统
        self.bear += 5
        if self.bear >= 100:
            self.bear = 100
            self.quick_is = 1

    def bear_dec(self):  # 耐力值消耗系统
        self.bear -= 25
        if self.bear <= 0:
            self.bear = 0
            self.quick_is = 0

    """def predation(self,food,speed_s,speed_i):#捕食过程
        a=((food.setting[0]-self.setting[0])**2+(food.setting[1]-self.setting[1])**2)**0.5
        if a<=(speed_s-speed_i):
            self.setting=food.setting
            return 1
        else:
            for i in range(self.setting[0]-speed_s,self.setting[0]+speed_s+1):
                for j in range(self.setting[1]-speed_s,self.setting[1]+speed_s+1):
                    c=((i-self.setting[0])**2+(j-self.setting[1])**2)**(0.5)
                    if c<=speed_s:
                        b.append([i,j])
            n=b[0]
            for m in b:
                d=((m[0]-food.setting[0])**2+(m[1]-food.setting[1])**2)**(0.5)
                e=((n[0]-food.setting[0])**2+(n[1]-food.setting[1])**2)**(0.5)
                if d<=e:
                    n=m
            self.setting=n
            return 0"""

    def escape(self, enermy, speed_s, speed_i):  # 逃跑过程
        a = (
            (enermy.setting[0] - self.setting[0]) ** 2
            + (enermy.setting[1] - self.setting[1]) ** 2
        ) ** 0.5
        enermy.food_is, enermy.food_mem = enermy.see(enermy.food)
        if (
            (a <= (speed_i - speed_s))
            & (enermy.food_is == 1)
            & (enermy.food_mem == self)
            & (enermy.hungry_is == 1)
        ):
            self.energyweight = 0
            self.energystorage = 0
            self.energy_lose += speed_s
            return 0
        else:
            b = []
            for i in range(self.setting[0] - speed_s, self.setting[0] + speed_s + 1):
                for j in range(
                    self.setting[1] - speed_s, self.setting[1] + speed_s + 1
                ):
                    c = ((i - self.setting[0]) ** 2 + (j - self.setting[1]) ** 2) ** (
                        0.5
                    )
                    if c <= speed_s:
                        b.append([i, j])
            n = b[0]
            for m in b:
                d = (
                    (m[0] - enermy.setting[0]) ** 2 + (m[1] - enermy.setting[1]) ** 2
                ) ** (0.5)
                e = (
                    (n[0] - enermy.setting[0]) ** 2 + (n[1] - enermy.setting[1]) ** 2
                ) ** (0.5)
                if d >= e:
                    n = m
            self.setting = n
            self.energy_lose += speed_s
            self.energystorage -= speed_s
            return 1

    def thirsty(self):  # 渴觉系统
        self.thirs -= 1

    def seekforwater(self):  # 觅水行为,确定方向
        a = self.memory_data[0]
        for i in self.memory_data:
            m = ((a[0] - self.setting[0]) ** 2 + (a[1] - self.setting[1]) ** 2) ** (0.5)
            n = ((i[0] - self.setting[0]) ** 2 + (i[1] - self.setting[1]) ** 2) ** (0.5)
            if n <= m:
                a = i
        return a

    def runforwater(self, target):  # 开始觅水
        b = []
        for i in range(self.setting[0] - self.speed, self.setting[0] + self.speed + 1):
            for j in range(
                self.setting[1] - self.speed, self.setting[1] + self.speed + 1
            ):
                a = ((i - self.setting[0]) ** 2 + (j - self.setting[1]) ** 2) ** (0.5)
                if a <= self.speed:
                    b.append([i, j])
        c = b[0]
        for i in b:
            m = ((c[0] - target[0]) ** 2 + (c[1] - target[1]) ** 2) ** (0.5)
            n = ((i[0] - target[0]) ** 2 + (i[1] - target[1]) ** 2) ** (0.5)
            if n <= m:
                c = i
        self.setting = c
        if c == target:
            self.thirs = 100

    def courtship(self, target):  # 配偶寻觅机制
        x = (
            (self.setting[0] - target.setting[0]) ** 2
            + (self.setting[1] - target.setting[1]) ** 2
        ) ** 0.5
        b = []
        for i in range(self.setting[0] - self.speed, self.setting[0] + self.speed + 1):
            for j in range(
                self.setting[1] - self.speed, self.setting[1] + self.speed + 1
            ):
                a = ((i - self.setting[0]) ** 2 + (j - self.setting[1]) ** 2) ** (0.5)
                if a <= self.speed:
                    b.append([i, j])
        c = b[0]
        for i in b:
            m = ((c[0] - target[0]) ** 2 + (c[1] - target[1]) ** 2) ** (0.5)
            n = ((i[0] - target[0]) ** 2 + (i[1] - target[1]) ** 2) ** (0.5)
            if n <= m:
                c = i
        if x <= self.speed + target.speed:
            return 1, c
        else:
            return 0, c


    def eatgrass(self,grass):
        self.energystorage+=grass[self.setting[0]][self.setting[1]].orig_plant_C
        #grass[self.setting[0]][self.setting[1]]=0
        grass[self.setting[0]][self.setting[1]].orig_plant_C=0

    def partnership(self):
        if (
            (self.age >= self.ageaverage * 0.2)
            & (self.age <= self.ageaverage * 0.3)
            & (self.baby_is == 0)
        ):
            self.partner_is = 1
        else:
            self.partner_is = 0

    def sex(self, target):
        if self.part_is == 0:
            pass
        else:
            self.baby_is = 1
            self.partner_is = 0
            target.baby_is = 1
            target.partner_is = 0

    def babygrow(self):
        self.baby_time += 25
        if self.baby_time >= 5 * self.ageaverage:
            self.bio.append(
                biology(
                    self.speed,
                    self.visibility,
                    0,
                    self.ageaverage,
                    self.authenweight,
                    self.authenweight,
                    0.5 * self.energystorage,
                    self.setting,
                    self.food,
                    self.enermy,
                    self.bio,
                )
            )
            self.energyweight -= self.authenweight
            self.energyweight = self.energyweight * 0.5
            self.baby_is = 0
