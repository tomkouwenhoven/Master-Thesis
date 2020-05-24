#-- this is the file with helper functions

import math
import random
import numpy as np

def select_fittest(fitness_list, perc):
    l = len(fitness_list)
    p = int(math.ceil(l * perc))
    return fitness_list[:p], fitness_list[p:l-p], fitness_list[l-p:]

def reproduce(agent_list, mut_prob):
    new_pro_social_list = []
    for agent in agent_list:
        if random.uniform(0,1) <= mut_prob:
            mutation_rate = random.choice([0.05, -0.05])
            new_pro_social_probability = np.clip(agent.pro_social + mutation_rate, 0.01, 0.99) #-- make sure that the pro sociality is not below 0.01 and above 0.99
        # new_go_probability = agent.gossip_prob * (1 + (mutation_rate * direction))
            new_pro_social_list.append((agent.groups[0], new_pro_social_probability))
        else:
                new_pro_social_list.append((agent.groups[0], agent.pro_social))
    return new_pro_social_list

def split_to_groups(args, population):
    groups = {}
    for agent in population:
        for group in agent.groups:
            if group in groups.keys():
                groups[group].append(agent)
            else:
                    groups[group] = [agent]    

    return groups    