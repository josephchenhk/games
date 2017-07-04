# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 13:49:17 2017

@author: joseph.chen
"""
import random
from copy import deepcopy
import constance as ct
from utils import Utils

#def evaluation_function(snake_id, state):
#    ''' Let's just target at achieving maximum score at the moment.
#    '''
#    # TODO: the evalFn must be designed delibrately.
#    if state.snakes[snake_id].state["is_revived"]:
#        print("revive!")
#        return 0
#    else:
#        score = state.snakes[snake_id].state["score"]  
#        min_distance = min(
#                [Utils.distance(state.snakes[snake_id].state["coordinate"][ct.HEAD],
#                 candy_pos) for candy_pos in state.candies.state.keys()]
#        )
#        #print(score, min_distance)
#        return score - min_distance

def evaluation_function(snake_id, state):
    ''' Let's just target at achieving maximum score at the moment.
    '''
    # TODO: the evalFn must be designed delibrately.
    score = state.get_score(snake_id)  
    min_distance = min(
                [Utils.distance(state.snakes[snake_id].state["coordinate"][ct.HEAD], candy_pos) for candy_pos in state.candies.state.keys()]
    ) # /  float(2*ct.CELLWIDTH)
    
#    if snake_id != "player" and min_distance<=1:
#        print("min distance: {}".format(min_distance))
#        print("snake id: {}".format(snake_id))
#        print(state.snakes[snake_id].state["coordinate"][ct.HEAD])
#        print(state.candies.state.keys())
#        print("------------------\n")
        
    min_distance = Utils.distance(state.snakes[snake_id].state["coordinate"][ct.HEAD], (0,0))     

    return - min_distance
    
class RandomAgent(object):
    def __init__(self):
        pass
    
    def get_action(self):
        return random.sample([ct.UP, ct.DOWN, ct.LEFT, ct.RIGHT],1)[0]
    

# Minimax Search with alpha-beta pruning
class AlphaBetaAgent(object):
    def __init__(self, depth):
        self.depth = depth
    
#    def alpha_beta(self, snake_id, state, depth, alpha, beta, maximizing, currentVal):
#        if depth == 0:
#            return currentVal
#        if maximizing:
#            value = -float('inf')
#            legal_actions = state.get_legal_actions(snake_id)
#            current_state = deepcopy(state)
#            for action in legal_actions:
#                next_state = current_state.generate_successor(snake_id, action)
#                value = max(value, self.alpha_beta(snake_id, next_state, depth-1, alpha, beta, False, currentVal + evaluation_function(snake_id, current_state)))
#                current_state = next_state
#                alpha = max(alpha, value)
#                if beta <= alpha:
#                    break
#            return value
#        else:
#            value = float('inf')
#            legal_actions = state.get_legal_actions(snake_id)
#            current_state = deepcopy(state)
#            for action in legal_actions:
#                next_state = current_state.generate_successor(snake_id, action)
#                value = min(value, self.alpha_beta(snake_id, next_state, depth-1, alpha, beta, True, currentVal + evaluation_function(snake_id, current_state)))
#                current_state = next_state
#                beta = min(beta, value)
#                if beta <= alpha:
#                    break
#            return value
        
    def alpha_beta(self, snake_id, state, depth, alpha, beta, maximizing):
        if depth == 0:
            currentVal = evaluation_function(snake_id, state)
            return currentVal
        if maximizing:
            value = -float('inf')
            legal_actions = state.get_legal_actions(snake_id)
            current_state = deepcopy(state)
            for action in legal_actions:
                next_state = current_state.generate_successor(snake_id, action)
                value = max(value, self.alpha_beta(snake_id, next_state, depth-1, alpha, beta, False))
                alpha = max(alpha, value)
                if beta <= alpha:
                    break
            return value
        else:
            value = float('inf')
            legal_actions = state.get_legal_actions(snake_id)
            current_state = deepcopy(state)
            for action in legal_actions:
                next_state = current_state.generate_successor(snake_id, action)
                value = min(value, self.alpha_beta(snake_id, next_state, depth-1, alpha, beta, True))
                current_state = next_state
                beta = min(beta, value)
                if beta <= alpha:
                    break
            return value
              
    def get_action(self, snake_id, state):
        legal_actions = state.get_legal_actions(snake_id)
        actions = {}
#        before = best_action
        alpha = -(float("inf"))
        beta = float("inf")
        for action in legal_actions:
            next_state = state.generate_successor(snake_id, action)
            score = self.alpha_beta(snake_id, next_state, self.depth, alpha, beta, True)
            actions[action] = score
#        print("{}\n-----------------\n".format(actions))
#        after = best_action
#        print(before, after)
        best_actions = []
        max_score = max(actions.values())
        for k,v in actions.iteritems():
            if v==max_score:
                best_actions.append(k)
#        print("best actions: {}".format(best_actions))
        return random.sample(best_actions,1)[0]

   
class SmartGreedyAgent(object):
    """
    Take action which brings us closest to a candy
    Checks if we're hitting another snake
    """
    
    def __init__(self):
        pass
    
    def get_action(self, snake_id, state):
        snake = state.snakes[snake_id]
        # Computing the list of actions that won't kill the snake
        actions = [move for move in state.get_legal_actions(snake_id) if not (state.check_body_collision(snake_id, move) or state.check_border_collision(snake_id, move))]
    
        # If it is empty, then the snake will die and we move randomly
        if len(actions) == 0:
            return None
    
        # If there is no candy we move randomly
        if len(state.candies.state) == 0:
            return random.sample(actions, 1)[0]
        
        best_move = min((Utils.distance(snake.predict_head(move), candy_pos), move)
                        for candy_pos in state.candies.state.iterkeys() for move in actions)
        return best_move[1]