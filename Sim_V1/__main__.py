# this is the main python code which you should run from terminal

import argparse

from Agent import Agent

import numpy as np
import random

from matplotlib import pyplot as plt

GROUP_ACCEPTANCE = 5
GROUP_REJECTION = .2

def socialize(social_agent, out_group, population):
    # print(f"{social_agent.name} wants to be prosocial, group: {social_agent.groups[0]}")
    
    if out_group:
        #-- the other agents can not be in any of the groups that the social agent is in. 

        # print("out group socializing")

        #-- groups agent 1= [1,2]      agent 2= [3, 5, 2]      agent 3= [3,4,5]
        other_agents = [agent for agent in population if not any(group_number in agent.groups for group_number in social_agent.groups)]
        if other_agents:
            #-- there must be some agents out group before you can socialize with them 
            other = random.choice(other_agents)    
            # print(f"{social_agent.name} with {other.name}")

            #-- here agent.groups[0] is the first element of the groups where agent belongs to. Index 0 is the group which it is born into. 
            social_agent.history[other.groups[0]] = social_agent.history[other.groups[0]] + 1 if other.groups[0] in social_agent.history else 1
            other.history[social_agent.groups[0]] = other.history[social_agent.groups[0]] + 1 if social_agent.groups[0] in other.history else 1

    else: 
        #-- an agent plays save, and communicates with in group members. 

        # print("in group socializing")
        other_agents = [agent for agent in population if any(group_number in social_agent.groups for group_number in agent.groups) and agent is not social_agent]
        other = random.choice(other_agents)

        # print(f"agent {social_agent.name, social_agent.groups} with {other.name, other.groups}")

        social_agent.history[other.groups[0]] = social_agent.history[other.groups[0]] + 1 if other.groups[0] in social_agent.history else 1
        other.history[social_agent.groups[0]] = other.history[social_agent.groups[0]] + 1 if social_agent.groups[0] in other.history else 1

def check_groups(args, population, groups):
    
    # print(np.append(groups[0], population[0]))
    for agent in population:
        added = False
        
        for key in agent.history:
            if agent.history[key] >= GROUP_ACCEPTANCE and key not in agent.groups:
                agent.groups.append(key) #-- add to agent's personal list
                groups[key].append(agent) #-- add to general group list
                added = True    
        
        #-- you can not become rejected from your innate group
        new_groups = [group for group in agent.groups[1:] if agent.history[group] >= GROUP_ACCEPTANCE]
        if new_groups and not added: #-- can only be rejected if you are not adding new groups
            if random.uniform(0,1) <= GROUP_REJECTION:
                #-- an agent is deleted from a random group
                remove_group = random.choice(new_groups) 

                agent.groups.remove(remove_group) #-- remove from agent's personal list
                del agent.history[remove_group] #-- remove from agent's history

                groups[remove_group].remove(agent) #-- remove from general group list

def run_rounds(args, population, groups):
    
    for agent in population:
        if random.uniform(0,1) < agent.pro_social:
            #-- socialize out group
            socialize(social_agent = agent, out_group = True, population = population)
        else:
            #-- socialize in group
            socialize(social_agent = agent, out_group = False, population = population)
    
    check_groups(args, population, groups)



def run(args):
    population = []

    group_sizes = np.zeros((args.ngroups, args.nrounds))

    for i in range(args.nagents):
        population.append(Agent(_name = i, _pro_social = args.prosocial))

    groups = np.split(np.array(population), args.ngroups)
    groups = np.array(groups).tolist()

    for i, group in enumerate(groups):
        for agent in group:
            agent.groups.append(i)

    for r in range(args.nrounds):
        print(f'Round: {r}', sep=' ', end='\r')
        run_rounds(args, population, groups)
        
        for i, group in enumerate(groups):
            group_sizes[i][r] = len(group)
    
    # print("------------ END -------------")
        # for a in population:
        #     print(a.name, a.groups, a.history)  

    for i, line in enumerate(group_sizes):
        plt.plot(line, label = i)
    plt.ylabel("Group size")
    plt.xlabel("Rounds")
    plt.title(f"Group size plot, agents: {args.nagents}")
    plt.grid()
    plt.legend()
    plt.savefig(f'/Users/Tom/Desktop/Thesis/Sim_V1/output/07-05-{args.nagents}-{args.ngroups}-{args.nrounds}')
    plt.show()



def main(args = None):
    #-- 

    parser = argparse.ArgumentParser(description="process some values")
    parser.add_argument('--nagents', '-na', type = int, dest = 'nagents', help = 'The starting population size', default = 10)
    parser.add_argument('--prosocial', '-ps', type = int, dest = 'prosocial', help = 'The starting pro sociality chance for each agent', default = 0.2)
    parser.add_argument('--ngroups', '-ng', type = int, dest = 'ngroups', help = 'The starting number of groups', default = 5)
    parser.add_argument('--generations', '-g', type = int, dest = 'generations', help ='The number of generations', default = 200)
    parser.add_argument('--nrounds', '-nr', type = int, dest = 'nrounds', help ='The number rounds for each generation', default = 5)
    args = parser.parse_args()

    print(args)
        
    run(args)

if __name__ == "__main__":
    main()

