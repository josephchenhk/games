# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 17:22:04 2017

@author: joseph.chen
"""
import random
import constance as ct

class Snake(object):
    ''' Snake object
    '''
    def __init__(self):
        #self.new(snakes)
        self.state = {"direction": None, 
                      "coordinate": [], 
                      "score": None, 
                      "energy": None,
                      "move": None, 
                      "acc_net_score": None,
                      "is_revived": None}
        
    def get_state(self):
        return self.state 
    
    def set_state(self, new_state):
        self.state = new_state
        
#    def new(self, snakes, energy=0, move=0, acc_net_score=0):    
#        # 随机初始化设置一个点作为贪吃蛇的起点
#        while True:
#            head_valid = True
#            startx = random.randint(5, ct.CELLWIDTH - 6)
#            starty = random.randint(5, ct.CELLHEIGHT - 6)
#            for snake_id in snakes.keys():
#                if (startx, starty) in snakes[snake_id].state["coordinate"]:
#                    head_valid = False
#                    break
#            if head_valid:
#                break
#    
#        # 以这个点为起点，建立一个长度为4格的贪吃蛇（数组）
##        snake_coords = [{'x': startx, 'y': starty},
##                      {'x': startx - 1, 'y': starty},
##                      {'x': startx - 2, 'y': starty},
##                      {'x': startx - 3, 'y': starty}]
#        snake_coords = [(startx, starty),
#                        (startx - 1, starty),
#                        (startx - 2, starty),
#                        (startx - 3, starty)]
#    
#    
#        direction = ct.RIGHT # 初始化一个运动的方向
#        self.init_score = len(snake_coords) * ct.VALUE_SNAKE_BODY
#        self.state = {"direction":direction, "coordinate":snake_coords, 
#                      "score": self.init_score, "energy":energy,
#                      "move":move, "acc_net_score":acc_net_score,
#                      "is_revived":False}

#    def new(self, snakes, energy=0, move=0, acc_net_score=0):   
#        # initialize a direction
#        direction = random.sample([ct.UP, ct.DOWN, ct.LEFT, ct.RIGHT], 1)[0] 
#        # 随机初始化设置一个点作为贪吃蛇的起点
#        while True:
#            head_valid = True
#            startx = random.randint(5, ct.CELLWIDTH - 6)
#            starty = random.randint(5, ct.CELLHEIGHT - 6)
#            for snake_id in snakes.keys():
#                if (startx, starty) in snakes[snake_id].state["coordinate"]:
#                    head_valid = False
#                    break
#            if head_valid:
#                break
#    
#        # 以这个点为起点，建立一个长度为4格的贪吃蛇（数组）
##        snake_coords = [{'x': startx, 'y': starty},
##                      {'x': startx - 1, 'y': starty},
##                      {'x': startx - 2, 'y': starty},
##                      {'x': startx - 3, 'y': starty}]
#        snake_coords = [(startx, starty),
#                        (startx - 1, starty),
#                        (startx - 2, starty),
#                        (startx - 3, starty)]
#    
#    
#        direction = ct.RIGHT # 初始化一个运动的方向
#        self.init_score = len(snake_coords) * ct.VALUE_SNAKE_BODY
#        self.state = {"direction":direction, "coordinate":snake_coords, 
#                      "score": self.init_score, "energy":energy,
#                      "move":move, "acc_net_score":acc_net_score,
#                      "is_revived":False}
        
#    def revive(self, snakes):
#        energy = self.state["energy"]
#        acc_net_score = self.state["acc_net_score"]
#        self.new(snakes, energy=energy, move=0, acc_net_score=acc_net_score)
        
    def predict_head(self, direction):
        coords = self.state["coordinate"]        
        if direction == ct.UP:
            newHead = (coords[ct.HEAD][0], coords[ct.HEAD][1] - 1)
        elif direction == ct.DOWN:
            newHead = (coords[ct.HEAD][0], coords[ct.HEAD][1] + 1)
        elif direction == ct.LEFT:
            newHead = (coords[ct.HEAD][0] - 1, coords[ct.HEAD][1])
        elif direction == ct.RIGHT:
            newHead = (coords[ct.HEAD][0] + 1, coords[ct.HEAD][1])
        return newHead
        


    
