#TODO

from Agent import Agent
from itertools import combinations

import numpy as np
import random
import math


#-- Grooming    

def groom(grooming_agent, group):
    if not(grooming_agent.groom or grooming_agent.gossip):
        available_agents = [agent for agent in group if not(agent.groom or agent.gossip) and agent is not grooming_agent]

        if available_agents:
            other_agent = np.random.choice(available_agents)

            #-- Grooming takes place here
            # print(f'Agent: {grooming_agent.name} grooms with agent: {other_agent.name}')
            grooming_agent.groom = True
            other_agent.groom = True
            
            #-- Add a single event to the memories of both agents. 
            add_events(grooming_agent, [(grooming_agent.name, other_agent.name)])
            add_events(other_agent, [(grooming_agent.name, other_agent.name)])

            grooming_agent.groom_events.append([grooming_agent.name, other_agent.name]) #-- keep track of groom events. 
            other_agent.groom_events.append([other_agent.name, grooming_agent.name])

            # -- select the observers for this event. 
            # available_observers = [agent for agent in group if agent is not other_agent and agent is not grooming_agent]
            # observers = random.sample(available_observers, 4 if 4 < len(available_observers) else len(available_observers))
            # observe(observers, [grooming_agent.name, other_agent.name])

#-- Gossiping
def gossip(gossiping_agent, group):
    # for social_agent in gossiping_agents:
    if not (gossiping_agent.groom and gossiping_agent.gossip):
        available_agents = [agent for agent in group if not(agent.groom or agent.gossip) and agent is not gossiping_agent]
        
        num_other_agents = np.random.randint(1, 4) #-- gossip group size is maximum 4 (self + 3 others)
        if num_other_agents > len(available_agents): 
            num_other_agents = len(available_agents)
        if num_other_agents != 0 :
            other_agents = random.sample(available_agents, num_other_agents) 
            other_agents_names = [agent.name for agent in other_agents]

            # print(f'Agent {gossiping_agent.name} gossips with {other_agents_names}')
            gossip_members = [gossiping_agent.name] + other_agents_names
            # gossip([gossiping_agent], [other_agents])

            #-- a gossiping event happens with up to 3 others, the normal events and shared events are added to each's memory. 
            all_agents = np.concatenate(([gossiping_agent], other_agents), axis=None)
            agent_combinations = [(a.name, b.name) for a, b in list(combinations(all_agents, 2))]    
            
            info_agent = np.random.choice(all_agents) #-- random agent selected to share 10 of its memory items. 
            events_to_share = random.sample(info_agent.memory, 10 if len(info_agent.memory) >= 10 else len(info_agent.memory))    
            events_to_add = list(dict.fromkeys(agent_combinations + events_to_share)) #-- all events to be added by the participating agents in a gossiping event. 

            for a in all_agents:
                a.gossip = True
                add_events(a, events_to_add)
                participants_names = [agent.name for agent in all_agents]
                a.gossip_events.append(participants_names) #-- keep track of gossip events 

            # -- select the observers for this event. 
            # available_observers = [agent for agent in group if agent is not gossiping_agent and agent not in other_agents]
            # observers = random.sample(available_observers, 4 if 4 < len(available_observers) else len(available_observers))
            # observe(observers, gossip_members)


# def groom(initiator, others):
#     #-- Add a single event to the memories of both agents. 
#     print(f'Agent: {initiator.name} grooms with agent: {others[0].name}')
#     initiator.groom = True
#     others[0].groom = True
#     add_events(initiator, [(initiator.name, others[0].name)])
#     add_events(others[0], [(initiator.name, others[0].name)])

#     initiator.groom_events.append([initiator.name, others[0].name]) #-- keep track of groom events. 
#     others[0].groom_events.append([others[0].name, initiator.name])

# def gossip(initiator, others):
#     #-- a gossiping event happens with up to 3 others, the normal events and shared events are added to each's memory. 
#     all_agents = np.concatenate((initiator, others), axis=None)
#     agent_combinations = [(a.name, b.name) for a, b in list(combinations(all_agents, 2))]    
    
#     info_agent = np.random.choice(all_agents) #-- random agent selected to share 10 of its memory items. 
#     events_to_share = random.sample(info_agent.memory, 10 if len(info_agent.memory) >= 10 else len(info_agent.memory))    
#     events_to_add = list(dict.fromkeys(agent_combinations + events_to_share)) #-- all events to be added by the participating agents in a gossiping event. 

#     for a in all_agents:
#         a.gossip = True
#         add_events(a, events_to_add)
#         participants_names = [agent.name for agent in all_agents]
#         a.gossip_events.append(participants_names) #-- keep track of gossip events 

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
        if (random.randint(1,100)/100) <= mut_prob:
            mutation_rate = random.uniform(1.0, 1.051) #-- maximum of 5% change in gossip prob
            new_go_probability = agent.gossip_prob * mutation_rate
        # new_go_probability = agent.gossip_prob * (1 + (mutation_rate * direction))
            return new_go_probability
        else:
            return agent.gossip_prob

def select_fittest(fitness_list, perc):
    l = len(fitness_list)
    p = int(math.ceil(l * perc))
    return fitness_list[:p], fitness_list[p:l-p], fitness_list[l-p:]
    
