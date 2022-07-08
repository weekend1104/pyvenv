# -*- coding:utf-8 -*-
"""
project: pythonProject1
file: displayboard
author: Yujin
create date: 2022/6/21 14:58
description: 
"""
import math

def predict_board(x,y,label,board_x_out,board_y_out,board_x_in,board_y_in,boardId_out,boardId_in,model_name):
    R1_5 = 1.5
    R2 = 2
    boardId = ''
    length_out = len(board_x_out)
    length_in = len(board_x_in)
    if (label == 0):
        for i in range(length_out):
            if ((math.sqrt((x - board_x_out[i]) ** 2 + (y - board_y_out[i]) ** 2)) <= R1_5):
                boardId = "{}{}".format(model_name,boardId_out[i])
                break
    else:
        for i in range(length_in):
            if ((math.sqrt((x - board_x_in[i]) ** 2 + (y - board_y_in[i]) ** 2)) <= R2):
                boardId = "{}{}".format(model_name,boardId_in[i])
                break
    return boardId

def display(x, y, label, model_name):

    boardall_x_out = [[12.6, 5.4, 0.9, 10.8, 15.3],
                      [12.6, 5.4, 0.9, 10.8, 15.3],
                      [12.6, 5.4, 0.9, 10.8, 15.3],
                      [12.6, 5.4, 0.9, 15.3],
                      [12.6, 5.4, 0.9, 10.8, 15.3, 15.3]]

    boardall_y_out = [[15.3, 15.3, 10.8, 0.9, 5.4],
                      [15.3, 15.3, 10.8, 0.9, 5.4],
                      [15.3, 15.3, 10.8, 0.9, 5.4],
                      [15.3, 15.3, 10.8, 5.4],
                      [15.3, 15.3, 10.8, 0.9, 5.4, 12.6]]

    boardall_x_in = [[10.8, 6.3, 7.2, 5.4],
                     [10.8, 6.3, 7.2, 10.8, 5.4],
                     [10.8, 6.3, 7.2],
                     [6.3, 7.2, 10.8],
                     [10.8, 6.3, 7.2, 10.8, 5.4]]

    boardall_y_in = [[12.6, 12.6, 8.1, 3.6],
                     [12.6, 12.6, 8.1, 3.6, 3.6],
                     [12.6, 12.6, 8.1],
                     [12.6, 8.1, 3.6],
                     [12.6, 12.6, 8.1, 3.6, 3.6]]

#    boardall_Id_out = [[1, 2, 3, 4, 5],
 #                      [1, 9, 10, 7, 8],
  #                     [1, 2, 3, 4, 5],
   #                    [1, 6, 7, 2],
    #                   [1, 2, 3, 11, 10, 9]]

   # boardall_Id_in = [[6, 7, 8, 9],
    #                  [2, 3, 4, 5, 6],
     #                 [6, 7, 8],
      #                [5, 4, 3],
       #               [8, 7, 6, 5, 4]]

    boardall_Id_out = [['01', '02', '03', '04', '05'],
                       ['01', '09', '10', '07', '08'],
                       ['01', '02', '03', '04', '05'],
                       ['01', '06', '07', '02'],
                       ['01', '02', '03', '11', '10', '09']]

    boardall_Id_in = [['06', '07', '08', '09'],
                      ['02', '03', '04', '05', '06'],
                      ['06', '07', '08'],
                      ['05', '04', '03'],
                      ['08', '07', '06', '05', '04']]

    model_name_all = ['1EC','2MA','3EN','4CO','5AR']
    
    boardId = ''
    for i in range(len(model_name_all)):
        if model_name == model_name_all[i]:
            board_x_out = boardall_x_out[i]
            board_y_out = boardall_y_out[i]
            board_x_in = boardall_x_in[i]
            board_y_in = boardall_y_in[i]
            boardId_out = boardall_Id_out[i]
            boardId_in = boardall_Id_in[i]
            boardId = predict_board(x, y, label, board_x_out, board_y_out, board_x_in, board_y_in, boardId_out,
                                    boardId_in,model_name)
            break

    return boardId
