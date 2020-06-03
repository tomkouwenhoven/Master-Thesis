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

        self.gossip_prob = _gossip_prob
        self.memory = list()

        self.gossip_members_list = []
        self.groom_members_list = []
        
        self.social_fitness = 0
        self.info_fitness = 0 
        self.fitness = 0

    def calc_info_fitness(self):
        self.info_fitness = len(self.memory) ** 2

    def calc_social_fitness(self):
        # self.social_fitness = len(self.groups) #-- OLD OLD OLD OLD

        #-- Calculate social fitness acquired through GROOMING
        sum_gr_fitness = 0
        for gr_event in self.groom_members_list:
            sum_gr_fitness += self.func(gr_event)

        #-- Calculate social fitness acquired through GOSSIPING
        sum_go_fitness = 0
        for go_event in self.gossip_members_list:
            sum_go_fitness += self.func(go_event)

        self.social_fitness = (5 * sum_gr_fitness) + (4 * sum_go_fitness)

    def func(self, n_people):
        return 1 / (n_people - 1)

    def calc_fitness(self):
        self.calc_info_fitness()
        self.calc_social_fitness()
        self.fitness = self.info_fitness * self.social_fitness
        return self.fitness
