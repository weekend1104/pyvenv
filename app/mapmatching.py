# -*- coding:utf-8 -*-
"""
project: pythonProject1
file: Mapmatching
author: Yujin
create date: 2022/6/21 14:55
description: 
"""
import math

class Mapmatching(object):
    def __init__(self):
        pass

    def select_model(self,model_name):
        pathA_x_out = [12.6, 12.6,  0.9, 0.9, 15.3, 15.3, 12.6, 12.6]
        pathA_y_out = [16.2, 15.3, 15.3, 0.9,  0.9, 15.3, 15.3, 13.5]
        pathA_x_in = [12.6,  12.6,  6.3,  6.3, 9.9, 9.9, 3.6, 3.6, 3.6]
        pathA_y_in = [13.5,  12.6, 12.6,  8.1, 8.1, 3.6, 3.6, 2.5, 0.9]
        pathB_x_out = [3.6,15.3,15.3,12.6,12.6,12.6,12.6,0.9,0.9]
        pathB_y_out = [0.9,0.9,15.3,15.3,16.2,13.5,15.3,15.3,0.9]
        pathB_x_in = [12.6,12.6,6.3,6.3,9.9,9.9,3.6,3.6,3.6]
        pathB_y_in = [13.5,12.6,12.6,8.1,8.1,3.6,3.6,2.5,0.9]
        line1_out = [[12.6,16.2,12.6,15.3],
                 [12.6,15.3,0.9,15.3],
                 [0.9,15.3,0.9,0.9],
                 [0.9,0.9,15.3,0.9],
                 [15.3,0.9,15.3,15.3],
                 [15.3,15.3,12.6,15.3],
                 [12.6,15.3,12.6,13.5]]

        line1_in = [[12.6, 13.5, 12.6, 12.6],
                 [12.6, 12.6, 6.3, 12.6],
                 [6.3, 12.6, 6.3, 8.1],
                 [6.3, 8.1, 9.9, 8.1],
                 [9.9, 8.1, 9.9, 3.6],
                 [9.9, 3.6, 3.6, 3.6],
                 [3.6, 3.6, 3.6, 2.5],
                 [3.6, 2.5, 3.6, 0.9]]

        line2_out = [[3.6, 0.9, 15.3, 0.9],
                     [15.3, 0.9, 15.3, 15.3],
                     [15.3, 15.3, 12.6, 15.3],
                     [12.6, 15.3, 12.6, 16.2],
                     # [12.6, 16.2, 12.6, 13.5],
                     [12.6, 13.5, 12.6, 15.3],
                     [12.6, 15.3, 0.9, 15.3],
                     [0.9, 15.3, 0.9, 0.9]]

        line2_in = [[12.6, 13.5, 12.6, 12.6],
                    [12.6, 12.6, 6.3, 12.6],
                    [6.3, 12.6, 6.3, 8.1],
                    [6.3, 8.1, 9.9, 8.1],
                    [9.9, 8.1, 9.9, 3.6],
                    [9.9, 3.6, 3.6, 3.6],
                    [3.6, 3.6, 3.6, 2.5],
                    [3.6, 2.5, 3.6, 0.9]]

        if model_name == '1EC':
#            path_x_out = pathA_x_out
#            path_y_out = pathA_y_out
#            path_x_in = pathA_x_in
 #           path_y_in = pathA_y_in
            line_out = line1_out
            line_in = line1_in
            board1_x = [12.6,12.6,5.4,0.9,10.8,15.3,12.6,6.3,7.2,5.4]
            board1_y = [16.2,15.3,15.3,10.8,0.9,5.4,12.6,12.6,8.1,3.6]
        elif model_name=='2MA':
  #          path_x_out = pathB_x_out
   #         path_y_out = pathB_y_out
    #        path_x_in = pathB_x_in
     #       path_y_in = pathB_y_in
            line_out = line2_out
            line_in = line2_in
        elif model_name == '3EN':
      #      path_x_out = pathA_x_out
       #     path_y_out = pathA_y_out
        #    path_x_in = pathA_x_in
         #   path_y_in = pathA_y_in
            line_out = line1_out
            line_in = line1_in
        elif model_name == '4CO':
#            path_x_out = pathB_x_out
 #           path_y_out = pathB_y_out
  #          path_x_in = pathB_x_in
   #         path_y_in = pathB_y_in
            line_out = line2_out
            line_in = line2_in
      #  elif model_name == '5AR':
        else:
            path_x_out = pathA_x_out
            path_y_out = pathA_y_out
            path_x_in = pathA_x_in
            path_y_in = pathA_y_in
            line_out = line1_out
            line_in = line1_in
        return line_out,line_in

    def point_distance_line(self,x, y, x1, y1, x2, y2):

        cross = (x2 - x1) * (x - x1) + (y2 - y1) * (y - y1)
        d2 = (x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1)
        if cross <= 0:
            return math.sqrt((x - x1) * (x - x1) + (y - y1) * (y - y1))

        if cross >= d2:
            return math.sqrt((x - x2) * (x - x2) + (y - y2) * (y - y2))

        r = cross / d2
        px = x1 + (x2 - x1) * r
        py = y1 + (y2 - y1) * r
        return math.sqrt((x - px) * (x - px) + (py - y) * (py - y))

    def replace(self,x, y, x1, y1, x2, y2):

        cross = (x2 - x1) * (x - x1) + (y2 - y1) * (y - y1)

        if cross <= 0:
            return x1, y1

        d2 = (x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1)

        if cross >= d2:
            return x2, y2

        r = cross / d2
        px = x1 + (x2 - x1) * r
        py = y1 + (y2 - y1) * r
        return px, py

    def project(self,x,y,label,model_name):
        line_out,line_in = self.select_model(model_name)
        if label == 0:
            line = line_out
       # elif label == 1:
        else:
            line = line_in
        temp_dist = []
        newx , newy = x,y
        for j in range(len(line)):
            temp_dist.append(
                self.point_distance_line(x, y, line[j][0], line[j][1], line[j][2],line[j][3]))

            min_dist = min(temp_dist)

            if min_dist <= 2:
                min_line = temp_dist.index(min_dist)
                newx, newy = self.replace(x, y, line[min_line][0], line[min_line][1],
                                     line[min_line][2], line[min_line][3])
          #  else:
           #     newx,newy = x,y
        return newx,newy
