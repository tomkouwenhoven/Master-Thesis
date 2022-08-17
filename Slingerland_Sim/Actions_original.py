#TODO

from Agent import Agent
from itertools import combinations

import numpy as np
import random
import math


#-- Grooming    
def groom(social_agent, group, event_name):
    #-- Grooming is one-to-ONE and is only possible if both agents are not active in another grooming or gossiping event.
    if not(social_agent.groom or social_agent.gossip):
        available_participants = [a for a in group if not(a.groom or a.gossip) and a is not social_agent]
        # print(f'available_names:{[a.name for a in available_participants]}'')

        if available_participants:
            
            #-- Determine the one other participant to groom with 
            other_agent = random.choice(available_participants)

            add_to_mem([social_agent, other_agent], [event_name])
            social_agent.groom_members_list.append(2)
            other_agent.groom_members_list.append(2)
            
            # print(f'grooming: {social_agent.name, other_agent.name}')

            #-- 4 observers can observe the event, however, if you are in the event you can not observe the event itself. 
            available_observers = [a for a in group if a is not social_agent and a is not other_agent]
            observers = random.sample(available_observers, 4 if 4 < len(available_observers) else len(available_observers))

            #-- add event to the memories of the observers
            for observer in observers:
                observe(observer, event_name)

            #-- Make sure that none of the agents can engage in other social activities. 
            social_agent.groom = True
            other_agent.groom = True
            

#-- Gossiping
def gossip(social_agent, group, event_name):
    #-- Gossiping is one-to-MANY with a maximum of 3 others. It is only possible if all agents are not active in another grooming or gossiping event.
    if not(social_agent.groom or social_agent.gossip):
        available_participants = [a for a in group if not(a.groom or a.gossip) and a is not social_agent]
        
        #-- determine with how many and with who the social agent will gossip. 
        num_participants = random.randint(1,3)
        # num_participants = random.randint(1,3) #-- ORIGINEEL
        if num_participants > len(available_participants):
            num_participants = len(available_participants)
        if num_participants != 0:    
            participants = random.sample(available_participants, num_participants)
            # print(f'social agent: {social_agent.name} with gossipers:{[a.name for a in participants]}')
            gossiping_agents = [social_agent] + participants
            
            #-- Pick gossiping agent and share memory
            info_agent = random.choice(gossiping_agents)
            shared_events = random.sample(info_agent.memory, 10 if 10 < len(info_agent.memory) else len(info_agent.memory))
            add_by_gossip(gossiping_agents, shared_events)

            #-- Add the gossiping event itself to everyones memory
            add_to_mem(gossiping_agents, [event_name])
            
            #-- 4 observers can observe the event, however, if you are in the event you can not observe the event itself. 
            available_observers = [a for a in group if a not in gossiping_agents]
            observers = random.sample(available_observers, 4 if 4 < len(available_observers) else len(available_observers))
            # print(f'{event_name} being observed by: {[a.name for a in observers]}')
            for observer in observers:
                observe(observer, event_name)

            #-- Make sure that none of the agents can engage in other social activities. 
            for a in gossiping_agents:
                a.gossip = True
                a.gossip_members_list.append(len(gossiping_agents))

def add_to_mem(agents, events):
    #-- only add events that are not in memory yet
    for a in agents:
        new_memories = [event for event in events if event not in a.memory] 
        a.memory += new_memories

def add_by_gossip(agents, events):
    #-- add events that are not in memory yet
    #-- without the number of the agents for calulation purposes. 
    for a in agents:
        new_memories = [event for event in events if event not in a.memory] 
        a.memory += new_memories
        # a.event_members_list.append(len(agents))

def observe(observer, event_name):
    observer.memory.append(event_name)

def reproduce(agent, mut_prob):
        if random.uniform(0,1) <= mut_prob:
            mutation_rate = random.choice([0.05, -0.05])
            # mutation_rate = random.uniform(0.95, 1.051) #-- maximum of 5% change in gossip prob
            # new_go_probability = agent.gossip_prob * mutation_rate
            new_go_probability = np.clip(agent.gossip_prob + mutation_rate, 0.01, 0.99)
        # new_go_probability = agent.gossip_prob * (1 + (mutation_rate * direction))
            return new_go_probability
        else:
            return agent.gossip_prob

def select_fittest(fitness_list, perc):
    l = len(fitness_list)
    p = int(math.ceil(l * perc))
    return fitness_list[:p], fitness_list[p:l-p], fitness_list[l-p:]
    
