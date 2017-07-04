# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 14:28:19 2017

@author: joseph.chen
"""

import pygame
import sys
import random

from snake import Snake
from candies import Candies
from state import State
import constance as ct
from utils import Utils
#from strategy import RandomAgent, AlphaBetaAgent

class Slither(object):
    '''Slither Game
    '''
        
    def __init__(self, player_name="player"):
        self.player = player_name
        self.util = Utils()
        pygame.init()     
        self.FPSCLOCK = pygame.time.Clock() # pygame clock
        self.DISPLAYSURF = pygame.display.set_mode((ct.WINDOWWIDTH + ct.PANELWIDTH, ct.WINDOWHEIGHT)) # 设置屏幕宽高  
        self.DISPLAYSURF.fill(ct.BGCOLOR)  
        self.font = pygame.font.Font(None, 25)
        pygame.display.set_caption('Slither') # caption of screen
                           
    def run_game(self):
        snakes = {self.player: Snake()}
        for n in range(ct.NUM_SNAKE_AI):
            snakes[n] = Snake()
        candies = Candies()
        self.state = State(self.player, snakes, candies)
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                elif event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_LEFT):
                        self.state.snakes[self.player].state["direction"] = ct.LEFT
                    elif (event.key == pygame.K_RIGHT):
                        self.state.snakes[self.player].state["direction"] = ct.RIGHT
                    elif (event.key == pygame.K_UP):
                        self.state.snakes[self.player].state["direction"] = ct.UP
                    elif (event.key == pygame.K_DOWN):
                        self.state.snakes[self.player].state["direction"] = ct.DOWN
                    elif (event.key == pygame.K_ESCAPE):
                        self.quit_game()
            
            if not self.game_over(self.state):                       
                       
                self.DISPLAYSURF.fill(ct.BGCOLOR)   
                self.draw_grid()
                self.state.update()
                
                energy_text = "energy: {}".format(self.state.snakes[self.player].state["energy"])
                move_text = "move: {}".format(self.state.snakes[self.player].state["move"])
                score_text = "score: {}".format(self.state.snakes[self.player].state["score"])
                acc_net_score_text = "net score: {}".format(self.state.snakes[self.player].state["acc_net_score"])
                current_return = self.state.snakes[self.player].state["acc_net_score"] * 1.0 * ct.CANDY_POINT_TO_MONEY
                current_payment = (self.state.snakes[self.player].state["energy"] * 1.0 / ct.MAX_NO_CANDY) * ct.WAGER  
                try: 
                    current_rtp =  current_return / current_payment
                except ZeroDivisionError:
                    current_rtp = 0
                rtp_text = "RTP: {}".format(current_rtp)
                for snake_id in self.state.snakes.keys():
                    if snake_id == self.player:
                        self.draw_snake(self.state.snakes[self.player], ct.COLORS['GREEN'])
                    else:
                        self.draw_snake(self.state.snakes[snake_id], ct.COLORS['RED'])
                self.draw_candies(self.state.candies)
                self.draw_panel(self.font, ct.WINDOWWIDTH, 0, energy_text, (240,20,20))
                self.draw_panel(self.font, ct.WINDOWWIDTH, 30, move_text, (240,20,20))
                self.draw_panel(self.font, ct.WINDOWWIDTH, 60, score_text, (240,20,20))
                self.draw_panel(self.font, ct.WINDOWWIDTH, 90, acc_net_score_text, (240,20,20))
                self.draw_panel(self.font, ct.WINDOWWIDTH, 120, rtp_text, (240,20,20))
                pygame.display.update()
                self.FPSCLOCK.tick(ct.FPS)
            
    
    def quit_game(self):
        pygame.quit()
        sys.exit()
        
    def game_over(self, state):
        '''check the condition of game over.
        '''
        if state.snakes["player"].state["energy"] == ct.MAX_ENERGY:
            return True
        else:
            return False
        
    def draw_grid(self):
        for x in range(0, ct.WINDOWWIDTH + ct.CELLSIZE, ct.CELLSIZE): # draw vertical lines
            pygame.draw.line(self.DISPLAYSURF, ct.LINECOLOR, (x, 0), (x, ct.WINDOWHEIGHT))
        for y in range(0, ct.WINDOWHEIGHT + ct.CELLSIZE, ct.CELLSIZE): # draw horizontal lines
            pygame.draw.line(self.DISPLAYSURF, ct.LINECOLOR, (0, y), (ct.WINDOWWIDTH, y))
            
    def draw_snake(self, snake, body_color):
        snake_coords = snake.state["coordinate"]
        for i,coord in enumerate(snake_coords):
            if i==0:
                color = ct.COLORS['WHITE']
            else:
                color = body_color
            x = coord[0] * ct.CELLSIZE
            y = coord[1] * ct.CELLSIZE
#            snakeSegmentRect = pygame.Rect(x, y, ct.CELLSIZE, ct.CELLSIZE)
#            pygame.draw.rect(self.DISPLAYSURF, color, snakeSegmentRect)
            radius = int(ct.CELLSIZE/2.0)
            pygame.draw.circle(self.DISPLAYSURF, color, [x+radius, y+radius], radius, 0)
    
    def draw_candies(self, candies):
        for candy_pos in self.state.candies.state.keys():
            if self.state.candies.state[candy_pos][1] == "common":
                color = ct.COLORS["BRONZE"]
            elif self.state.candies.state[candy_pos][1] == "question":
                color = ct.COLORS["GOLD"]
            x = candy_pos[0] * ct.CELLSIZE
            y = candy_pos[1] * ct.CELLSIZE
            candySegmentRect = pygame.Rect(x, y, ct.CELLSIZE, ct.CELLSIZE)
            pygame.draw.rect(self.DISPLAYSURF, color, candySegmentRect)
            
    def draw_panel(self, font, x, y, text, color=(255,255,255)):
        imgText = font.render(text, True, color)
        screen = pygame.display.get_surface() #req'd when function moved into MyLibrary
        screen.blit(imgText, (x,y))
            
