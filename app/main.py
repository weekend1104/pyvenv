import copy,json,os
from math import sin, cos, ceil
import cv2
import numpy as np
import pandas as pd


class Worker():
  def __init__(self):
    self.sensor_data_process = []
    self.frequency = 20
    self.delta_time = 0.06
    self.map_matching = MapMatching()
    self.min_acceleration = 0.2
    self.max_acceleration = 2
    self.min_interval = 0.4
    self.slide = 7
    self.temp_t = 0.0
    return

  def Run(self,data):
    self.current_pose = Quaternion()
    temp_data_buffer = []
    buffer_size = 0
    buffer_size_max = 40
    acc = data['accelerometer']
    gyo = data['gyroscope']

    for i in range (len(acc)):
      temp_data = []
      temp_data.append(float(acc[i]['x']))
      temp_data.append(float(acc[i]['y']))
      temp_data.append(float(-acc[i]['z']))
      temp_data.append(float(acc[i]['ts']))
      temp_data.append(float(gyo[i]['x']))
      temp_data.append(float(gyo[i]['y']))
      temp_data.append(float(-gyo[i]['z']))
      temp_data.append(float(gyo[i]['ts']))
      temp_data_buffer.extend(temp_data)
      buffer_size +=1
      if buffer_size > buffer_size_max:
        self.sensor_data_process.extend(temp_data_buffer)
        position = self.StepDection()
        temp_data_buffer = []
        buffer_size = 0
    if position is None:
      return
    else:
      return position

  def StepDection(self):
    data_process = self.sensor_data_process

    data_length = len(data_process) //8
    if data_length < 40:
      return

    acc_norm = []
    acc_norm_t = []
    gyr_t = []
    for i in range(data_length):
      acc_norm.append(
        math.sqrt(data_process[i * 8 + 0] ** 2 + data_process[i * 8 + 1] ** 2 + data_process[i * 8 + 2] ** 2)-1
      )
      acc_norm_t.append(data_process[i*8+3])
      gyr_t.append(data_process[i * 8 + 7])

    steps = []
    peak = {'index': 0, 'acceleration': 0}

    for i,v in enumerate(acc_norm):
      if v >= peak['acceleration'] and v >= self.min_acceleration and v <= self.max_acceleration:
        peak['acceleration'] = v
        peak['index'] = i
      if i % self.slide == 0 and peak['index'] < 5:
        peak = {'index': 0, 'acceleration': 0}
      if i % self.slide == 0 and peak['index'] > 5:
        steps.append(peak)
        peak = {'index': 0, 'acceleration': 0}

    if len(steps) > 0:
      lastStep = steps[0]
      dirty_points = []
      for key, step_dict in enumerate(steps):
        if key ==0:
          continue
        if (acc_norm_t[step_dict['index']] - acc_norm_t[lastStep['index']]) / 1000 < self.min_interval:
          if step_dict['acceleration'] <= lastStep['acceleration']:
            dirty_points.append(key)
          else:
            lastStep = step_dict
            dirty_points.append(key - 1)
        else:
          lastStep = step_dict

      counter = 0
      for key in dirty_points:
        del steps[key - counter]
        counter = counter + 1
    current_pose = self.current_pose
    if len(steps) > 0:
      index = []
      yaw = []
      for key, step_dict in enumerate(steps):
        index.append(step_dict['index'])
      for i in range(0,steps[-1]['index']+1):
        if i in index:
          current_pose.Update(data_process[i * 8 + 6], gyr_t[i], self.temp_t)
          yaw.append(current_pose.get_yaw())
          if i == index[-1]:

            position = self.StepDisplacement(steps, acc_norm, yaw)
        else:
          current_pose.Update(data_process[i * 8 + 6],gyr_t[i],self.temp_t)
          self.temp_t = gyr_t[i]
      data_process = data_process[((steps[-1]['index']+1) * 8):]

    self.sensor_data_process = data_process
    if len(steps) > 0:
      return position
    else:
      return

  def StepDisplacement(self, steps, acc_normal,yaw):
    index_test = []
    value_test = []
    step_length = []
    position = {}
    for v in steps:
      index_test.append(v['index'])
      value_test.append(v['acceleration'])
    for j in range(0, len(steps)):
      if j == 0:
        acc_min = min(acc_normal[0:index_test[j]])
        step_length_temp = (0.7 * np.sqrt(np.sqrt(value_test[j] - acc_min)))
        step_length.append(step_length_temp)
      else:
        acc_min = min(acc_normal[index_test[j - 1]:index_test[j]])
        step_length_temp = (0.7 * np.sqrt(np.sqrt(value_test[j] - acc_min)))
        step_length.append(step_length_temp)

    position = self.map_matching.Update(step_length,yaw)
    return position

