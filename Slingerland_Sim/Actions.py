#TODO

from Agent import Agent
from itertools import combinations

import numpy as np
import random
import math


#-- Grooming    

def groom_all(grooming_agents, group):
    for social_agent in grooming_agents: 
        if social_agent.available:
            # other_agents = []
            available_agents = [agent for agent in group if agent.available and agent is not social_agent]

            if available_agents:
                other_agent = np.random.choice(available_agents)

                groom(initiator = social_agent, others = [other_agent])

                available_observers = [agent for agent in group if agent is not other_agent and agent is not social_agent]
                observers = random.sample(available_observers, 4 if 4 < len(available_observers) else len(available_observers))
                observe(observers, [social_agent.name, other_agent.name])

#-- Gossiping
def gossip_all(gossiping_agents, group):
    for social_agent in gossiping_agents:
        if social_agent.available:
            # social_agent.available = False
            available_agents = [agent for agent in group if agent.available and agent is not social_agent]
            
            num_other_agents = np.random.randint(1, 4) #-- gossip group size is maximum 4 (self + 3 others)
            if num_other_agents > len(available_agents): 
                num_other_agents = len(available_agents)
            
            if num_other_agents != 0 :
                other_agents = random.sample(available_agents, num_other_agents) 
                other_agents_names = [agent.name for agent in other_agents]

                gossip_members = [social_agent.name] + other_agents_names
                gossip([social_agent], [other_agents])

                available_observers = [agent for agent in group if agent is not social_agent and agent not in other_agents]
                observers = random.sample(available_observers, 4 if 4 < len(available_observers) else len(available_observers))
                observe(observers, gossip_members)


def groom(initiator, others):
    #-- Add a single event to the memories of both agents. 
    initiator.available = False
    others[0].available = False
    add_events(initiator, [(initiator.name, others[0].name)])
    add_events(others[0], [(initiator.name, others[0].name)])

    initiator.groom_events.append([initiator.name, others[0].name]) #-- keep track of groom events. 
    others[0].groom_events.append([others[0].name, initiator.name])

def gossip(initiator, others):
    #-- a gossiping event happens with up to 3 others, the normal events and shared events are added to each's memory. 
    # print(f'{initiator[0].name} going to gossip with {others[0]} group size = {1 + len(others[0])}')
    all_agents = np.concatenate((initiator, others), axis=None)
    agent_combinations = [(a.name, b.name) for a, b in list(combinations(all_agents, 2))]    
    
    info_agent = np.random.choice(all_agents) #-- random agent selected to share 10 of its memory items. 
    events_to_share = random.sample(info_agent.memory, 10 if len(info_agent.memory) >= 10 else len(info_agent.memory))    
    events_to_add = list(dict.fromkeys(agent_combinations + events_to_share)) #-- all events to be added by the participating agents in a gossiping event. 

    for a in all_agents:
        a.available = False
        add_events(a, events_to_add)
        participants_names = [agent.name for agent in all_agents]
        a.gossip_events.append(participants_names) #-- keep track of gossip events 

def observe(observers, event_members):
    agent_combinations = list(combinations(event_members, 2))
    
    for observer in observers:
        # print(f'Agent:{observer.name} observes : {agent_combinations} with memory: {observer.memory}')
        add_events(observer, agent_combinations)
        # print(f'Agent:{observer.name} with memory: {observer.memory}')
    # pass

def add_events(current_agent, events):
    #-- only add events that are not in memory yet

    new_events = [event for event in events if ((event[0], event[1]) not in current_agent.memory) and ((event[1], event[0]) not in current_agent.memory)] 
    current_agent.memory += new_events

def reproduce(agent, mut_prob, mut_rate):
        mutation_rate = random.randint(1, mut_rate) / 100 if (random.randint(1,100)/100) <= mut_prob else 0 #-- maximum of 5% change in gossip prob
        direction = 1 if random.random() > .5 else -1 #--HERE?
        # new_go_probability = agent.gossip_prob + ((agent.gossip_prob * mutation_rate) * direction)
        new_go_probability = agent.gossip_prob * (1 + (mutation_rate * direction))

        return new_go_probability

def select_fittest(fitness_list, perc):
    l = len(fitness_list)
    p = int(math.ceil(l * perc))
    return fitness_list[:p], fitness_list[p:l-p], fitness_list[l-p:]
    
