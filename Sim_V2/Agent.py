import numpy as np
import random

class Agent:
    #-- Agent class, with two main variables: gossip probability and prosocial 

    def __init__(self, _name, _pro_social, _groups, _gossip_prob):
        self.name = _name
        self.pro_social = _pro_social
        self.history = {}
        self.groups = [_groups]
        self.available = True
        self.social_preference = 0 #-- 0 undecided, 1 in group, 2 out group 

        self.social_fitness = 0

        self.gossip_prob = _gossip_prob
        self.memory = list()

        self.gossip_members_list = []
        self.groom_members_list = []
        
        self.info_fitness = 0 
        self.fitness = 0

    def calc_info_fitness(self):
         self.info_fitness = len(self.memory) ** 2

    def calc_social_fitness(self):
        self.social_fitness = len(self.groups)

    def func(self, n_people):
        return 1 / (n_people - 1)

    def calc_fitness(self):
        pass