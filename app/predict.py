# -*- coding:utf-8 -*-
"""
project: pythonProject1
file: predict
author: Yujin
create date: 2022/6/21 14:50
description: 
"""
import os
import numpy as np
from scipy.signal import savgol_filter
import joblib
from .mapmatching import Mapmatching
from .displayboard import display
from .connect_sql import Mysql


class Core(object):
  def __init__(self):
    self.scaler = joblib.load(os.path.join(os.path.dirname(__file__),'static/scalar_both'))
    self.reg_fit = joblib.load(os.path.join(os.path.dirname(__file__),'static/K Nearest Neighbor_both.pkl'))
    self.model = joblib.load(os.path.join(os.path.dirname(__file__),'static/cluster_both.pkl'))

  def predict(self,test_feature,userId,model_name):
    mysql = Mysql(userId)
    length = len(test_feature)
    cluster_result  =[]
    for i in range(length):
      test_x = np.array(test_feature.iloc[i,:]).reshape(1, -1)
      cluster_result.append(self.model.predict(test_x))
      test_x = self.scaler.transform(test_x)
      prediction = self.reg_fit.predict(test_x)
      temp_position_x = prediction[0,0]
      temp_position_y = prediction[0,1]
      mysql.insertdata(temp_position_x,temp_position_y)
    count_num1 = mysql.getdatalen()
    
    if count_num1 <= 100:
        position_both = mysql.getdata()
    else:
        start = count_num1 -100
        position_both = mysql.getgapdata(start,count_num1)



   # if count_num1 >= 100:
    #  mysql.deletedata()
   # position_both = mysql.getdata()
    position_both_arry = np.array(position_both)
    position_x_list = position_both_arry[:, 0].tolist()
    position_y_list = position_both_arry[:, 1].tolist()
    num = 41
    smooth_x = savgol_filter(position_x_list, num, 2, mode='nearest')
    smooth_y = savgol_filter(position_y_list, num, 2, mode='nearest')

    mapmatching = Mapmatching()
    project_x, project_y = mapmatching.project(smooth_x[-1], smooth_y[-1], cluster_result[-1], model_name)


    ID = display(project_x, project_y, cluster_result[-1], model_name)

    return project_x, project_y, ID





