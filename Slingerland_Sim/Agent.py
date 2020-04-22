import numpy as np
import random

class Agent:
    #-- Agent class, with two main variables: gossip_prob and memory

    def __init__(self, _name, _gossip_prob):
        self.name = _name
        self.gossip_prob = _gossip_prob
        self.memory = list()
        self.available = True
        self.groom = False
        self.gossip = False
        self.gossip_members_list = []
        self.groom_members_list = []
        self.info_fitness = 0 
        self.social_fitness = 0
        self.fitness = 0

    def calc_info_fitness(self):
        self.info_fitness = len(self.memory) ** 2
        # return self.info_fitness

    def calc_social_fitness(self):
        
        #-- Calculate social fitness acquired through GROOMING
        sum_gr_fitness = 0
        for gr_event in self.groom_members_list:
            sum_gr_fitness += self.func(gr_event)

        #-- Calculate social fitness acquired through GOSSIPING
        sum_go_fitness = 0
        for go_event in self.gossip_members_list:
            sum_go_fitness += self.func(go_event)

        self.social_fitness = (5 * sum_gr_fitness) + (4 * sum_go_fitness)
        # return self.social_fitness

    def func(self, n_people):
        return 1 / (n_people - 1)

    def calc_fitness(self):
        self.calc_info_fitness()
        self.calc_social_fitness()
        self.fitness = self.info_fitness * self.social_fitness
        return self.fitness