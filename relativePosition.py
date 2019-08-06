# -*- coding: utf-8 -*-

#   2019/7/23 0023 下午 4:03     

__author__ = 'RollingBear'

import math

from sympy import *
from math import radians, cos, sin, asin, sqrt, degrees


class relativePosition():

    def __init__(self, postLongitude, postLatitude, lightLongitude, lightLatitude):
        '''
        传入数据，初始化信号源和探照灯经纬度
        :param postLongitude: 信号源经度(x)
        :param postLatitude: 信号源纬度(y)
        :param lightLongitude: 探照灯经度(x)
        :param lightLatitude: 探照灯纬度(y)
        '''

        # 地球半径
        self.R = 6372795.477598
        self.Ea = 6378137 # 赤道半径
        self.Eb = 6356725 # 极半径

        self.postLongitude = postLongitude
        self.postLatitude = postLatitude
        self.lightLongitude = lightLongitude
        self.lightLatitude = lightLatitude

    def getCoordinate(self, distance, angle):
        '''
        通过角度和距离计算目标经纬度
        :param distance: 距离
        :param angle: 角度
        :return:目标位置的元祖(目标位置经度, 目标位置纬度)
        '''

        dx = distance * sin(angle * math.pi / 180.0)
        dy = distance * cos(angle * math.pi / 180.0)

        ec = self.Eb + (self.Ea - self.Eb) * (90.0 - self.postLatitude) / 90.0
        ed = ec * cos(self.postLatitude * math.pi / 180.0)

        resultLongitude = (dx / ed + self.postLongitude * math.pi / 180.0) * 180.0 / math.pi
        resultLatitude = (dy / ec + self.postLatitude *math.pi / 180.0) * 180.0 / math.pi

        return (resultLongitude, resultLatitude)

    def getDistance(self, longitude1, latitude1, longitude2, latitude2):
        '''
        使用两点的经纬度坐标计算两点间距离
        :param longitude1: 位置1经度
        :param latitude1: 位置1纬度
        :param longitude2: 位置2经度
        :param latitude2: 位置2纬度
        :return: 距离
        '''

        flatten = (self.Ea - self.Eb) / self.Ea
        longitude1, latitude1, longitude2, latitude2 = map(radians, [longitude1, latitude1, longitude2, latitude2])
        pA = atan(self.Eb / self.Ea * tan(latitude1))
        pB = atan(self.Eb / self.Ea * tan(latitude2))

        x = acos(sin(pA) * sin(pB) + cos(pA) * cos(pB) * cos(longitude1 - longitude2))

        c1 = (sin(x) - x) * (sin(pA) + sin(pB)) ** 2 / cos(x / 2) ** 2
        c2 = (sin(x) + x) * (sin(pA) - sin(pB)) ** 2 / sin(x / 2) ** 2

        dr = flatten / 8 * (c1 - c2)
        distance = self.Ea * (x + dr)

        return distance

    def getAngle(self, longitude1, latitude1, longitude2, latitude2):
        '''
        使用两点的经纬度坐标计算位置2相对于位置1的角度
        :param longitude1: 位置1经度
        :param latitude1: 位置1纬度
        :param longitude2: 位置2经度
        :param latitude2: 位置2纬度
        :return: 角度
        '''

        radLat1 = radians(latitude1)
        radLon1 = radians(longitude1)
        radLat2 = radians(latitude2)
        radLon2 = radians(longitude2)
        dLon = radLon2 - radLon1

        y = sin(dLon) * cos(radLat2)
        x = cos(radLat1) * sin(radLat2) - sin(radLat1) * cos(radLat2) * cos(dLon)
        angle = degrees(atan2(y, x))
        angle = (angle + 360) % 360
        return angle

    def getResult(self, distance, angle):
        '''
        获取目标相对于探照灯的距离和方位角
        :param distance: 目标和观测点的距离
        :param angle: 目标相对于观测点的方位角
        :return: 字典
        '''

        shipPosition = self.getCoordinate(distance, angle)

        distanceResult = self.getDistance(self.lightLongitude, self.lightLatitude, shipPosition[0], shipPosition[1])

        angleResult = self.getAngle(self.lightLongitude, self.lightLatitude, shipPosition[0], shipPosition[1])

        return {'distance': distanceResult,
                'angle': angleResult}


if __name__ == '__main__':
    postLon = 116.322201
    postLat = 39.895349

    lightLon = 116.378506
    lightLat = 39.866369

    relative1 = relativePosition(postLon, postLat, lightLon, lightLat)

    print(relative1.getCoordinate(30400, 45))
    print(relative1.getResult(30400, 45))

    relative2 = relativePosition(116.57426789092189, 40.088739059087956, postLon, postLat)

    print(relative2.getCoordinate(29820.4563410530, 213.940890532890705))
    print(relative2.getResult(29820.4563410530, 213.940890532890705))

    postLon = 117.986298
    postLat = 38.400469

    lightLon = 121.120234
    lightLat = 38.806942

    pointLon = 121.837864
    pointLat = 40.865465

    relative3 = relativePosition(postLon, postLat, lightLon, lightLat)

    print(relative3.getDistance(postLon, postLat, pointLon, pointLat))
    print(relative3.getAngle(postLon, postLat, pointLon, pointLat))

    relative4 = relativePosition(postLon, postLat, lightLon, lightLat)

    print(relative4.getCoordinate(429145, 49.056))
    print(relative4.getResult(429145, 49.056))