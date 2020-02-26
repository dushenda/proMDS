#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@ide        : PyCharm
@project    : hdf_pd
@file       : get_info_mxd03.py
@author     : CALIBRATION
@time       : 2020/2/22 17:02
@description: 通过MXD03数据的经纬度范围得到图像的索引点
"""
import numpy as np
from pyhdf.SD import SD, SDC
import pprint


def get_angle(path_mxd03, index):
    """

    :param path_mxd03:str 文件位置
    :param index:ndarray 位置索引
    :return:list 太阳天顶角、太阳方位角、观测天顶角、观测方位角
    """
    solar_zenith_matrix = get_mxd03_attr_matrix(path_mxd03, 'SolarZenith')
    solar_zenith_scale = get_mxd03_attr_attr(path_mxd03, 'SolarZenith', 'scale_factor')
    solar_azimuth_matrix = get_mxd03_attr_matrix(path_mxd03, 'SolarAzimuth')
    solar_azimuth_scale = get_mxd03_attr_attr(path_mxd03, 'SolarAzimuth', 'scale_factor')
    sensor_zenith_matrix = get_mxd03_attr_matrix(path_mxd03, 'SensorZenith')
    sensor_zenith_scale = get_mxd03_attr_attr(path_mxd03, 'SensorZenith', 'scale_factor')
    sensor_azimuth_matrix = get_mxd03_attr_matrix(path_mxd03, 'SensorAzimuth')
    sensor_azimuth_scale = get_mxd03_attr_attr(path_mxd03, 'SensorAzimuth', 'scale_factor')
    solar_zenith = np.mean(solar_zenith_matrix[index]) * solar_zenith_scale
    solar_azimuth = np.mean(solar_azimuth_matrix[index]) * solar_azimuth_scale
    sensor_zenith = np.mean(sensor_zenith_matrix[index]) * sensor_zenith_scale
    sensor_azimuth = np.mean(sensor_azimuth_matrix[index]) * sensor_azimuth_scale
    result = dict(SolarZenith=solar_zenith, SolarAzimuth=solar_azimuth, SensorZenith=sensor_zenith,
                  SensorAzimuth=sensor_azimuth)
    return result


def get_matrix_range(path_mxd03, position, delta):
    """

    :param path_mxd03: str mxd03文件所在位置
    :param position: tuple 地理坐标，经度和纬度
    :param delta: double 取坐标的范围
    :return: tuple 返回数值矩阵所在的索引，左下、左上、右下、右上
    """
    lon = position[0]
    lat = position[1]
    lon_min = lon - delta
    lon_max = lon + delta
    lat_min = lat - delta
    lat_max = lat + delta
    lon_matrix = get_mxd03_attr_matrix(path_mxd03, 'Longitude')
    lat_matrix = get_mxd03_attr_matrix(path_mxd03, 'Latitude')
    index = np.where((lon_matrix < lon_max) & (lon_matrix > lon_min) &
                     (lat_matrix < lat_max) & (lat_matrix > lat_min))
    return index


def get_mxd03_attr_matrix(path_mxd03, attr):
    """

    :param path_mxd03: mxd03文件所在位置
    :param attr: mxd03影像的属性
    :return: mxd影像属性对应的数据集
    """
    file = SD(path_mxd03, SDC.READ)
    sds_obj = file.select(attr)
    matrix = sds_obj.get()
    return matrix


def get_mxd03_attr_attr(path_mxd03, attr1, attr2):
    """

    :param path_mxd03:mxd03文件所在位置
    :param attr1:mxd03影像的数据集名称
    :param attr2:mxd03影像的数据集属性
    :return:属性值
    """
    file = SD(path_mxd03, SDC.READ)
    sds_obj = file.select(attr1)
    dict_attr = sds_obj.attributes()
    result = dict_attr[attr2]
    return result


def get_mxd_attr(path_mxd, attr):
    """

    :param path_mxd:mxd单个文件所在位置
    :param attr:mxd03影像的数据集名称
    :return:数据集的DN值
    """
    file = SD(path_mxd, SDC.READ)
    sds_obj = file.select(attr)
    result_dict = sds_obj.attributes()
    return result_dict


def main():
    pos = [94.32, 40.14]
    delta = 0.018
    file_path = './MOD03.A2019364.0405.061.2019364104023.hdf'
    index = get_matrix_range(file_path, pos, delta)
    angle = get_angle(file_path, index)
    # r = get_mxd03_attr_attr(file_path, 'SolarZenith', 'scale_factor')
    pprint.pprint(angle)


if __name__ == '__main__':
    main()
