#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@ide        : PyCharm
@project    : hdf_pd
@file       : get_info_mxd021km.py
@author     : CALIBRATION
@time       : 2020/2/23 0:30
@description: None
"""
import get_info_mxd03
import pprint
import numpy as np
import pandas as pd
import os
import datetime


def get_result_scale(path_mxd03_list, path_mxd02_list, position, delta):
    """

    :param path_mxd03_list:mxd03文件所在路径
    :param path_mxd02_list:mxd02文件所在路径
    :param position:经纬度
    :param delta:经纬度偏移量
    :return:DataFrame格式的数据，影像中获取的定标系数
    """
    columns_names = ['DateTime', 'Longitude', 'Latitude', 'SolarZenith', 'SolarAzimuth', 'SensorZenith',
                     'SensorAzimuth', 'ref_1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                     '11', '12', '13lo', '13hi', '14lo', '14hi', '15', '16', '17', '18',
                     '19', '26', 'rad_1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                     '11', '12', '13lo', '13hi', '14lo', '14hi', '15', '16', '17', '18',
                     '19', '26']
    df = pd.DataFrame(columns=columns_names)
    for i, path_mxd03, path_mxd02 in zip(range(len(path_mxd03_list)), path_mxd03_list, path_mxd02_list):
        index = get_info_mxd03.get_matrix_range(path_mxd03, position, delta)
        if index[0].size == 0:
            continue
        dict_angles = get_info_mxd03.get_angle(path_mxd03, index)
        list_scale = get_band_scales(path_mxd02)
        date_time = get_date_time(path_mxd02)
        cont_list = position + list(dict_angles.values()) + list_scale
        cont_list.insert(0, date_time)
        df.loc[i] = cont_list
    return df


def get_result(path_mxd03_list, path_mxd02_list, position, delta):
    """

    :param path_mxd03_list:mxd03文件所在路径
    :param path_mxd02_list:mxd02文件所在路径
    :param position:经纬度
    :param delta:经纬度偏移量
    :return:DataFrame格式的数据，影像中获取的DN值
    """
    columns_names = ['DateTime', 'Longitude', 'Latitude', 'SolarZenith', 'SolarAzimuth', 'SensorZenith',
                     'SensorAzimuth', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                     '11', '12', '13lo', '13hi', '14lo', '14hi', '15', '16', '17', '18',
                     '19', '26']
    df = pd.DataFrame(columns=columns_names)

    for i, path_mxd03, path_mxd02 in zip(range(len(path_mxd03_list)), path_mxd03_list, path_mxd02_list):
        index = get_info_mxd03.get_matrix_range(path_mxd03, position, delta)
        if index[0].size == 0:
            continue
        dict_angles = get_info_mxd03.get_angle(path_mxd03, index)
        dict_band_dn = get_band_dn(path_mxd02, index)
        # list_band_names = get_band_names(path_mxd02)
        date_time = get_date_time(path_mxd02)
        cont_list = position + list(dict_angles.values()) + dict_band_dn['dn_ref_sb250_rad'].tolist() + \
                    dict_band_dn['dn_ref_sb500_rad'].tolist() + dict_band_dn['dn_ref_sb_rad'].tolist()
        cont_list.insert(0, date_time)
        df.loc[i] = cont_list
    return df


def get_date_time(path_mxd021km):
    """

    :param path_mxd021km:mxd02单个文件路径
    :return:时间数据
    """
    file_name = os.path.basename(path_mxd021km)
    yyyy = file_name[10:14]
    ddd = file_name[14:17]
    # 这个是UTC Time，要转换为BJT
    hh = file_name[18:20]
    hh_int = int(hh) + 8
    hh = str(hh_int)
    mm = file_name[20:22]
    dt_str = yyyy + ddd + hh + mm
    dt = datetime.datetime.strptime(dt_str, "%Y%j%H%M")
    dt_str_out = dt.strftime("%Y-%m-%d %H:%M:%S")
    return dt_str_out


def get_band_names(path_mxd021km):
    """

    :param path_mxd021km: mxd02单个文件路径
    :return: list 太阳波段名称
    """
    dict_ref_sb_band_names = get_info_mxd03.get_mxd03_attr_attr(path_mxd021km, 'EV_1KM_RefSB', 'band_names')
    dict_ref_sb250_band_names = get_info_mxd03.get_mxd03_attr_attr(path_mxd021km, 'EV_250_Aggr1km_RefSB', 'band_names')
    dict_ref_sb500_band_names = get_info_mxd03.get_mxd03_attr_attr(path_mxd021km, 'EV_500_Aggr1km_RefSB', 'band_names')
    result = dict_ref_sb250_band_names.split(',') + dict_ref_sb500_band_names.split(',') + dict_ref_sb_band_names.split(
        ',')
    return result


def get_band_scales(path_mxd021km):
    """

    :param path_mxd021km:mxd02单个文件路径
    :return:定标系数
    """
    dict_ref_sb_band_scales = get_info_mxd03.get_mxd03_attr_attr(path_mxd021km, 'EV_1KM_RefSB', 'reflectance_scales')
    dict_ref_sb250_band_scales = get_info_mxd03.get_mxd03_attr_attr(path_mxd021km, 'EV_250_Aggr1km_RefSB',
                                                                    'reflectance_scales')
    dict_ref_sb500_band_scales = get_info_mxd03.get_mxd03_attr_attr(path_mxd021km, 'EV_500_Aggr1km_RefSB',
                                                                    'reflectance_scales')
    dict_rad_sb_band_scales = get_info_mxd03.get_mxd03_attr_attr(path_mxd021km, 'EV_1KM_RefSB', 'radiance_scales')
    dict_rad_sb250_band_scales = get_info_mxd03.get_mxd03_attr_attr(path_mxd021km, 'EV_250_Aggr1km_RefSB',
                                                                    'radiance_scales')
    dict_rad_sb500_band_scales = get_info_mxd03.get_mxd03_attr_attr(path_mxd021km, 'EV_500_Aggr1km_RefSB',
                                                                    'radiance_scales')
    result1 = dict_ref_sb250_band_scales + dict_ref_sb500_band_scales + dict_ref_sb_band_scales
    result2 = dict_rad_sb250_band_scales + dict_rad_sb500_band_scales + dict_rad_sb_band_scales
    result = result1 + result2
    return result


def get_band_dn(path_mxd021km, index):
    """

    :param path_mxd021km: 1km分辨率影像文件路径（mxd02km）
    :param index: 索引点
    :return: 太阳波段dn值平均
    """
    ref_sb_matrix = get_info_mxd03.get_mxd03_attr_matrix(path_mxd021km, 'EV_1KM_RefSB')
    ref_sb_dict_attr = get_info_mxd03.get_mxd_attr(path_mxd021km, 'EV_1KM_RefSB')
    ref_sb250_matrix = get_info_mxd03.get_mxd03_attr_matrix(path_mxd021km, 'EV_250_Aggr1km_RefSB')
    ref_sb250_dict_attr = get_info_mxd03.get_mxd_attr(path_mxd021km, 'EV_250_Aggr1km_RefSB')
    ref_sb500_matrix = get_info_mxd03.get_mxd03_attr_matrix(path_mxd021km, 'EV_500_Aggr1km_RefSB')
    ref_sb500_dict_attr = get_info_mxd03.get_mxd_attr(path_mxd021km, 'EV_500_Aggr1km_RefSB')
    ref_sb_ref = np.mean(ref_sb_matrix[:, index[0], index[1]], axis=1) - ref_sb_dict_attr['reflectance_offsets']
    ref_sb_rad = np.mean(ref_sb_matrix[:, index[0], index[1]], axis=1) - ref_sb_dict_attr['radiance_offsets']
    ref_sb250_ref = np.mean(ref_sb250_matrix[:, index[0], index[1]], axis=1) - ref_sb250_dict_attr[
        'reflectance_offsets']
    ref_sb250_rad = np.mean(ref_sb250_matrix[:, index[0], index[1]], axis=1) - ref_sb250_dict_attr['radiance_offsets']
    ref_sb500_ref = np.mean(ref_sb500_matrix[:, index[0], index[1]], axis=1) - ref_sb500_dict_attr[
        'reflectance_offsets']
    ref_sb500_rad = np.mean(ref_sb500_matrix[:, index[0], index[1]], axis=1) - ref_sb500_dict_attr['radiance_offsets']
    result = dict(dn_ref_sb_ref=ref_sb_ref, dn_ref_sb_rad=ref_sb_rad, dn_ref_sb250_ref=ref_sb250_ref,
                  dn_ref_sb250_rad=ref_sb250_rad, dn_ref_sb500_ref=ref_sb500_ref, dn_ref_sb500_rad=ref_sb500_rad)
    return result


def main():
    pos = [94.32, 40.14]
    delta = 0.018
    path_mxd03 = ['./MOD03.A2019364.0405.061.2019364104023.hdf']
    path_mxd02 = ['./MOD021KM.A2019364.0405.061.2019364130814.hdf']
    get_result(path_mxd03, path_mxd02, pos, delta)


if __name__ == '__main__':
    main()
