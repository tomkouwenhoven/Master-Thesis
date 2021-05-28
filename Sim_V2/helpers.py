#-- this is the file with helper functions

from Agent import Agent

import math
import random
import numpy as np

event_no = 0

def select_fittest(fitness_list, perc):
    l = len(fitness_list)
    p = int(math.ceil(l * perc))
    return fitness_list[:p], fitness_list[p:l-p], fitness_list[l-p:]

def reproduce(agent_list, mut_prob):
    new_tolerance_list = []
    for agent in agent_list:
        if random.uniform(0,1) <= mut_prob:
            mutation_rate_social = random.choice([0.05, -0.05])
            mutation_rate_go_prob = random.choice([0.05, -0.05])

            new_tolerance_probability = np.clip(agent.tolerance + mutation_rate_social, 0.01, 0.99) #-- make sure that the tolerance is not below 0.01 and above 0.99
            new_gossip_probability = np.clip(agent.gossip_prob + mutation_rate_go_prob, 0.01, 0.99) #-- make sure that the probability is not below 0.01 and above 0.99
        # new_go_probability = agent.gossip_prob * (1 + (mutation_rate_social * direction))
            new_tolerance_list.append((agent.groups[0], new_tolerance_probability, new_gossip_probability))
        else:
                new_tolerance_list.append((agent.groups[0], agent.tolerance, agent.gossip_prob))
    return new_tolerance_list

def split_to_groups(args, population):
    groups = {}
    for i in range(args.ngroups):
        groups[i] = []

    for agent in population:
        for group in agent.groups:
            
            groups[group].append(agent)


    return groups    

def regroup_agents(args, population, groups, GROUP_REJECTION):
    #-- This function checks for each infividual agent to which groups he belongs. He can be added to a group, stay in his groups or be removed from one

    for agent in population:
        added = False
        agent.social_preference = 0

        for key in agent.history:
            group_acceptance = len(groups[key]) / 2 #-- The number of agents of a group should you have spoken before you get accepted into a group 
            
            if agent.history[key] >= group_acceptance and key not in agent.groups:
                agent.groups.append(key) #-- add to agent's personal list
                added = True

        new_groups = [group for group in agent.groups[1:] if agent.history[group] >= group_acceptance]
        if new_groups and not added: #-- can only be rejected if you are not adding new groups
            if random.uniform(0,1) <= GROUP_REJECTION:
                #-- an agent is deleted from a random group
                
                remove_group = random.choice(new_groups) 

                # print(f'going to remove {agent.name} from {remove_group}')
                agent.groups.remove(remove_group) #-- remove from agent's personal list
                del agent.history[remove_group] #-- remove from agent's history

def groom(social_agent, population, out_group, max_invited):
    #-- Grooming is one-to-ONE and is only possible if both agents are not active in another grooming or gossiping event.
    #-- This function takes a social agent, the population and the fact whether an agent socializes out group or in group. 
    #-- It first determines if there are agents to groom, out or in group. Then adds the event to the memories, lastly it updates the encounters with groups. 
    
    global event_no

    actual_participants = []

    # print(f'Grooming event: {event_no} out group: {out_group}')

    # print(f'social agent {social_agent.name} from group: {social_agent.groups[0]}')

    if out_group:
        # print('outgroup grooming')
        #-- the other agents are only from other groups. 
        social_agent.social_preference = 2 #-- out group preference
       
        possible_participants = get_participants(social_agent, population, True, max_invited)
        if possible_participants:
            # print([agent.name for agent in possible_participants])

            for other_agent in possible_participants:
                
                preference = other_agent.social_preference if other_agent.social_preference !=0 else determine_preference(other_agent)
                # print(f'preference other: {preference}')
                
                if preference == 2:
                    # print(f'agent: {other_agent.name} accepts')
                    other_agent.social_preference = preference

                    actual_participants.append(other_agent)
                
                else:
                    #-- other agent does not want to gossip out group and rejects. 
                    #-- preference of an agent should be stored for next possible events. 

                    # print(f'agent: {other_agent.name} rejects')
                    other_agent.social_preference = preference
                    other_agent.available = False

    else:
        #-- the other agents are only from known groups. 
        # print('in group grooming')
        social_agent.social_preference = 1 #-- in group preference

        possible_participants = get_participants(social_agent, population, False, max_invited)
        if possible_participants:
            # print([agent.name for agent in possible_participants])
            for other_agent in possible_participants:
                
                preference = other_agent.social_preference if other_agent.social_preference !=0 else determine_preference(other_agent)
                # print(f'preference other: {preference}')
                
                if preference == 1:
                    # print(f'agent: {other_agent.name} accepts')
                    other_agent.social_preference = preference

                    actual_participants.append(other_agent)
                
                else:
                    #-- other agent does want to gossip out group and rejects. 
                    #-- preference of an agent should be stored for next possible events. 
                    # print(f'agent: {other_agent.name} rejects')
                    other_agent.social_preference = preference
                    other_agent.available = False

    if actual_participants:
        grooming_agents = [social_agent] + actual_participants
        
        #-- Add the gossiping event itself to everyones memory and history 
        add_event_to_mem(grooming_agents, [f'event_{event_no}'])
        add_interaction_to_hist(grooming_agents)

        #-- Make sure that none of the agents can engage in other social activities. 
        for agent in grooming_agents:
            agent.available = False
            agent.groom_members_list.append(len(grooming_agents))

        #-- 4 observers can observe the event, however, if you are in the event you can not observe the event itself. 
        available_observers = [a for a in population if a not in grooming_agents]
        observers = random.sample(available_observers, 4 if 4 < len(available_observers) else len(available_observers))

        # print(f"grooming {event_no} done by: {[a.name for a in grooming_agents]} is observed by: {[a.name for a in observers]}")

        #-- add event to the memories of the observers
        for observer in observers:
            observe(observer, event_no)

        event_no += 1
    
