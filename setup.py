#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@ide        : PyCharm
@project    : ImageRead
@file       : setup.py.py
@author     : CALIBRATION
@time       : 2020/2/24 15:01
@description: None
"""
import sys
from cx_Freeze import setup, Executable

path = sys.path + ['C:\\ProgramData\\Anaconda3\\envs\\pysideEnv36\\Library\\bin',
                   'C:\\ProgramData\\Anaconda3',
                   'C:\\ProgramData\\Anaconda3\\Scripts',
                   'C:\\ProgramData\\Anaconda3\\Library\\bin']
# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os", 'pyhdf', 'PySide2', 'numpy'], "excludes": ["tkinter"], "path": path}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

icon_path = './.images/alpha.ico'

setup(name="proMDS",
      version='1.0',
      description='A tool get data from MXD02&MXD03',
      author='dushenda',
      author_email='dushenda@outlook.com',
      options={"build_exe": build_exe_options},
      executables=[Executable("main.py", base=base, icon=icon_path, targetName="proMDS")]
      )
