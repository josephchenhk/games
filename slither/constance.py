# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 12:33:21 2017

@author: joseph.chen
"""
FPS = 5 # 屏幕刷新率（在这里相当于贪吃蛇的速度）
WINDOWWIDTH = 700 # 屏幕宽度
WINDOWHEIGHT = 700 # 屏幕高度
CELLSIZE = 14 # 小方格的大小
assert CELLSIZE % 2 == 0, "Cell size must be a multipe of 2."
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)
assert CELLWIDTH >= 20, "Cell width must be no less than 20."
assert CELLHEIGHT >= 20, "Window height must be no less than 20."
PANELWIDTH = CELLSIZE * 10
SNAKE_INIT_LENGTH = 4
VALUE_SNAKE_BODY = 15
VALUE_COMMON_CANDY = 5
VALUE_QUESTION_CANDY = [1, 2, 3, 4, 5, 6, 7, 8, 9]
MULT_PILL_CANDY = [1.5, 0.5]
MOVES_OF_PROTECTOR = 20
MULT_ACCELERATOR = 2
WAGER = 100
MAX_NO_CANDY = 100
CANDY_POINT_TO_MONEY = 0.18
INIT_CNADY_NUMBER = 10

COLORS = {'BLACK' : (0, 0, 0), 
          'WHITE' : (255,255,255), 
          'RED' : (255,0,0), 
          'GREEN': (0,255,0),
          'BLUE': (0,0,255),
          'BRONZE': (205,127,50), 
          'GRAY': (180,180,180), 
          'GOLD': (212,175,55),
          'VIOLET': (200,0,255),
          'DARKGRAY': (40,40,40)
          }
BGCOLOR = COLORS['BLACK']
LINECOLOR = COLORS['DARKGRAY']

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

# 贪吃蛇的头（）
HEAD = 0 # syntactic sugar: index of the snake's head
TAIL = -1 # syntactic sugar: index of the snake's tail

MAX_ENERGY = 100
NUM_SNAKE_AI = 5
MAX_WANDER_MOVE = 20

PROB = {"default": [0,0,0,0,1,0,0,0,0],
        "normal": [1.0/9.0]*9,
        "revival": [0,0,0] + [1.0/3.0]*3 + [0,0,0],
        "killed": [1.0/6.0]*3 + [0]*3 + [1.0/6.0]*3}