# Q-learning Agent plays Pitfalls
## Description
A simple q-learning agent trains via reinforcement learning on a Q-table to learn how to play the game Pitfalls.

## What is the game Pitfalls?
Player starts at top-left-hand corner and must learn to find his/her way down to the goal at bottom-right-hand corner. 
For example:

S F F F

F F F H

F H F H

H F F G


F = normal floor

S = starting / normal floor

H = hole (game ends)

G = Goal (wins! and game ends)


## AI Gym Environment
The Pitfalls game is a special AI environment that behaves similarly to Open AI Gym environments. 