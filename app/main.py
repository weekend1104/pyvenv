# -*- coding:utf-8 -*-
"""
project: pythonProject1
file: main
author: Yujin
create date: 2022/6/21 14:47
description: 
"""
import json

import numpy as np
import pandas as pd
from .predict import Core


class Ble(object):
  def run(self,data):
    test_feature = pd.DataFrame(columns=['1055', '1060', '1087', '1075', '1037', '1051', '1067', '1046', '1041',
                                         '1053', '1058', '1092', '1088', '1066', '1036', '1063', '1070', '1050', '1073',
                                         '1045', '1034', '1061',
                                         '1082', '1076', '1042', '1068', '1054', '1080', '1086', '1062', '1040', '1089',
                                         '1052', '1057', '1047',
                                         '1081', '1074', '1064', '1072', '1091', '1090', '1038', '1084', '1078', '1085',
                                         '1033','ts'],dtype=object)
    AP = [1055,1060,1087,1075,1037,1051,1067,1046,1041,1053,1058,1092,1088,1066,1036,1063,1070,1050,1073,1045,1034,1061,
    1082,1076,1042,1068,1054,1080,1086,1062,1040,1089,1052,1057,1047,1081,1074,1064,1072,1091,1090,1038,1084,1078,1085,1033]

    n = 0
    bl_data = data['beacons']
    length = len(bl_data)
    rssi_temp = np.zeros((47, 1))
    ts_initial = bl_data[0]['ts']
    for i in range(0, length):
        if bl_data[i]['ts'] == ts_initial:
            for j in range(46):
                if bl_data[i]['minor'] == AP[j]:
                    rssi_temp[j] = bl_data[i]['rssi']
                    rssi_temp[46] = bl_data[i]['ts']
                    ts_initial = bl_data[i]['ts']
                    break
        else:
            rssi_list = rssi_temp.reshape(1, -1).tolist()
            test_feature.loc[n] = rssi_list[0]
            n = n + 1
            rssi_temp = np.zeros((47, 1))
            for j in range(46):
                if bl_data[i]['minor'] == AP[j]:
                    rssi_temp[j] = bl_data[i]['rssi']
                    rssi_temp[46] = bl_data[i]['ts']
                    ts_initial = bl_data[i]['ts']
                    break

    rssi_list = rssi_temp.reshape(1, -1).tolist()
    test_feature.loc[n] = rssi_list[0]

    test_feature_bool = (test_feature == 0)
    test_feature_bool_sum = test_feature_bool.sum(axis = 1)
    length = len(test_feature)
    id = []
    for i in range(length-1):
      if (test_feature_bool_sum[0] > 40) :
        id.append(i)
    test_feature = test_feature.drop(id)
    test_feature = test_feature.drop(columns='ts')
    test_feature.fillna(value=-105, inplace=True)
    test_feature.replace(0, -105, inplace=True)
    '''到此为止，输入的json格式数据被转为(n,46)的dataframe。实际定位时，每m秒传入的数据会被整合成这个形式'''
    core = Core()
    userId = data['uid']
    model_name = data['path']
    position_x, position_y, ID = core.predict(test_feature,userId,model_name)
    return position_x, position_y,ID


# if __name__ == '__main__':

# #-----------------------------------------------------------------------#
#     '''目前是读取离线txt格式的数据,模拟在线情况，用于测试'''
#     # core = Core()
#     # file_name = 'test.txt'
#     # in_file = open(file_name)
#     # json_str = in_file.read()
#     # Data = json.loads(json_str)
#     # ble = Ble()
#     # position_x, position_y,ID = ble.run(Data)
#     # print(position_x)#单个数据
#     # print(position_y)
#     # print(ID)#ID就是各个展板的编号，类型是字符串。

# #-----------------------------------------------------------------------#
#     # '''之后在线应用时采用下面这种写法，读取的是发来的一段一段的json数据，保存到json_str中'''
#     core = Core()
#     Data = json.loads(json_str)  # data是一个列表，每个元素时一个字典，分别为每次蓝牙和惯性器件对应的数据。
#     ble = Ble()
#     position_x, position_y,ID = ble.run(Data)
#     print(position_x)  # 单个数据
#     print(position_y)
#     print(ID)  # ID就是各个展板的编号，类型是字符串。
