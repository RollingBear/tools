# -*- coding: utf-8 -*-

#   2019/7/23 0023 下午 4:03     

__author__ = 'RollingBear'

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
        self.R = 6371 * 1000

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

        resultLongitude = self.postLongitude + (180 * distance * sin(radians(angle)) / (self.R * pi))
        resultLatitude = self.postLatitude + (180 * distance * cos(radians(angle)) / (self.R * pi))

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

        longitude1, latitude1, longitude2, latitude2 = map(radians,
                                                           [float(longitude1), float(latitude1), float(longitude2),
                                                            float(latitude2)])
        dlon = longitude2 - longitude1
        dlat = latitude2 - latitude1
        a = sin(dlat / 2) ** 2 + cos(latitude1) * cos(latitude2) * sin(dlon / 2) ** 2
        distance = 2 * asin(sqrt(a)) * self.R
        distance = round(distance, 3)
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
        :return: 元祖(目标和探照灯的距离, 目标相对于探照灯的方位角)
        '''

        shipPosition = self.getCoordinate(distance, angle)

        distanceShipLight = self.getDistance(self.lightLongitude, self.lightLatitude, shipPosition[0], shipPosition[1])

        angleShipLight = self.getAngle(self.lightLongitude, self.lightLatitude, shipPosition[0], shipPosition[1])

        return (distanceShipLight, angleShipLight)


if __name__ == '__main__':
    postLon = 0
    postLat = 0

    lightLon = 0.001254513
    lightLat = 0.000000023

    relativePositioning = relativePosition(postLon, postLat, lightLon, lightLat)

    print(relativePositioning.getResult(1000, 30))