import math



class Quaternion(object):
  def __init__(self):

    self.yaw = 0.0
    return

  def Update(self,gz, current_t,last_t):
    delta_t = (current_t - last_t)/1000
    if last_t == 0:
      self.yaw += gz * 0.06
    else:
      self.yaw += gz * delta_t
    if self.yaw >= 2*math.pi:
      self.yaw -= 2*math.pi
    if self.yaw < 0:
      self.yaw += 2*math.pi
    return

  def get_yaw(self):
    return self.yaw


class Node(object):
  def __init__(self, _id, _layer, _x, _y):
    self.id = _id
    self.layer = _layer
    self.x = _x
    self.y = _y

    return

class Link(object):
  def __init__(self, _id, _type, _node0, _node1):
    self.id = _id
    self.type = _type
    self.layer = _node0.layer
    self.node0 = _node0
    self.node1 = _node1

    return

class Arrow(object):
  def __init__(self, _id, _type, _node0, _node1):
    self.id = _id
    self.type = _type
    self.layer = _node0.layer
    self.node0 = _node0
    self.node1 = _node1

    return

class MapMatching():
  def __init__(self):
    map_path = os.path.dirname(__file__)
    map_path = os.path.join(map_path,'map\\')
    map_filename = 'core.txt'

    # map_path = 'map\\'
    # map_filename = 'core.txt'

    self.floor_number = 1
    self.map_images = []
    self.floor_height = 5.0
    self.start_floor = 0
    self.node_filename = None
    self.link_filename = None
    self.arrow_filename = None
    self.polygon_filename = None

    in_file = open(os.path.join(map_path,map_filename), 'r')
    # in_file = open(map_path + map_filename, 'r')
    in_file.readline()
    for tLine in in_file.readlines():
      tSeq = tLine.split(',')
      if len(tSeq) < 1:
        continue
      if tSeq[0] == 'floor':
        self.floor_number = int(tSeq[1])
        for i in range(self.floor_number):
          self.map_images.append(
            cv2.imread(
              map_path + tSeq[i + 2].split('\n')[0]
            )
          )
      elif tSeq[0] == 'height':
        self.floor_height = float(tSeq[1])
      elif tSeq[0] == 'start':
        self.start_floor = int(tSeq[1])
      elif tSeq[0] == 'node':
        self.node_filename = tSeq[1].split('\n')[0]
      elif tSeq[0] == 'link':
        self.link_filename = tSeq[1].split('\n')[0]
      elif tSeq[0] == 'arrow':
        self.arrow_filename = tSeq[1].split('\n')[0]
      elif tSeq[0] == 'polygon':
        self.polygon_filename = tSeq[1].split('\n')[0]
    in_file.close()

    self.current_floor = self.start_floor
    self.view_particle = True
    self.window_name = 'Current Position'

    self.map_width = self.map_images[0].shape[1]
    self.map_height = self.map_images[0].shape[0]

    self.nodes = {}
    self.links = []
    self.arrows = []
    self.polygon_zone = []
    for i in range(self.floor_number):
      self.links.append([])
      self.arrows.append([])
      self.polygon_zone.append(
        np.ones(
          (self.map_height, self.map_width, 1),
          dtype=np.uint8
        ) * 255
      )

    if self.node_filename is None:
      print('Error: node file is None...')
      return
    in_file = open(map_path + self.node_filename, 'r')
    in_file.readline()
    for tLine in in_file.readlines():
      tSeq = tLine.split(',')
      if len(tSeq) < 1:
        continue
      tNode = Node(
        int(tSeq[0]),
        int(tSeq[1]),
        float(tSeq[2]),
        float(tSeq[3])
      )
      self.nodes[tNode.id] = tNode
    in_file.close()

    if self.link_filename is None:
      print('Error: link file is None...')
    in_file = open(map_path + self.link_filename, 'r')
    in_file.readline()
    for tLine in in_file.readlines():
      tSeq = tLine.split(',')
      if len(tSeq) < 1:
        continue
      tLink = Link(
        int(tSeq[0]),
        int(tSeq[1]),
        self.nodes[int(tSeq[2])],
        self.nodes[int(tSeq[3])]
      )
      self.links[tLink.layer].append(tLink)
    in_file.close()

    if self.arrow_filename is None:
      print('Error: arrow file is None...')
    in_file = open(map_path + self.arrow_filename, 'r')
    in_file.readline()
    for tLine in in_file.readlines():
      tSeq = tLine.split(',')
      tArrow = Arrow(
        int(tSeq[0]),
        int(tSeq[1]),
        self.nodes[int(tSeq[2])],
        self.nodes[int(tSeq[3])]
      )
      self.arrows[tArrow.layer].append(tArrow)
    in_file.close()

    if self.polygon_filename is None:
      print('Error: polygon file is None...')

    in_file = open(map_path + self.polygon_filename, 'r')
    in_file.readline()
    for tLine in in_file.readlines():
      tSeq = tLine.split(',')
      temp_type = int(tSeq[1])
      if temp_type != 1:
        continue
      temp_node_number = int(tSeq[2])
      temp_points = []
      temp_layer = None
      for i in range(temp_node_number):
        tNode = self.nodes[int(tSeq[i + 3])]
        temp_points.append((int(tNode.x), int(tNode.y)))
        temp_layer = tNode.layer
      temp_points_array = np.array([temp_points], dtype=np.int32)
      cv2.fillPoly(self.polygon_zone[temp_layer], temp_points_array, temp_type)
    in_file.close()

    in_file = open(map_path + self.polygon_filename, 'r')
    in_file.readline()
    for tLine in in_file.readlines():
      tSeq = tLine.split(',')
      temp_type = int(tSeq[1])
      if temp_type == 1:
        continue
      temp_node_number = int(tSeq[2])
      temp_points = []
      temp_layer = None
      for i in range(temp_node_number):
        tNode = self.nodes[int(tSeq[i + 3])]
        temp_points.append((int(tNode.x), int(tNode.y)))
        temp_layer = tNode.layer
      temp_points_array = np.array([temp_points], dtype=np.int32)
      cv2.fillPoly(self.polygon_zone[temp_layer], temp_points_array, temp_type)
    in_file.close()

    self.start_x = 463
    self.start_y = 229
    self.current_position_x = self.start_x
    self.current_position_y = self.start_y
    self.particle_number_max = 1000


    self.Xmin = 196
    self.Xmax = 1111
    self.Ymax = 936
    self.Ymin = 21

    self.P = np.zeros((2, self.particle_number_max))
    self.star = 1

  def CheckParticleSteps(self, Xp1, Xp2):
    particle_x = Xp1[0]
    particle_y = Xp1[1]
    current_x = Xp2[0]
    current_y = Xp2[1]

    for tLink in self.links[self.current_floor]:
      tNode0 = tLink.node0
      tNode1 = tLink.node1
      temp_hit, temp_t, temp_s = self.Intersect(particle_x, particle_y, current_x, current_y, tNode0.x, tNode0.y,
                                                tNode1.x, tNode1.y)
      if temp_hit:
        return False
    return True

  def Intersect(self, _x0, _y0, _x1, _y1, _x2, _y2, _x3, _y3):
    if not self.IntersectBase(_x0, _y0, _x1, _y1, _x2, _y2, _x3, _y3):
      return False, -1.0, -1.0

    s_x_0 = _x1 - _x0
    s_y_0 = _y1 - _y0
    s_x_1 = _x3 - _x2
    s_y_1 = _y3 - _y2

    determinant = s_x_0 * s_y_1 - s_x_1 * s_y_0
    threshold = 0.0001
    if abs(determinant) < threshold:
      return False, -1.0, -1.0

    s = (s_x_0 * (_y0 - _y2) - s_y_0 * (_x0 - _x2)) / determinant
    if s < 0.0 or s > 1.0:
      return False, -1.0, -1.0

    t = (s_x_1 * (_y0 - _y2) - s_y_1 * (_x0 - _x2)) / determinant
    if t < 0.0 or t > 1.0:
      return False, -1.0, -1.0

    return True, t, s

  def IntersectBase(self, _x0, _y0, _x1, _y1, _x2, _y2, _x3, _y3):
    threshold = 0.1

    mid_x_0 = (_x0 + _x1) * 0.5
    mid_y_0 = (_y0 + _y1) * 0.5
    mid_x_1 = (_x2 + _x3) * 0.5
    mid_y_1 = (_y2 + _y3) * 0.5

    if (abs(mid_x_1 - mid_x_0) > abs(_x1 - mid_x_0) + abs(_x3 - mid_x_1) + threshold) or (
            abs(mid_y_1 - mid_y_0) > abs(_y1 - mid_y_0) + abs(_y3 - mid_y_1) + threshold):
      return False

    return True


  def Update(self,distance,yaw):
    length = len(distance)
    WallPerc = np.zeros((1, length+1))
    WallPerc[:, 0] = 1
    N = self.particle_number_max
    Pf1 = np.zeros((2, N))
    w = np.zeros((N, 1)) * 1 / N

    if self.star == 1:
      for i in range(0, N):
        self.P[0, i] = self.start_x + np.random.normal(0,5,size=(1,1))
        self.P[1, i] = self.start_y + np.random.normal(0,5,size=(1,1))
    position = pd.DataFrame(columns=['x', 'y'])

    for k in range(0, length):
      for i in range(0, N):
        Xp1 = copy.deepcopy(self.P[:, i])
        self.P[0, i] = self.P[0, i] + 60 * distance[k] * cos(yaw[k]) + np.random.normal(0, 5, size=(1, 1))
        self.P[1, i] = self.P[1, i] + 60 * distance[k] * sin(yaw[k]) + np.random.normal(0, 5, size=(1, 1))
        Xp2 = copy.deepcopy(self.P[:, i])
        if (Xp2[0] <= self.Xmin or Xp2[0] >= self.Xmax or Xp2[1] <= self.Ymin or Xp2[1] >= self.Ymax):
          w[i] = 0
        elif self.CheckParticleSteps(Xp1, Xp2):
          w[i] = 1
        else:
          w[i] = 0
      WallPerc[:, k + 1] = np.sum(w) / N

      self.P[0, :] = self.P[0, :] * w.T
      self.P[1, :] = self.P[1, :] * w.T

      w_average = w / np.sum(w)
      Pf1[0, :] = self.P[0, :] * w_average.T
      Pf1[1, :] = self.P[1, :] * w_average.T

      self.current_position_x = Pf1.sum(axis=1)[0]
      self.current_position_y = Pf1.sum(axis=1)[1]

      if WallPerc[:, k+1] <= 0.5:
        order = np.argsort(w.T).reshape(-1, 1)
        order2 = np.argsort(-(w.T)).reshape(-1, 1)
        number = N - np.sum(w)
        w2 = w
        flag = int(np.round(number / 2))
        w2[order[0:flag]] = 1

        if np.sum(w) >= flag:
          self.P[:, order[0:flag]] = self.P[:, order2[0:flag]]

        elif (flag % np.sum(w)) != 0:
          times = ceil(flag / np.sum(w))
          for h in range(0, times - 1):
            self.P[:, order[(h - 1) * np.sum(w):h * np.sum(w)]] = self.P[:, order2[0:order2[0:np.sum(w)]]]
          self.P[:, order[h * np.sum(w): flag]] = self.P[:, order2[:(flag % np.sum(w))]]
        else:
          times = flag / np.sum(w)
          for h in range(0, times):
            self.P[:, order[(h - 1) * np.sum(w): h * np.sum(w)]] = self.P[:, order2[0: np.sum(w)]]
        w = w2
        WallPerc[:, k+1] = np.sum(w) / N
      position.loc[k,'x'] = self.current_position_x
      position.loc[k,'y'] = self.current_position_y
    self.star = 2


    if position is not None:
      position = position.values.tolist()

      position_lists=[]

      for numbers in range(0,len(position)):
        position_dict={}
        position_dict["x"]=position[numbers][0]
        position_dict["y"]=position[numbers][1]

        position_lists.append(position_dict)

    return position_lists


# if __name__ == '__main__':

#   file_path = os.path.dirname(__file__)
#   file_paths = os.path.join(file_path,'data.json')
#   file_date = open(file_paths,'r',encoding='utf-8')
#   test_data = json.load(file_date)
#   worker = Worker()
#   position = worker.Run(test_data)

#   # 一段数据读入，则返回数个位置坐标（dataframe格式）
#   print(position)
