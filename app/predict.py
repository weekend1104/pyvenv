# -*- coding:utf-8 -*-
import joblib,os
import tensorflow.compat.v1 as tf
import numpy as np
#import sklearn

def point_lists_change(points,rel_points):
    point_lists = [-110] * len(points)

    rel_points = rel_points["beacons"]
    for number in range(0,len(rel_points)):
        t_dict={'major':rel_points[number]['major'],'minor':rel_points[number]['minor']}
        listnumber = points.index(t_dict)
        point_lists[listnumber]=rel_points[number]['rssi']
    return point_lists

def ble_predict(x):
  
  file_path = os.path.dirname(__file__)

  scaler = joblib.load(os.path.join(file_path,'static/scalar01'))
  test_x = scaler.transform(x)
  meta_path = os.path.join(file_path,'static/Model/ann.ckpt.meta')
  with tf.Session() as sess:
    new_saver = tf.train.import_meta_graph(meta_path)
    new_saver.restore(sess, tf.train.latest_checkpoint(os.path.join(file_path,'static/Model')))
    feed_dict = {"x_:0": test_x}
    pred_y = tf.get_collection("predict")
    ble_position = sess.run(pred_y, feed_dict)[0]
  return ble_position

# test_data = [-11, -30, -110, -110, -110, -57, -110, -22, -110, -23, -110, -110, -110, -110, -110, -110, -110, -110, -50, -40]
# test_data= np.array(test_data).reshape(1, -1)
# jisuanjieguo = ble_predict(test_data)[0]
# print(jisuanjieguo)

# 输入为存有一个x坐标和1个y坐标的列表
# 输出为字符串形式的标志号
def displayboard(position):
    x1=[8.10,2.32,2.32,2.32,13.85,13.85,13.85,8.10]#室外展板X坐标  
    x2=np.array(x1)#数组化
    x3=[4.90,12.20,12.67,11.23,8.10,3.44,3.57,8.50,11.31]#室内展板X坐标
    x4=np.array(x3)
    
    y1=[13.93,12.79,8.1,3.41,12.79,8.1,3.41,2.23]#室内展板Y
    y2=np.array(y1)
    y3=[4.39,3.50,8.23,8.01,8.10,6.89,12.67,12.63,11.13]#室外展板Y
    y4=np.array(y3)
    
    position2=np.array(position)
    px=position2[0]#人的位置XY
    py=position2[1]
    
    if  px<= 2.32 or px>=13.85 or py>=13.93 or py<=2.23:#在房间外
        a_out=x2-px#x坐标差
        #print (a_out)
        b_out=y2-py#y坐标差
        #print (b_out)
        c_out=np.sqrt((a_out**2)+(b_out**2))#欧式距离
        i=np.argsort(c_out)
        #print (c_out)
        displaybroadnum='A'+str(i[0]+1)
        #print("人在室外，推送的展板号为",displaybroadnum)
        #print("人在室外,参观的展板位置为(",x2[i[0]],',',y2[i[0]],")")
        return displaybroadnum
    else:
        a_in=x4-px
        #print (a_in)
        b_in=y4-py
        #print (b_in)
        c_in=np.sqrt((a_in**2)+(b_in**2))
        i=np.argsort(c_in)#排序
        #print (c_in)
        displaybroadnum='B'+str(i[0]+1)
        #print("推送的展板号为",displaybroadnum)
        #print("人在室内，参观的展板位置为(",x4[i[0]],',',y4[i[0]],")")
        return displaybroadnum