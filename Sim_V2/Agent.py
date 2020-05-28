import numpy as np
import random

class Agent:
    #-- Agent class, with two main variables: language and history

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
        self.groom = False
        self.gossip = False
        self.gossip_members_list = []
        self.groom_members_list = []
        
        
        self.info_fitness = 0 
        self.fitness = 0

    def calc_info_fitness(self):
        pass

    def calc_social_fitness(self):
        self.social_fitness = len(self.groups)
        

    def func(self, n_people):
        pass

    def calc_fitness(self):
        pass