import numpy as np
import random

class Agent:
    #-- Agent class, with two main variables: language and history

    def __init__(self, _name, _pro_social):
        self.name = _name
        self.pro_social = _pro_social
        self.history = {}

    def calc_info_fitness(self):
        pass

    def calc_social_fitness(self):
        pass

    def func(self, n_people):
        pass

    def calc_fitness(self):
        pass