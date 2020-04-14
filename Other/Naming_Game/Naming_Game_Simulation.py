from Agent import Agent
from Game import Game

import numpy as np
import random
import matplotlib.pyplot as plt

agents = []
indexes = []
successes = []
alignment_successes = []

num_agents = 10
num_objects = 8
num_games = 100

for i in range(num_agents):
    agents.append(Agent(_name = i, _xpos = np.random.uniform(500), _ypos = np.random.uniform(500), _speed = 2))
    indexes.append(i)

count_games = 0
total_success = np.zeros(num_games)
total_alignment = np.zeros(num_games)
# temp_successes = np.array(successes)

while(count_games < num_games):
    print(f"--------- Round {count_games} ---------")
    for agent in agents:
        agent.move()
        
    speaker, hearer = random.sample(agents, 2)
    print(f'speaker : {speaker.name}, hearer: {hearer.name}')
    game = Game(speaker, hearer)
    game.play()
    successes.append(game.success)
    alignment_successes.append(game.alignment_success)

    total_success[count_games] = sum(successes)
    total_alignment[count_games] = sum(alignment_successes)

    count_games += 1

# print(total_success)


plt.plot(total_success)
plt.plot(total_alignment)
plt.legend()
plt.grid(True)
plt.show()


# pd.DataFrame(mlp_history.history).plot(figsize=(8, 5))
# plt.grid(True)
# plt.gca().set_ylim(0, 1)
# plt.show()