#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@ide        : PyCharm
@project    : ImageRead
@file       : pack_assist.py
@author     : CALIBRATION
@time       : 2020/3/26 22:42
@description: None
"""
import os

dir_path = './build/exe.win-amd64-3.6/lib'
modlist = []
for _ in os.listdir(dir_path):
    file_path = os.path.join(dir_path, _)
    if os.path.isdir(file_path):
        modlist.append(_)

with open('ModuleList.txt', 'w') as f:
    f.write('[')
    for eachmod in modlist:
        f.write("'"+eachmod+"', ")
    f.write(']')
