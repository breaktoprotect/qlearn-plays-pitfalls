# Author        : JS @breaktoprotect
# Description   : A simple 8 by 8 environment with a static start and goal point. 
#                 Agent's goal is to reach the goal point while avoiding holes. 
import numpy as np
import pygame
import time

class Pitfalls:
    def __init__(self, height=8, width=8, starvation_move=200):
        self.height = height
        self.width = width
        self.rewards_table = self._init_difficult_rewards_table(height=height, width=width)
        #self.rewards_table = self._init_rewards_table(height=height, width=width) # Standard difficulty or Normal
        self.starvation_move = starvation_move

    def reset(self):
        self.current_pos = (0,0) # Starting position
        self.done = False
        self.move = 0
        return

    # Return random action: Up = 0; Right = 1; Down = 2; Left = 3
    def action_space_sample(self):
        return np.random.randint(0,4)

    #* Every step you take
    def step(self, action):
        #TODO validate for actions

        original_position = self.current_pos

        # Up = 0; Right = 1; Down = 2; Left = 3
        if action == 0:
            self.current_pos = tuple(np.add(self.current_pos, (-1, 0))) # Up
        elif action == 1: 
            self.current_pos = tuple(np.add(self.current_pos, (0, 1))) # Right
        elif action == 2:
            self.current_pos = tuple(np.add(self.current_pos, (1, 0))) # Down
        elif action == 3:
            self.current_pos = tuple(np.add(self.current_pos, (0, -1))) # Left
        else:
            return -1

        # Track number of moves
        self.move += 1

        #* Assign rewards
        reward = 0

        # Out of bounds
        if not self.is_within_bounds(self.current_pos):
            self.current_pos = original_position # revert to most previous position

            return None, reward, self.done, {'msg':'Out of bounds!'}

        # Stucked Agent - starved to death
        if self.move > self.starvation_move:
            reward = -1
            self.done = True

            #debug
            #print("Starved to death!")

            return self.current_pos, reward, self.done, {'msg':'Starved to death.'}

        # Goal
        if np.all(self.current_pos == (7,7)):
            reward = 100 # Win game
            self.done = True
            return self.current_pos, reward, self.done, {'msg':'Win!'}
        
        # Hole
        if np.all(self.rewards_table[tuple(self.current_pos)] == -100):
            reward = -100
            self.done = True
            return self.current_pos, reward, self.done, {'msg':'Death by pitfall!'}

        # Ordinary tile
        if np.all(self.rewards_table[tuple(self.current_pos)] <= -1) or np.all(self.rewards_table[tuple(self.current_pos)] >= -3):
            reward = self.rewards_table[tuple(self.current_pos)]
            return self.current_pos, reward, self.done, {}



        print("[!] Unexpected state reached!")

    def is_within_bounds(self, position):
        if position[0] > 7 or position[0] < 0:
            return False
        if position[1] > 7 or position[1] < 0:
            return False
        return True

    def render(self):
        pass

    #* Normal: Create a reward table 8 by 8 states
    def _init_rewards_table(self, height, width):
        #? Idea: Negative reinforcement reduces as agent approaches goal
        '''
        S F F F F F F F
        F F F F F F F F
        F F F H F F F F
        F F F F F H F F
        F F F H F F F F
        F H H F F F H F
        F H F F H F H F
        F F F H F F F G
        '''
        rewards_table = np.zeros(shape=(height, width))

        #* Set all state to various negative reinforcement
        #  -3 for [2][2] and below
        #  -2 for [4][4] and below
        #  -1 for [5][5] and above
        for row, y in enumerate(rewards_table):
            for col, x in enumerate(rewards_table[row]):
                if  row <= 2 and col <= 2:
                    rewards_table[row][col] = -3
                elif (row > 2 and row <= 4) or (col > 2 and col <=4):
                    rewards_table[row][col] = -2
                else:
                    rewards_table[row][col] = -1


        # Holes are -100 reward
        rewards_table[2][3] = -100
        rewards_table[3][5] = -100
        rewards_table[4][3] = -100
        rewards_table[5][1] = -100
        rewards_table[5][2] = -100
        rewards_table[5][6] = -100
        rewards_table[6][1] = -100
        rewards_table[6][4] = -100
        rewards_table[6][6] = -100
        rewards_table[7][3] = -100

        # Goal is 100 reward
        rewards_table[7][7] = 100

        #debug
        print("rewards_table:\n", rewards_table)
        print("")

        return rewards_table

    #* Difficult: Create a reward table 8 by 8 states
    def _init_difficult_rewards_table(self, height, width):
        #? Idea: Negative reinforcement reduces as agent approaches goal
        '''
        S F F F F F F F
        F F F F F F F F
        F F F H F F F F
        F F F F F H F F
        F F F H F F F H
        F H H F F F H F
        F H F F H F H F
        F F F H F F F G
        '''
        rewards_table = np.zeros(shape=(height, width))

        #* Set all state to various negative reinforcement
        #  -3 for [2][2] and below
        #  -2 for [4][4] and below
        #  -1 for [5][5] and above
        for row, y in enumerate(rewards_table):
            for col, x in enumerate(rewards_table[row]):
                if  row <= 2 and col <= 2:
                    rewards_table[row][col] = -3
                elif (row > 2 and row <= 4) or (col > 2 and col <=4):
                    rewards_table[row][col] = -2
                else:
                    rewards_table[row][col] = -1


        # Holes are -100 reward
        rewards_table[2][3] = -100
        rewards_table[3][5] = -100
        rewards_table[4][3] = -100
        rewards_table[4][7] = -100
        rewards_table[5][1] = -100
        rewards_table[5][2] = -100
        rewards_table[5][6] = -100
        rewards_table[6][1] = -100
        rewards_table[6][4] = -100
        rewards_table[6][6] = -100
        rewards_table[7][3] = -100

        # Goal is 100 reward
        rewards_table[7][7] = 100

        #debug
        print("rewards_table:\n", rewards_table)
        print("")

        return rewards_table

    def render_text(self):
        for r, x in enumerate(self.rewards_table):
            for c, y in enumerate(self.rewards_table[r]):
                if np.all((r,c) == self.current_pos):
                    if self.move == 0:
                        print("\u001b[36m[\u001b[0m", end="")
                    else:
                        print("[", end="")
                else:
                    print(" ", end="")
                
                if self.rewards_table[r][c] <= -1 and self.rewards_table[r][c] >= -3:
                    print("F", end="")
                elif self.rewards_table[r][c] == -100:
                    print("\u001b[30mH\u001b[0m", end="")
                else:
                    print("\u001b[33mG\u001b[0m", end="")

                if np.all((r,c) == self.current_pos):
                    if self.move == 0:
                        print("\u001b[36m]\u001b[0m", end="")
                    else:
                        print("]", end="")
                else:
                    print(" ", end="")
            print("")
        print("")

    def game_screen_setup(self, height=8, width=8, segment_size=25):
        self.segment_size = segment_size

#? Test bed
if __name__ == "__main__":
    env = Pitfalls()
    env.reset()
    env.render_text()
    
    print(env.step(1))
    env.render_text()
    '''
    print(env.step(1))
    env.render_text()

    print(env.step(1))
    env.render_text()

    print(env.step(2))
    env.render_text()

    print(env.step(2))
    env.render_text()
    '''
