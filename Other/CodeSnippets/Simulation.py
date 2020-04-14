from AgentClass import Agent
from FoodClass import Food

import numpy as np

agents = []
for i in range(5):
    agents.append(Agent(name = i, hp = 5 , speed = 5)) #-- np.random.randint(low=10, high=15)

apple = Food("apple", xPos = 10, yPos = 15, foodValue = 3, availability = 5)
pear = Food("pear", xPos = 5, yPos = 40, foodValue = 5, availability = 5)
banana = Food("banana", xPos =  40, yPos = 20, foodValue = 4, availability = 1)


# foods = [[1, apple], [1, pear], [2, banana]]
foods = {"apple" : apple, "pear" : pear, "banana" : banana}
# foods = [apple, pear, banana]
# print(foods)

print("Start simulation")
# print(foods)
print('\n')
    
for round in range(15):
    print(f'---------- Round number: {round} ----------')

    for agent in agents:
        # print(len(agent.inventory))
        foodsAvailable = list(filter(lambda x: foods[x].availability > 0, foods))
        agent.Live(foods)
        print(f'Agent: {agent.name}, location: {(agent.xPos, agent.yPos)}, health: {agent.hp}, Food Location: {agent.memory}, Inventory: {agent.inventory}')
    print(apple.availability, pear.availability, banana.availability)
    
    agents = [agent for agent in agents if agent.hp > 0]
    # print(foods["apple"])

    print('---------- END ROUND ---------- \n\n')

        # a = [1, 2, 3, 4, 5, 6]
        # filter(lambda x : x % 2 == 0, a) # Output: [2, 4, 6]

        # dict_a = [{'name': 'python', 'points': 10}, {'name': 'java', 'points': 8}]

        # filter(lambda x : x['name'] == 'python', dict_a) # Output: [{'name': 'python', 'points': 10}]
