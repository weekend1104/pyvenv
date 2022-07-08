# -*- coding:utf-8 -*-
from app import app
import os,json,joblib,random,codecs
import numpy as np
from flask import  request,jsonify
# import tensorflow.compat.v1 as tf
from .main import * 



file_path = os.path.dirname(__file__)
json_path = os.path.join(file_path,'static/points.json')

with open(json_path,'r',encoding="utf-8") as point:
    point_datas = json.load(point)
    point.close()

def list_of_groups(init_list, children_list_len):
    list_of_groups = zip(*(iter(init_list),) * children_list_len)
    end_list = [list(i) for i in list_of_groups]
    count = len(init_list) % children_list_len
    end_list.append(init_list[-count:]) if count != 0 else end_list
    return end_list

@app.route('/calculation',methods=["POST"])
def point_calculate():
    get_data=request.data.decode('utf-8')
    # 获取传入的json，转化为计算用的坐标列表

    filename = os.path.join(file_path,'test.txt')
    Notes = open(filename,mode='a')
    Notes.write(get_data)
    Notes.write('\n')
    Notes.close()

    get_data = json.loads(get_data)

    # 将计算用的坐标传入函数中计算坐标值并返回
    
    ble=Ble()
    position_x, position_y,ID = ble.run(get_data)
    location_dict = {"x":float(position_x),"y":float(position_y),"board":str(ID)}
    return  jsonify(location_dict)

@app.route('/test',methods=["GET","POST"])
def test_point():
    USERS = {
    1:{'name':'derek','age':18},
    2:{'name':'tom','age':20},
    3:{'name':'杰克','age':22},
    }
    data = json.dumps(USERS,ensure_ascii=False)
    with codecs.open(os.path.join(file_path,'data.json'),'w',encoding='utf-8') as fp:
        json.dump(USERS,fp,ensure_ascii=False)
    fp.close()
    print(__name__)
    return jsonify(USERS)

@app.route('/redirecttest',methods=["GET","POST"])
def redirectpoint():

    headers = {"location":"http://www.baidu.com"}

    return '<html></html>',301,headers


