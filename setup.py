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

path = sys.path
packages = ["os", 'pyhdf']
include_files = ['.ui', '.images']
# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": packages,
    "excludes": ["tkinter"],
    "path": path,
    "include_files": include_files}

company_name = 'AIOFM'
product_name = 'proMOS'
upgrade_code = '{66620F3A-DC3A-11E2-B341-002219E9B01E}'
bdist_msi_options = {
    'upgrade_code': upgrade_code,
    'add_to_path': False,
    'initial_target_dir': r'[ProgramFilesFolder]\%s\%s' % (company_name, product_name),
    'target_name': 'setupMDS'
}


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
      options={"build_exe": build_exe_options,
               "bdist_msi": bdist_msi_options},
      executables=[Executable("main.py", base=base, icon=icon_path, targetName="proMDS")]
      )
