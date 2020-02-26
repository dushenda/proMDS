#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@ide        : PyCharm
@project    : hdf_pd
@file       : 1.py
@author     : CALIBRATION
@time       : 2020/2/22 17:01
@description: 一个获取MXD021KM和MXD03的类
"""
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput
import os
import pprint
import re
import get_info_mxd021km


class ModDir:

    def __init__(self, path, position, delta):
        """

        :param path:
        :param position:
        :param delta:
        """
        self.path = path
        self.__set_dir_list()
        self.position = position
        self.delta = delta

    def __set_dir_list(self):
        """

        :return:
        """
        # path为文件所在文件夹，得到MXD021KM数据列表和MXD03数据列表
        file_all = os.listdir(self.path)
        self.mxd_21 = list(filter(lambda x: re.match('M.D021KM.*hdf', x) is not None, file_all))
        self.mxd_21 = [self.path + i for i in self.mxd_21]
        self.mxd_03 = list(filter(lambda x: re.match('M.D03.*hdf', x) is not None, file_all))
        self.mxd_03 = [self.path + i for i in self.mxd_03]

    def generate_table(self, out_path):
        """

        :param out_path:
        :return:
        """
        df = get_info_mxd021km.get_result(self.mxd_03, self.mxd_21, self.position, self.delta)
        df.to_csv(out_path)

    def get_file_nums(self):
        """

        :return:
        """
        print('总文件数:', len(self.mxd_21))

    def generate_table_scale(self, out_path):
        """

        :param out_path:
        :return:
        """
        df = get_info_mxd021km.get_result_scale(self.mxd_03, self.mxd_21, self.position, self.delta)
        df.to_csv(out_path)


def main():
    # pp = pprint.PrettyPrinter(indent=1)
    pos = [94.32, 40.14]
    delta = 0.018
    dl = ModDir('.\\', pos, delta)
    dl.get_file_nums()
    dl.generate_table_scale('./myd_scale.csv')


if __name__ == '__main__':
    gra = GraphvizOutput(output_file="a.png")
    with PyCallGraph(output=gra):
        main()
