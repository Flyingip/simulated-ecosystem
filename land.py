from pygame import *
import numpy as np
import random as rd


class Land:
    def __init__(self, index):
        # index为类型序号，
        # 0河流
        # 1河边草地
        # 2平原草地
        # 3平原森林
        # 4高山草地
        # 5高山荒地
        self.index = index
        self.qualt_H2O = 0
        self.qualt_resc = 0
        self.qualt_metbls = 0
        self.qualt_rain = 0
        self.qualt_off = 0
        match self.index:
            case 0:
                self.land_type = "river"
            case 1:
                self.land_type = "riverside_meadow"  # 类型名称
                self.qualt_H2O = 1.5  # 水量因子（与植被有关
                self.qualt_resc = 1  # 资源量因子（与植被有关
                self.qualt_metbls = 1.2  # 代谢率因子（与植被有关
                self.qualt_rain = 1  # 降雨概率因子（与海拔有关
                self.qualt_off = 0.5  # 损失率因子（与植被有关
            case 2:
                self.land_type = "plain_meadow"
                self.qualt_H2O = 1
                self.qualt_resc = 1
                self.qualt_metbls = 1
                self.qualt_rain = 1
                self.qualt_off = 0.5
            case 3:
                self.land_type = "plain_forest"
                self.qualt_H2O = 1.2
                self.qualt_resc = 1.5
                self.qualt_metbls = 1.2
                self.qualt_rain = 1
                self.qualt_off = 0.3
            case 4:
                self.land_type = "mountain_meadow"
                self.qualt_H2O = 0.8
                self.qualt_resc = 0.8
                self.qualt_metbls = 0.6
                self.qualt_rain = 0.5
                self.qualt_off = 0.5
            case 5:
                self.land_type = "mountain_desert"
                self.qualt_H2O = 0.5
                self.qualt_resc = 0.1
                self.qualt_metbls = 0.3
                self.qualt_rain = 0.5
                self.qualt_off = 1
        ###水循环部分
        self.orig_soil_H2O = self.qualt_H2O * 10  # 初始土壤水，标准为10
        self.evapo_rate = (
            self.qualt_off * self.orig_soil_H2O * 0.01
        )  # 蒸发速率，标准为0.01倍水量(约10*0.01*800*800=64000)
        self.flow_rate = self.qualt_off * self.orig_soil_H2O * 0.01  # 径流速率，标准为0.01倍水量
        self.rain_rate = self.qualt_rain * 0.2  # 降雨速率，标准为0.2
        self.new_soil_H2O = self.orig_soil_H2O
        ###碳循环部分
        self.orig_plant_C = self.qualt_resc * 5  # 初始植物碳，标准为100
        self.prodc_rate = self.qualt_resc * self.qualt_H2O * 3  # 光合作用生产植物有机物速率，标准为3
        self.respr_rate = self.qualt_metbls * 0.5  # 呼吸作用消耗植物有机物速率，标准为0.5
        self.fallin_rate = 0.5 * self.qualt_metbls * 0.1  # 死亡/掉落消耗植物有机物速率，标准的0.5概率的0.1
        self.orig_soil_C = self.qualt_resc * 10  # 初始土壤碳，标准为10
        self.decom_rate = self.qualt_metbls * 0.1  # 分解作用消耗土壤有机物速率，标准为0.1


class Air:
    def __init__(self):
        self.orig_air_H2O = 10000  # 初始大气水
        self.orig_air_C = 10000  # 初始大气碳
        # 水汽输送（水量补充）速率


# 径流函数
def inter_flow(Land1, Land2):
    Land1.new_soil_H2O = Land1.orig_soil_H2O - Land1.flow_rate * 0.25
    Land1.orig_soil_H2O = Land1.new_soil_H2O
    Land2.new_soil_H2O = Land2.orig_soil_H2O + Land1.flow_rate * 0.25
    Land2.orig_soil_H2O = Land2.new_soil_H2O


def flow_off(Land, Air):
    Land.new_soil_H2O = Land.orig_soil_H2O - Land.flow_rate * 0.25
    Land.orig_soil_H2O = Land.new_soil_H2O
    Air.orig_air_H2O = Air.orig_air_H2O + Land.flow_rate * 0.25


# 降水函数
def rain(Air, Land):
    rain_rate = Land.rain_rate * np.random.normal(
        1, 0.1
    )  # 降雨速率 平均0.2 减少0.2*800*800=2*64000
    if rain_rate > 0:
        Land.new_soil_H2O = Land.orig_soil_H2O + rain_rate
        Land.orig_soil_H2O = Land.new_soil_H2O
        Air.new_air_H2O = Air.orig_air_H2O - rain_rate
        Air.orig_air_H2O = Air.new_air_H2O


# 蒸发作用函数
def evapo(Land, Air):
    Land.new_soil_H2O = Land.orig_soil_H2O - Land.evapo_rate
    Land.orig_soil_H2O = Land.new_soil_H2O
    Air.new_air_H2O = Air.orig_air_H2O + Land.evapo_rate
    Air.orig_air_H2O = Air.new_air_H2O


# 光合作用函数（植物&大气
def photosyn(Land, Air):
    Land.new_plant_C = Land.orig_plant_C + Land.prodc_rate
    Land.orig_plant_C = Land.new_plant_C
    Air.new_air_C = Air.orig_air_C - Land.prodc_rate
    Air.orig_air_C = Air.new_air_C


# 呼吸作用函数（植物&大气
def respr(Land, Air):
    Land.new_plant_C = Land.orig_plant_C - Land.respr_rate
    Land.orig_plant_C = Land.new_plant_C
    Air.new_air_C = Air.orig_air_C + Land.respr_rate
    Air.orig_air_C = Air.new_air_C


# 死亡掉落函数（植物&土壤
def falling(Land):
    Land.new_plant_C = Land.orig_plant_C - Land.fallin_rate
    Land.orig_plant_C = Land.new_plant_C
    Land.new_soil_C = Land.orig_soil_C + Land.fallin_rate
    Land.orig_soil_C = Land.new_soil_C


# 分解作用函数（土壤&大气
def decomp(Land, Air):
    Land.new_soil_C = Land.orig_soil_C - Land.decom_rate
    Land.orig_plant_C = Land.new_plant_C
    Air.new_air_C = Air.orig_air_C + Land.decom_rate
    Air.orig_air_C = Air.new_air_C


##12.5  接口：动物尸体 动物呼吸消耗的能量（大气） 动物摄取植物的有机物量
def die(Animal, Land):
    Land.new_soil_C = Land.orig_soil_C  # + 动物能量
    Land.orig_soil_C = Land.new_soil_C


def respr_a(Animal, Land):
    Land.new_soil_C = Land.orig_soil_C  # - 动物呼吸
    Land.orig_soil_C = Land.new_soil_C


def eat(Animal, Land):
    Land.new_plant_C = Land.orig_plant_C  # - 动物摄入
    Land.orig_plant_C = Land.new_plant_C
