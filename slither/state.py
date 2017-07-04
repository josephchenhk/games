# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 18:22:26 2017

@author: joseph.chen
"""
import random
from copy import copy, deepcopy
import constance as ct
from snake import Snake
from utils import Utils
from strategy import RandomAgent, AlphaBetaAgent, SmartGreedyAgent

class State(object):
    '''state of snakes and candies
    '''
    def __init__(self, player="player", snakes={}, candies={}):
        self.player = player
        self.candies = candies
        self.snakes = snakes
        for snake_id in self.snakes.keys():
            del self.snakes[snake_id]
            self.new_snake(snake_id)        
        self.util = Utils()
        #self.snake_ai = RandomAgent()
        #self.snake_ai = AlphaBetaAgent(depth=4)
        self.snake_ai = SmartGreedyAgent()
        
    def get_state(self):
        return self.snakes, self.candies
    
    def set_state(self, snakes, candies):
        self.snakes = snakes
        self.candies = candies
        
    def update(self):
        '''update status of game state
        '''
        if len(self.snakes)>0:
            for snake_id in self.snakes.keys():
                
                if snake_id != self.player: # directions for Snake AI 
                    self.snakes[snake_id].state["direction"] = self.snake_ai.get_action(snake_id, self)                           
                
                snake = self.snakes[snake_id]
                direction = snake.state["direction"]
                coords = snake.state["coordinate"]
                score = snake.state["score"]
                energy = snake.state["energy"]
                move = snake.state["move"]
                acc_net_score = snake.state["acc_net_score"]
                is_revived = snake.state["is_revived"]
                
                # If a snake dies, just make it revived.
                if (self.check_border_collision(snake_id, direction) or
                    self.check_body_collision(snake_id, direction)
                ):
                    self.revive_snake(snake_id)
                    continue

                newHead = snake.predict_head(direction)
                
                if move == ct.MAX_WANDER_MOVE:
                    self.candies.add(positions=newHead, event="default")
                    move = 0
                move += 1
                
                if is_revived:
                    self.candies.add(positions=newHead, event="revival")
                    is_revived = False
                    
                if newHead in self.candies.state.keys():
                    candy_val, candy_type = self.candies.state[newHead]
                    score += candy_val        # add score
                    acc_net_score += candy_val
                    energy += 1          # add energy
                    candies_new_state = deepcopy(self.candies.state)
                    del candies_new_state[newHead] # remove candy
                    self.candies.set_state(candies_new_state)  # update candies state
                    
                body_added = score / ct.VALUE_SNAKE_BODY - len(coords)
                    
                coords.insert(ct.HEAD, newHead)
                tail = coords[ct.TAIL]
                del coords[ct.TAIL]
                for n in range(body_added):
                    coords.append(tail)
                    
#                if move == ct.MAX_WANDER_MOVE:
#                    default_candy_val = self.util.random_pick(ct.VALUE_QUESTION_CANDY, ct.PROB["default"])
#                    score += default_candy_val
#                    acc_net_score += default_candy_val
#                    energy += 1 
#                    move = 0
#                move += 1
                       
                snake_new_state = {"direction":direction, "coordinate":coords, 
                                   "score":score, "energy":energy, "move":move,
                                   "acc_net_score":acc_net_score, "is_revived":is_revived}
                self.snakes[snake_id].set_state(snake_new_state) # update snake state
        
        if random.random() < 0.1:
            self.candies.add(number_common_candy=1, number_question_candy=1, positions=None, 
            event="normal")
            
    def get_legal_actions(self, snake_id):
        '''Let's just assume all four directions are legal, and no acceleration now.
        '''
        return [ct.UP, ct.DOWN, ct.LEFT, ct.RIGHT]
    
    def generate_successor(self, snake_id, action):
        '''Generate successive state.
        * Note: this successor is NOT completed. Here for simplicity we just assume
        the target snake moves according to `action`, while others keep moving in
        their original directions. However, as we know, this should not be always
        correct. Other snakes might also change their directions.
        '''
        state_copy = deepcopy(self)
        assert snake_id in state_copy.snakes
        
        for snake_id in state_copy.snakes.keys():                
            if self.util.border_collision(state_copy.snakes[snake_id]): # check if bumping into border                         
                snake_body_pos = state_copy.snakes[snake_id].state["coordinate"][1:] # exclude snake head
                state_copy.candies.add(positions=snake_body_pos, event="killed")
                state_copy.snakes[snake_id].revive(state_copy.snakes)
                state_copy.snakes[snake_id].state["is_revived"] = True
            if self.util.body_collision(snake_id, state_copy.snakes): # check if bumping into snake body                        
                snake_body_pos = state_copy.snakes[snake_id].state["coordinate"][1:] # exclude snake head
                state_copy.candies.add(positions=snake_body_pos, event="killed")
                state_copy.snakes[snake_id].revive(state_copy.snakes)
                state_copy.snakes[snake_id].state["is_revived"] = True
#            if snake_id != "player": # TODO: random directions for Snake AI 
#                #snakes[snake_id].state["direction"] = random.sample([ct.UP, ct.DOWN, ct.LEFT, ct.RIGHT],1)[0]
#                # snakes[snake_id].state["direction"] = self.snake_ai.get_action()
#                state_copy.snakes[snake_id].state["direction"] = self.snake_ai.get_action(snake_id, state_copy)
#        
        if len(state_copy.snakes)>0:
            for snake_id2 in state_copy.snakes.keys():
                snake = state_copy.snakes[snake_id2]
                direction = snake.state["direction"]
                coords = snake.state["coordinate"]
                score = snake.state["score"]
                energy = snake.state["energy"]
                move = snake.state["move"]
                acc_net_score = snake.state["acc_net_score"]
                is_revived = snake.state["is_revived"]
                
                # If action provided, move according to action required.
                if snake_id2==snake_id:
                    direction = action
                    
                # 根据方向，添加一个新的蛇头，以这种方式来移动贪吃蛇
#                if direction == ct.UP:
#                    newHead = (coords[ct.HEAD][0], coords[ct.HEAD][1] - 1)
#                elif direction == ct.DOWN:
#                    newHead = (coords[ct.HEAD][0], coords[ct.HEAD][1] + 1)
#                elif direction == ct.LEFT:
#                    newHead = (coords[ct.HEAD][0] - 1, coords[ct.HEAD][1])
#                elif direction == ct.RIGHT:
#                    newHead = (coords[ct.HEAD][0] + 1, coords[ct.HEAD][1])
                newHead = snake.predict_head(direction)
                
                if move == ct.MAX_WANDER_MOVE:
                    #state_copy.candies.add(positions=newHead, event="default")
                    move = 0
                move += 1
                
                if is_revived:
                    #state_copy.candies.add(positions=newHead, event="revival")
                    is_revived = False
                    
                if newHead in state_copy.candies.state.keys():
                    candy_val, candy_type = state_copy.candies.state[newHead]
                    score += candy_val        # add score
                    acc_net_score += candy_val
                    energy += 1          # add energy
                    #candies_new_state = deepcopy(state_copy.candies.state)
                    #del candies_new_state[newHead] # remove candy
                    #state_copy.candies.set_state(candies_new_state)  # update candies state
                    
                body_added = score / ct.VALUE_SNAKE_BODY - len(coords)
                    
                coords.insert(ct.HEAD, newHead)
                tail = coords[ct.TAIL]
                del coords[ct.TAIL]
                for n in range(body_added):
                    coords.append(tail)
                       
                snake_new_state = {"direction":direction, "coordinate":coords, 
                                   "score":score, "energy":energy, "move":move,
                                   "acc_net_score":acc_net_score, "is_revived":is_revived}
                state_copy.snakes[snake_id2].set_state(snake_new_state) # update snake state
        
#        if random.random() < 0.1:
#            state_copy.candies.add(number_common_candy=1, number_question_candy=1, positions=None, 
#            event="normal")
            
        return state_copy
    
    def get_score(self, snake_id):
        if self.snakes[snake_id].state["is_revived"]:
            return 0
        else:
            return self.snakes[snake_id].state["score"]
        
    def check_body_collision(self, snake_id, action):
        '''action means direction here.
        '''
        snake = self.snakes[snake_id]
        predict_head = snake.predict_head(action)
        if (predict_head[0] == -1 or predict_head[0] == ct.CELLWIDTH 
            or predict_head[1] == -1 or predict_head[1] == ct.CELLHEIGHT
        ):
            return True
        else:
            return False
        
    def check_border_collision(self, snake_id, action):
        '''action means direction here.
        '''
        snake = self.snakes[snake_id]
        predict_head = snake.predict_head(action)
        for snake2_id in self.snakes.keys():
            if (snake2_id != snake_id):
                snake2_coords = self.snakes[snake2_id].state["coordinate"]
                if predict_head in snake2_coords: # bump into other snakes' body
                    return True
        return False
    
    def new_snake(self, snake_id, energy=0, move=0, acc_net_score=0, is_revived=False):
        # TODO: What if the grid is really full and cannot add a snake anymore?
        # Must think of gameover condition to break this loop.
        while True:
            # initialize a direction
            direction = random.sample([ct.UP, ct.DOWN, ct.LEFT, ct.RIGHT], 1)[0] 
            # randomly assign a head position  
            startx = random.randint(5, ct.CELLWIDTH - 6)
            starty = random.randint(5, ct.CELLHEIGHT - 6)   
            # build a body length equal to 4
            if direction==ct.UP:
                snake_coords = [(startx, starty),
                                (startx, starty + 1),
                                (startx, starty + 2),
                                (startx, starty + 3)]
            elif direction==ct.DOWN:
                snake_coords = [(startx, starty),
                                (startx, starty - 1),
                                (startx, starty - 2),
                                (startx, starty - 3)]
            elif direction==ct.LEFT:
                snake_coords = [(startx, starty),
                                (startx + 1, starty),
                                (startx + 2, starty),
                                (startx + 3, starty)]
            elif direction==ct.RIGHT:
                snake_coords = [(startx, starty),
                                (startx - 1, starty),
                                (startx - 2, starty),
                                (startx - 3, starty)]
            # check validicity of snake coordinates 
            coords_valid = True
            if set(snake_coords).intersection(list(self.candies.state.keys())):
                coords_valid = False
            for sid in self.snakes.keys():
                if set(snake_coords).intersection(self.snakes[sid].state["coordinate"]):
                    coords_valid = False
                    break
            
            if coords_valid:
                init_score = len(snake_coords) * ct.VALUE_SNAKE_BODY
                state = {"direction":direction, "coordinate":snake_coords, 
                         "score": init_score, "energy":energy,
                         "move":move, "acc_net_score":acc_net_score,
                         "is_revived":is_revived}
                self.snakes[snake_id] = Snake()
                self.snakes[snake_id].set_state(state)
                break
            else:
                print("coordinate not valid!")
            
    def kill_snake(self, snake_id):
        snake_body_pos = self.snakes[snake_id].state["coordinate"][0:] # include snake head
        self.candies.add(positions=snake_body_pos, event="killed")
        del self.snakes[snake_id]
        #self.snakes[snake_id].state["is_revived"] = True
        
    def revive_snake(self, snake_id):
        energy = self.snakes[snake_id].state["energy"]
        acc_net_score = self.snakes[snake_id].state["acc_net_score"]
        self.kill_snake(snake_id)
        self.new_snake(snake_id, energy=energy, move=0, acc_net_score=acc_net_score, 
                  is_revived=True)
        
