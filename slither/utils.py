# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 16:20:18 2017

@author: joseph.chen
"""
import math
import random
import constance as ct

class Utils(object):
    
    def __init__(self):
        pass
    
#    def border_collision(self, snake):
#        snake_coords = snake.state["coordinate"]
#        if (snake_coords[ct.HEAD][0] == -1 or snake_coords[ct.HEAD][0] == ct.CELLWIDTH 
#            or snake_coords[ct.HEAD][1] == -1 or snake_coords[ct.HEAD][1] == ct.CELLHEIGHT
#        ):
#            return True
#        else:
#            return False
#
#    def body_collision(self, snake_id, snakes):
#        for snake2_id in snakes.keys():
#            if (snake2_id != snake_id):
#                snake_coords = snakes[snake_id].state["coordinate"]
#                snake2_coords = snakes[snake2_id].state["coordinate"]
#                if snake_coords[ct.HEAD] in snake2_coords: # bump into other snakes' body
#                    return True
#        return False
    
    def candy_value(self, pos, candies):
        if pos in candies:
            return candies[pos]
        else:
            return None
        
    def random_pick(self, some_list, probabilities):
        """
        Source:　https://www.safaribooksonline.com/library/view/python-cookbook-2nd/0596007973/ch04s22.html
        """
        x = random.uniform(0, 1)
        cumulative_probability = 0.0
        for item, item_probability in zip(some_list, probabilities):
            cumulative_probability += item_probability
            if x < cumulative_probability: break
        return item
    
    @staticmethod
    def distance(pos1, pos2):
        return abs(pos1[0]-pos2[0]) + abs(pos1[1]-pos2[1])
        # return math.sqrt((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2 ) 