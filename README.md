# proMDS 工具

![](.images_readme/earth1.bmp)

`proMDS`是一个用来批量提取文件夹里面`MODIS`影像太阳光波段的平均`DN`值、定标系数的工具

## 用法

#### 输入

- 待提取的文件夹路径，文件夹应该包括一一对应的`mxd02`和`mxd03`的文件序列，数目应该相同
- 待输出的文件路径，`.csv`格式
- 提取位置的经纬度和小正方形的1/2边长(Δ)

#### 输出

- 输出为提取的文件数据

#### 运行界面

![](.images_readme/运行界面.jpg)

## 实现逻辑

#### 类

主要的类为`ModDir`，`UML`图如下

![](.images_readme/ModDir.jpg)

#### 调用关系

![](.images_readme/调用关系.png)

## API文档

运行代码文件有3个：`get_info_modis.py`、`get_info_mxd03.py`、`get_info_mxd021km.py`

界面代码文件有1个：`main.py`

ui文件有两个：`main.ui`、`info.ui`位于`.ui`文件夹内

### get_info_modis

![](.images_readme/ModDir.jpg)

#### 属性

- delta：小正方形边长的1/2
- mxd_03：mxd03文件的列表
- mxd_21：mxd21km文件的列表
- path：文件所在路径
- position：[经度，纬度]（°）

#### 方法

- generate_table()：输出DN值文件
- generate_table_scale()：输出定标系数的文件
- get_file_nums()：输出文件的数目