def gossip(social_agent, population, out_group, max_invited):
    #-- Gossiping is one-to-MANY with a maximum of 3 others. It is only possible if all agents are not active in another grooming or gossiping event.
    
    global event_no

    actual_participants = []

    # print(f'Gossip event: {event_no} out group: {out_group}')

    # print(f'social agent {social_agent.name} from group: {social_agent.groups[0]}')

    if out_group:
        #-- the other agents are only from other groups. 
        social_agent.social_preference = 2 #-- out group preference
       
        possible_participants = get_participants(social_agent, population, True, 3)
        if possible_participants:
            for other_agent in possible_participants:
                preference = other_agent.social_preference if other_agent.social_preference !=0 else determine_preference(other_agent)
                # print(f'preference other: {preference}')
                
                if preference == 2:
                    # print(f'agent: {other_agent.name} accepts')
                    other_agent.social_preference = preference

                    actual_participants.append(other_agent)
                
                else:
                    #-- other agent does not want to gossip out group and rejects. 
                    #-- preference of an agent should be stored for next possible events. 

                    # print(f'agent: {other_agent.name} rejects')
                    other_agent.social_preference = preference
                    other_agent.available = False

    else:
        #-- the other agents are only from known groups. 

        social_agent.social_preference = 1 #-- in group preference

        possible_participants = get_participants(social_agent, population, False, 3)
        if possible_participants:
            
            for other_agent in possible_participants:
                
                preference = other_agent.social_preference if other_agent.social_preference !=0 else determine_preference(other_agent)
                # print(f'preference other: {preference}')
                
                if preference == 1:
                    # print(f'agent: {other_agent.name} accepts')
                    other_agent.social_preference = preference

                    actual_participants.append(other_agent)
                
                else:
                    #-- other agent does want to gossip out group and rejects. 
                    #-- preference of an agent should be stored for next possible events. 
                    # print(f'agent: {other_agent.name} rejects')
                    other_agent.social_preference = preference
                    other_agent.available = False

    if actual_participants:
        gossiping_agents = [social_agent] + actual_participants

        # #-- Pick gossiping agent and share memory
        info_agent = random.choice(gossiping_agents)
        shared_events = random.sample(info_agent.memory, 10 if 10 < len(info_agent.memory) else len(info_agent.memory))
        add_by_gossip(gossiping_agents, shared_events)
        
        #-- Add the gossiping event itself to everyones memory and history 
        add_event_to_mem(gossiping_agents, [f'event_{event_no}'])
        add_interaction_to_hist(gossiping_agents)

        #-- Make sure that none of the agents can engage in other social activities. 
        for agent in gossiping_agents:
            agent.available = False
            agent.gossip_members_list.append(len(gossiping_agents))

        #-- 4 observers can observe the event, however, if you are in the event you can not observe the event itself. 
        available_observers = [a for a in population if a not in gossiping_agents]
        observers = random.sample(available_observers, 4 if 4 < len(available_observers) else len(available_observers))

        # print(f"gossip {event_no} done by: {[a.name for a in gossiping_agents]} is observed by: {[a.name for a in observers]}")

        #-- add event to the memories of the observers
        for observer in observers:
            observe(observer, event_no)

        event_no += 1


def add_interaction_to_hist(agents):
    #-- here agent.groups[0] is the first element of the groups where agent belongs to. Index 0 is the group which it is born into. 
    for agent in agents:
        for other in agents:
            if agent != other:
                agent.history[other.groups[0]] = agent.history[other.groups[0]] + 1 if other.groups[0] in agent.history else 1

def add_event_to_mem(agents, events):
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
    observer.memory.append(f'event_{event_name}')

def determine_preference(agent):
    #-- 0 undecided, 1 in group, 2 out group
    return 2 if random.uniform(0,1) < agent.tolerance else 1

def get_participants(social_agent, population, out_group, max_participants):

    if out_group:
        #-- from outside known groups
        available_agents = [agent for agent in population if not any(group_number in agent.groups for group_number in social_agent.groups) and agent.available]
    else: 
        #-- from within know groups
        available_agents = [agent for agent in population if any(group_number in agent.groups for group_number in social_agent.groups) and agent is not social_agent and agent.available]

    #-- determine with how many and with who the social agent will gossip. 
    # num_participants = random.randint(1,max_participants)
    num_participants = max_participants
    if num_participants > len(available_agents):
        num_participants = len(available_agents)
    if num_participants != 0:    
        possible_participants = random.sample(available_agents, num_participants)
        # print(f'social agent: {social_agent.name} with gossipers:{[a.name for a in possible_participants]}')
        
        return possible_participants
    else: 
        return []
     
def get_group_values(groups):
    # print(groups)
    avg_gp_per_group = {}
    avg_tol_per_group = {}
    for key in groups:
        if len(groups[key]) > 0:

        # print(key, groups[key])
            avg_gp, avg_tol = np.mean([(a.gossip_prob, a.tolerance) for a in groups[key]], axis = 0)
            avg_gp_per_group[key] = avg_gp
            avg_tol_per_group[key] = avg_tol
        else:
            avg_gp_per_group[key] = None
            avg_tol_per_group[key] = None

    sort_by_group_gp = sorted(avg_gp_per_group.items())
    sort_by_group_tol = sorted(avg_tol_per_group.items())

    return list(zip(*sort_by_group_gp))[1], list(zip(*sort_by_group_tol))[1]