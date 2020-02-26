#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@ide        : PyCharm
@project    : Image_Read
@file       : main.py
@author     : CALIBRATION
@time       : 2020/2/23 21:03
@description: None
"""
import os
import get_info_modis
from PySide2.QtGui import QPixmap, QIcon
from PySide2.QtWidgets import QApplication, QFileDialog, QProgressDialog, QMessageBox
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import Qt
from threading import Thread


class InfoWindow:
    def __init__(self, parent):
        """

        :param parent: 父窗口对象
        """
        self.info_dlg = QUiLoader(parent=parent).load("./.ui/info.ui")
        self.info_dlg.setWindowModality(Qt.ApplicationModal)
        icon_window = QIcon("./.images/tree.ico")
        self.info_dlg.setWindowIcon(icon_window)


class Stats:

    def __init__(self):

        # 加载UI
        self.ui = QUiLoader().load('./.ui/main.ui')
        self.chdWnd = InfoWindow(self.ui)
        # 初始化
        self.init_content()

        # 私有变量
        self.in_path = self.ui.lineEdit_in_dir.text() + '\\'
        self.out_path = self.ui.lineEdit_out_file.text()
        lon = float(self.ui.lineEdit_lon.text())
        lat = float(self.ui.lineEdit_lat.text())
        self.pos = [lon, lat]
        self.delta = float(self.ui.lineEdit_delta.text())

        # 信号与槽
        self.ui.pushButton_in_dir.clicked.connect(self.get_dir)
        self.ui.pushButton_out_file.clicked.connect(self.set_file)
        self.ui.pushButton_cal_dn.clicked.connect(lambda: self.show_psg(self.cal_dn_thd))
        self.ui.pushButton_cal_scales.clicked.connect(lambda: self.show_psg(self.cal_scales_thd))
        self.ui.pushButton_info.clicked.connect(self.info)

    def cal_dn_thd(self, progress):
        """

        调用ModDir.generate_table函数，得到DN值平均
        :param progress:线程对象
        :return:None
        """
        # 新建线程提取DN值
        self.refresh_attr()
        dl = get_info_modis.ModDir(self.in_path, self.pos, self.delta)
        dl.generate_table(self.out_path)
        progress.cancel()

    def cal_scales_thd(self, progress):
        """

        调用ModDir.generate_table_scales函数，得到定标系数
        :param progress:线程对象
        :return:None
        """
        # 新建线程提取定标系数
        self.refresh_attr()
        dl = get_info_modis.ModDir(self.in_path, self.pos, self.delta)
        dl.generate_table_scale(self.out_path)
        progress.cancel()

    def info(self):
        """

        产生说明窗口
        :return:None
        """
        # 说明窗口
        self.chdWnd.info_dlg.show()

    def get_dir(self):
        """
        输入文件夹路径获取按钮槽函数
        :return:None
        """
        # 输入文件夹设置
        dir_path = QFileDialog.getExistingDirectory(parent=self.ui, caption="输入文件夹路径", dir="./")
        if dir_path != '':
            self.ui.lineEdit_in_dir.setText(dir_path)

    def set_file(self):
        """
        输出文件路径设置槽函数
        :return:None
        """
        # 指定输出文件
        file_tuple = QFileDialog.getSaveFileName(parent=self.ui, caption="保存文件路径", str='./out.csv',
                                                 filter='文本文件(*.csv)')
        file_path = file_tuple[0]
        if file_path != '':
            self.ui.lineEdit_out_file.setText(file_path)

    def init_content(self):
        """
        初始化函数
        :return:None
        """
        # 初始化
        self.ui.setWindowIcon(QIcon("./.images/tree.ico"))
        title_img = QPixmap("./.images/alpha.png")
        self.ui.label_7.setPixmap(title_img)
        self.ui.lineEdit_in_dir.setText(os.path.abspath('./'))
        self.ui.lineEdit_out_file.setText(os.path.abspath('./') + '\\out.csv')
        self.ui.lineEdit_lon.setText('94.32')
        self.ui.lineEdit_lat.setText('40.14')
        self.ui.lineEdit_delta.setText('0.018')

    def refresh_attr(self):
        """
        更新获取信息（主要更新路径信息）
        :return:None
        """
        # 关联控件与变量的值
        self.in_path = self.ui.lineEdit_in_dir.text() + '\\'
        self.out_path = self.ui.lineEdit_out_file.text()
        lon = float(self.ui.lineEdit_lon.text())
        lat = float(self.ui.lineEdit_lat.text())
        self.pos = [lon, lat]
        self.delta = float(self.ui.lineEdit_delta.text())

    def show_psg(self, target):
        """
        显示进度条窗口
        :param target:线程处理函数
        :return:None
        """
        # 进度条
        progress = QProgressDialog(parent=self.ui, maximum=0, minimum=0, cancelButtonText="取消",
                                   labelText="正在提取...", flags=Qt.WindowFlags())
        progress.setWindowTitle("提取数据")
        run_psg_thd = Thread(target=target, args=(progress,))
        run_psg_thd.start()
        progress.exec_()
        self.show_finish()

    def show_finish(self):
        """
        完成显示信息窗口
        :return:None
        """
        # 提取数据完成窗口
        QMessageBox.information(self.ui, "信息", "数据提取成功！", QMessageBox.Ok)


app = QApplication([])
stats = Stats()
stats.ui.show()
app.exec_()
