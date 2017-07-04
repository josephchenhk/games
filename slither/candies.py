# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 18:07:35 2017

@author: joseph.chen
"""
import random

from utils import Utils
import constance as ct

class Candies(object):
    '''Candies coordinates and values in the grid
    '''
    def __init__(self):
        candies = {}
        n = 0
        while n < ct.INIT_CNADY_NUMBER:
            # 随机初始化设置一个点作为candy的起点
            startx = random.randint(1, ct.CELLWIDTH-1)
            starty = random.randint(1, ct.CELLHEIGHT-1)
            if (startx,starty) not in candies.keys():
                candies[(startx,starty)] = (ct.VALUE_COMMON_CANDY, "common")
                n += 1
        self.state = candies
        self.util = Utils()
        
    def get_state(self):
        return self.state 
    
    def set_state(self, new_state):
        self.state = new_state
        
#    def random_add(self, number_common_candy=0, number_question_candy=0, event="normal"):
#        candies = self.state
#        n = 0
#        while n < number_common_candy:
#            # 随机初始化设置一个点作为candy的起点
#            startx = random.randint(1, ct.CELLWIDTH-1)
#            starty = random.randint(1, ct.CELLHEIGHT-1)
#            if (startx,starty) not in candies.keys():
#                candies[(startx,starty)] = (ct.VALUE_COMMON_CANDY, "common")
#                n += 1
#        
#        m = 0
#        while m < number_question_candy:
#            # 随机初始化设置一个点作为candy的起点
#            startx = random.randint(1, ct.CELLWIDTH-1)
#            starty = random.randint(1, ct.CELLHEIGHT-1)
#            if (startx,starty) not in candies.keys():
#                candy_val = self.util.random_pick(ct.VALUE_QUESTION_CANDY, ct.PROB[event])
#                candies[(startx,starty)] = (candy_val, "question")
#                m += 1
#        
#        self.set_state(candies)        
#        #self.state = candies
        
    def add(self, number_common_candy=0, number_question_candy=0, positions=None, 
            event="killed"):
        '''Add candies according to different events.
        '''
        candies = self.state
        if event=="killed":
            assert positions != None, "Killed snakes must have positions!"
            for pos in positions:
                candy_val = self.util.random_pick(ct.VALUE_QUESTION_CANDY, ct.PROB[event])
                candies[pos] = (candy_val, "question")
                           
        elif event=="normal":
            n = 0
            while n < number_common_candy:
                # 随机初始化设置一个点作为candy的起点
                startx = random.randint(1, ct.CELLWIDTH-1)
                starty = random.randint(1, ct.CELLHEIGHT-1)
                if (startx,starty) not in candies.keys():
                    candies[(startx,starty)] = (ct.VALUE_COMMON_CANDY, "common")
                    n += 1        
            m = 0
            while m < number_question_candy:
                # 随机初始化设置一个点作为candy的起点
                startx = random.randint(1, ct.CELLWIDTH-1)
                starty = random.randint(1, ct.CELLHEIGHT-1)
                if (startx,starty) not in candies.keys():
                    candy_val = self.util.random_pick(ct.VALUE_QUESTION_CANDY, ct.PROB[event])
                    candies[(startx,starty)] = (candy_val, "question")
                    m += 1                   
        
        elif event=="default":
            assert positions != None, "Position must not be None! After 20 moves, default candy position would be in snake head."
            candy_val = self.util.random_pick(ct.VALUE_QUESTION_CANDY, ct.PROB[event])
            candies[positions] = (candy_val, "default")
            
        elif event=="revival": # same as default
            assert positions != None, "Position must not be None! After 20 moves, default candy position would be in snake head."
            candy_val = self.util.random_pick(ct.VALUE_QUESTION_CANDY, ct.PROB[event])
            candies[positions] = (candy_val, "default")
            
        self.set_state(candies)    