#-- TODO 
# - Locations update
# - Directions


import numpy as np
import random

from sklearn.metrics.pairwise import euclidean_distances

class Agent:
    def __init__(self, name, hp, speed):
        self.name = name
        # self.xPos = np.random.randint(low=1, high=50)
        # self.yPos = np.random.randint(low=1, high=50)
        self.xPos = 10
        self.yPos = 15
        self.hp = hp
        self.speed = speed
        self.memory = [] #-- list 
        self.inventory = []

    def Move(self):

        self.xPos += np.random.randint(low=-self.speed, high=self.speed)
        self.yPos += np.random.randint(low=-self.speed, high=self.speed)

        if self.xPos > 50:
            self.xPos = self.xPos - 50
        if self.xPos < 0:
            self.xPos = self.xPos + 50
        if self.yPos > 50:
            self.yPos = self.yPos - 50
        if self.yPos < 0:
            self.yPos = self.yPos + 50

    def FindFood(self, foods):
        foodsAvailable = list(filter(lambda x: foods[x].availability > 0, foods))
        fruitsInHood = [foods[fruit].Type for fruit in foodsAvailable if euclidean_distances([[foods[fruit].xPos, foods[fruit].yPos]], [[self.xPos, self.yPos]]) < 5]
        # fruitsInHood = [foods[fruit].Type for fruit in foods if euclidean_distances([[foods[fruit].xPos, foods[fruit].yPos]], [[self.xPos, self.yPos]]) < 5]


        for fruit in fruitsInHood:
            self.PickUp(fruit, foods)

        if not self.memory: #-- empty 
            for fruit in fruitsInHood:
                self.memory.append([fruit, (foods[fruit].xPos, foods[fruit].yPos)])
        else:
            for i, fruit in enumerate(fruitsInHood):
                if fruit not in self.memory[i]:
                    self.memory.append([fruit, (foods[fruit].xPos, foods[fruit].yPos)])


    def EatFood(self, foods, foodToEat):
        # print(np.random.randint(low=0, high=len(self.inventory)))
        # self.inventory[0] = ['apple', 0]
        # filteredInv = list(filter(lambda x: x[1] > 0, self.inventory)) #-- only the food that i have 
        # if filteredInv:
            # print(np.random.randint(low=0, high=len(filteredInv)))
            
            # foodToEat = filteredInv[np.random.randint(low=0, high=len(filteredInv))] #-- random item from inventory 
            print(f' I am going to eat an: {foodToEat[0]} and I will gain {foods[foodToEat[0]].foodValue}')

            self.hp += foods[foodToEat[0]].foodValue
            
            idx = self.index_2d(self.inventory, foodToEat[0])
            self.inventory[idx[0]] = [foodToEat[0], self.inventory[idx[0]][1] - 1]



    def index_2d(self, myList, v):
            for i, x in enumerate(myList):
                if v in x:
                    return (i, x.index(v))    

    def PickUp(self, fruit, foods):
        # print(fruit)
        print(f'I just picked up an {fruit}')
        if not self.inventory:
            self.inventory.append([fruit, 1])

        if not fruit in (item[0] for item in self.inventory):
            self.inventory.append([fruit, 1])
        else: 
            idx = self.index_2d(self.inventory, fruit)
            self.inventory[idx[0]] = [fruit, self.inventory[idx[0]][1] + 1]
        foods[fruit].availability -= 1 

    def Live(self, foods):
        # self.Move()
        # self.FindFood(foods)
        filteredInv = list(filter(lambda x: x[1] > 0, self.inventory))
        
        if self.hp < 4: #-- food available
            if filteredInv:
                foodToEat = filteredInv[np.random.randint(low=0, high=len(filteredInv))] #-- random item from inventory 
                # pass
        #         # print(f'I want to eat an: {foodToEat}')
                self.EatFood(foods, foodToEat)
            else:
                self.Move()
                self.FindFood(foods)
                self.hp -= 1
        else:
            self.Move()
            self.FindFood(foods)
            self.hp -= 1
