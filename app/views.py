from app import app
import os,json,joblib
import numpy as np
from flask import  request,jsonify
import tensorflow.compat.v1 as tf
from app.predict import * # 导入predict.py，内有转换json坐标与计算坐标的函数



file_path = os.path.dirname(__file__)
json_path = os.path.join(file_path,'static/points.json')

with open(json_path,'r',encoding="utf-8") as point:
    point_datas = json.load(point)
    point.close()

@app.route('/calculation',methods=["POST"])
def point_calculate():
    get_data=request.data.decode('utf-8')

    # 获取传入的json，转化为计算用的坐标列表
    get_data = json.loads(get_data)
    point_list = point_lists_change(point_datas,get_data)

    print(point_list)

    # 将计算用的坐标传入函数中计算坐标值并返回
    points= np.array(point_list).reshape(1, -1)
    point_lists = ble_predict(points)[0]
    test_dict = {"x":float(point_lists[0]),"y":float(point_lists[1])}

    return  jsonify(test_dict)


