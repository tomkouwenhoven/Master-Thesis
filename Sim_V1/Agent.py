import numpy as np
import random

class Agent:
    #-- Agent class, with two main variables: language and history

    def __init__(self, _name, _pro_social, _groups):
        self.name = _name
        self.pro_social = _pro_social
        self.history = {}
        self.groups = [_groups]
        self.available = True
        self.social_preference = 0 #-- 0 undecided, 1 in group, 2 out group 

        self.social_fitness = 0

    def calc_info_fitness(self):
        pass

    def calc_social_fitness(self):
        self.social_fitness = len(self.groups)
        

    def func(self, n_people):
        pass

    def calc_fitness(self):
        pass