# Author        : JS @breaktoprotect
# Description   : To create a simple q-learning agent to play learn to reach the goal without falling into a hole
import numpy as np
import gym
from pitfalls_env import Pitfalls
import keyboard
import time
import sys #for debugging try/catch

class QLearnAgent:
    def __init__(self, learning_rate=0.1, discount_rate=0.95, epsilon = 0.9, epsilon_decay = 0.999, epsilon_minimum=0.1):
        self.q_table = self._init_q_table()
        self.learning_rate = learning_rate
        self.discount_rate = discount_rate
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_minimum = epsilon_minimum


    #* Create a 8 by 8 states q-learning table with 4 choices (Up, Right, Down, Left)
    # 0 - Left; 1 - Down; 2 - Right; 3 - Up
    def _init_q_table(self, height=8, width=8):
        return np.zeros(shape=(height,width,4))

    #* Save Q-table 

    #* Train Q-Learning Agent              
    def train(self, num_of_episodes, fps=10):
        env = Pitfalls()
        render = False

        print("[*] Commencing Q-Learn Training...")

        for eps in range(0, num_of_episodes):
            env.reset()
            prev_observation = []

            # Epsilon - Exploration vs Exploitation

            # For each game
            while True:
                # Render current game
                if render:
                    env.render_text()
                    time.sleep(1/fps)

                # Turn on render when 'spacebar' is pressed
                if keyboard.is_pressed('spacebar'):
                    render = True
                    print("[~] Epsilon value:", self.epsilon)

                # Determine action
                if np.random.random() > max(self.epsilon_minimum, self.epsilon) and len(prev_observation) > 0:
                    action = np.argmax(self.q_table[prev_observation])
                    self.epsilon *= self.epsilon_decay
                else:
                    action = env.action_space_sample()

                #* Perform an action
                observation, reward, done, info = env.step(action)

                #* Update Q-table
                if len(prev_observation) > 0 and observation != None:
                    # Reached the goal
                    if done and reward == 100:
                        self.q_table[(prev_observation)][action] = 100 # Goal reward is 0; no penalty
                        
                        #debug
                        print("[+] Q-Learning agent reached the goal at episode {EPS}!".format(EPS=eps))
                        #print(self.q_table)
                        #print("Prev obs: {PREV}; Action: {ACTION}".format(PREV=prev_observation, ACTION=action))

                        break
                    # Reached a Hole or standard tile
                    else:
                        self.update_q_table(prev_observation, action, reward, observation)

                #* Keep a record of previous observation
                if observation != None:
                    prev_observation = observation
                else:
                    # Move not counted, recover the epilson value lost in decay
                    pass #! temp
                    #self.epsilon /= self.epsilon_decay
                    #self.epsilon = min(0.9, self.epsilon)

                if done:
                    render=False
                    break
        
            #? Report progress
            if (eps-1) % 1000 == 0 and eps != 1:
                print("[*] Completed {EPS}/{TOTAL} episodes of training.".format(EPS=eps-1, TOTAL=num_of_episodes))

    #* Update of Q value in the Q-table
    def update_q_table(self, state, action, reward, future_state):
        current_q_value = self.q_table[tuple(state)][action]
        max_future_q = np.max(self.q_table[tuple(future_state)])

        # Update: #?q-value = current q-value + lr x [reward + max expected future reward + current q-value ]
        self.q_table[tuple(state)][action] = (1 - self.learning_rate )* current_q_value + self.learning_rate * (reward + self.discount_rate*max_future_q)

        return

    #* Infer from trained q-table
    def play(self, num_of_times=5, fps=5):
        env = Pitfalls()
        print("[+] Playing from trained data!")

        for eps in range(0, num_of_times):
            env.reset()
            prev_observation = []

            while True:
                # Render
                env.render_text()
                time.sleep(1/fps)

                # Action inferred
                if len(prev_observation) > 0:
                    action = np.argmax(self.q_table[prev_observation])

                    #debug
                    #print("[PLAY] Chosen action:", action)

                else:
                    action = env.action_space_sample()

                try:                
                    observation, reward, done, info = env.step(action)

                except:
                    print("[!] Exception:", sys.exc_info()[:3])
                    print("    -> action:", action)
                    sys.exit()

                #* Keep a record of previous observation
                if observation != None:
                    prev_observation = observation

                if done:
                    print("[+] Game ended in {EPS} episodes.".format(EPS=eps), info)
                    break

            time.sleep(1)




#? Test bed
if __name__ == "__main__":
    #* Test agent
    qla = QLearnAgent(learning_rate=0.05, discount_rate=0.95, epsilon = 0.9, epsilon_decay = 0.99999, epsilon_minimum=0.3)

    #print(qla.q_table)
    #sys.exit(1)

    #* Cumulative training

    qla.train(15000)
    #qla.save()

    qla.play(fps=10, num_of_times=5)
    
    #observation, reward, done, _ = env.step(2)
    #print(observation,reward,done, _)
    #env.render()

    #* T
    #? print(env.__dict__)
    #{'env': <gym.envs.toy_text.frozen_lake.FrozenLakeEnv object at 0x000001AC13CF8640>, 'action_space': Discrete(4), 'observation_space': Discrete(64), 'reward_range': (0, 1), 'metadata': {'render.modes': ['human', 'ansi']}, '_max_episode_steps': 200, '_elapsed_steps': None}