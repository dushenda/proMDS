# proMDS 工具

![](D:\CodePycharm\PySide\ImageRead\.images_readme\earth1.bmp)`

proMDS`是一个用来批量提取文件夹里面`MODIS`影像太阳光波段的平均`DN`值、定标系数的工具。

## 用法

#### 输入

- 待提取的文件夹路径，文件夹应该包括一一对应的`mxd02`和`mxd03`的文件序列，数目应该相同
- 待输出的文件路径，`.csv`格式
- 提取位置的经纬度和小正方形的1/2边长（Δ）

#### 输出

- 输出为提取的文件数据

#### 运行界面

![](D:\CodePycharm\PySide\ImageRead\.images_readme\运行界面.jpg)

## 实现逻辑