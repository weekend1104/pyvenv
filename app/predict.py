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

