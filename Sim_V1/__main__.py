# this is the main python code which you should run from terminal

##TODO
# - 5% geen kinderen —> is na reproduce elke groep nog gevuld?
# - Maximaal aantal groepen voor 1 agent 

import argparse

from Agent import Agent
from helpers import select_fittest, reproduce

import numpy as np
import random

from matplotlib import pyplot as plt


GROUP_REJECTION = .2
MUTATION_PROB = .2
SELECTION = False

def socialize(social_agent, out_group, population):
    # print(f"{social_agent.name} wants to be prosocial, group: {social_agent.groups[0]}")
    
    if out_group:
        #-- the other agents can not be in any of the groups that the social agent is part of. 

        # print("out group socializing")

        #-- groups agent 1= [1,2]      agent 2= [3, 5, 2]      agent 3= [3,4,5]
        other_agents = [agent for agent in population if not any(group_number in agent.groups for group_number in social_agent.groups) and agent.available]
        if other_agents:
            #-- there must be some agents out group before you can socialize with them 
            other = random.choice(other_agents)    
            
            # print(f"agent {social_agent.name} with {other.name}")

            social_agent.available = False
            other.available = False

            #-- here agent.groups[0] is the first element of the groups where agent belongs to. Index 0 is the group which it is born into. 
            social_agent.history[other.groups[0]] = social_agent.history[other.groups[0]] + 1 if other.groups[0] in social_agent.history else 1
            other.history[social_agent.groups[0]] = other.history[social_agent.groups[0]] + 1 if social_agent.groups[0] in other.history else 1

    else: 
        #-- an agent plays save, and communicates with in group members. 
        # print("in group socializing")
        other_agents = [agent for agent in population if any(group_number in social_agent.groups for group_number in agent.groups) and agent is not social_agent and agent.available]
        if other_agents:
            other = random.choice(other_agents)

            # print(f"agent {social_agent.name} with {other.name}")

            social_agent.available = False
            other.available = False
            
            #-- here agent.groups[0] is the first element of the groups where agent belongs to. Index 0 is the group which it is born into. 
            social_agent.history[other.groups[0]] = social_agent.history[other.groups[0]] + 1 if other.groups[0] in social_agent.history else 1
            other.history[social_agent.groups[0]] = other.history[social_agent.groups[0]] + 1 if social_agent.groups[0] in other.history else 1

def check_groups(args, population, groups):
    
    # print(np.append(groups[0], population[0]))
    for agent in population:
        added = False
        
        for key in agent.history:
            # print(agent.name, key, len(groups[key]))
            group_acceptance = len(groups[key]) / 2 #-- The number of agents of a group should you have spoken before you get accepted into a group 
            if agent.history[key] >= group_acceptance and key not in agent.groups:
                agent.groups.append(key) #-- add to agent's personal list
                groups[key].append(agent) #-- add to general group list
                added = True    
        
        
        #-- THis can be done quicker with random.choice
        #-- you can not become rejected from your innate group
        new_groups = [group for group in agent.groups[1:] if agent.history[group] >= group_acceptance]
        if new_groups and not added: #-- can only be rejected if you are not adding new groups
            if random.uniform(0,1) <= GROUP_REJECTION:
                #-- an agent is deleted from a random group
                remove_group = random.choice(new_groups) 

                agent.groups.remove(remove_group) #-- remove from agent's personal list
                del agent.history[remove_group] #-- remove from agent's history

                groups[remove_group].remove(agent) #-- remove from general group list

def run_round(args, population, groups):
    #-- runs a single round where agents can engage with each other. 

    for agent in population:
        if agent.available: #-- an agents can only socialize when he is not already socializing. 
            # print([(a.name, a.available) for a in population])
            if random.uniform(0,1) < agent.pro_social:
                #-- socialize out group
                socialize(social_agent = agent, out_group = True, population = population)
            else:
                #-- socialize in group
                socialize(social_agent = agent, out_group = False, population = population)
    
    check_groups(args, population, groups)
    
    for agent in population:
        agent.available = True
        agent.calc_social_fitness()

def run_generation(args, population, groups, selection):
    #-- run a generation of nrounds returns the new pro sociality ratings 
    group_sizes = np.zeros((args.ngroups, args.nrounds))
    
    for r in range(args.nrounds):
        # print(f'Round: {r}', sep=' ', end='\r')
        # print(f"\n----------------- {r} -----------------")
        
        run_round(args, population, groups)
        
        for i, group in enumerate(groups):
            group_sizes[i][r] = len(group)
    
        random.shuffle(population) #-- shuffle the population so that there is no ordering effect

    #-- after all social rounds are over, it is time for selection
    if selection: 
            #-- select fittest agents from the entire population
            fitness_agent_list = [(a, a.social_fitness) for a in population]
            sorted_fitness = sorted(fitness_agent_list, key = lambda x: x[1], reverse=True) #-- list sorted from high fitness to low fitness
            sorted_agents = [a for a, _ in sorted_fitness]
            best, rest, worst = select_fittest(sorted_agents, 0.1) #-- select the best and worst 5 % of the agents. 

            # print(f'agent fitness, pro-social: {[(a.groups[0], a.social_fitness, a.pro_social) for a in sorted_agents]}\n')

            new_phenotypes = reproduce(agent_list = best + best + rest, mut_prob = MUTATION_PROB)

    else:
        #-- all agents can reproduce
        # print(f'agent fitness, pro-social: {[(a.groups[0], a.social_fitness, a.pro_social) for a in population]}\n')
        new_phenotypes = reproduce(agent_list = population, mut_prob = .1)
    
    return group_sizes, new_phenotypes

def generate_population(args, new_phenotypes, new_sim):
    population = []
    
    for i in range(args.nagents):
        population.append(Agent(_name = i, _pro_social = args.prosocial))

    if new_sim:
        #-- first sim
        groups = np.split(np.array(population), args.ngroups)
        groups = np.array(groups).tolist()

        for i, group in enumerate(groups):
            for agent in group:
                agent.groups.append(i)

    else:
        #-- not first sim
        groups_phenotypes, ps_phenotypes = list(zip(*new_phenotypes))

        for i, agent in enumerate(population):
            #-- assign the phenotypes to the agents
            agent.pro_social = ps_phenotypes[i]
            agent.groups.append(groups_phenotypes[i])
        # print([(a.groups[0], a.pro_social) for a in population])

        sorted_population = sorted(population, key=lambda x: x.groups[0]) 
        # print([(a.groups[0], a.pro_social) for a in sorted_population])

        groups = np.split(np.array(sorted_population), args.ngroups)
        groups = np.array(groups).tolist()

    return population, groups

def run_all(args):
    
    all_generations_group_sizes = []
    gen_numbers = []

    for num_gen in range(args.generations):
        #-- Run a single generation
        print(f'\nGeneration {num_gen}')
        if num_gen == 0:
            population, groups = generate_population(args, [], new_sim = True)
        #     group_sizes, new_phenotypes = run_generation(args, population, groups, selection = False)
        #     print(new_phenotypes)
        
        else:
            population, groups = generate_population(args, new_phenotypes, new_sim = False)

        group_sizes, new_phenotypes = run_generation(args, population , groups, selection = SELECTION)
        # print(new_phenotypes)

        if num_gen % int(args.generations/3) == 0 or num_gen == args.generations - 1:
            # all_data.append(data_generation)
            gen_numbers.append(num_gen)
            all_generations_group_sizes.append(np.mean(group_sizes, axis=0))
        
    
    
    
    fig, axs = plt.subplots(1,2, figsize=(11, 4))

    #-- plot the course of the last generations' group sizes
    for i, line in enumerate(group_sizes):
        axs[0].plot(line, label=i)
    axs[0].set_ylabel("Group size")
    axs[0].set_xlabel("Rounds")
    axs[0].set_title(f"Group size last generation, agents: {args.nagents}")
    axs[0].grid()
    axs[0].legend()
   
    #-- plot the average generation groups size in a single line
    for i, line in enumerate(all_generations_group_sizes):
        axs[1].plot(line, label=f'gen{gen_numbers[i]}')

    axs[1].set_title(f"Average group size, agents: {args.nagents}")
    axs[1].set_xlabel("Rounds")
    axs[1].grid()
    axs[1].legend(bbox_to_anchor=(1.01,1), loc="upper left")
    
    #-- postprocess and save plots
    plt.subplots_adjust(left=0.05)
    plt.savefig(f'/Users/Tom/Desktop/Thesis/Sim_V1/output/12-05-{args.nagents}-{args.ngroups}-{args.nrounds}-{args.generations}-{SELECTION}')
    plt.show()
    


def main(args = None):
    #-- 

    parser = argparse.ArgumentParser(description="process some values")
    parser.add_argument('--nagents', '-na', type = int, dest = 'nagents', help = 'The starting population size', default = 10)
    parser.add_argument('--prosocial', '-ps', type = float, dest = 'prosocial', help = 'The starting pro sociality chance for each agent', default = 0.2)
    parser.add_argument('--ngroups', '-ng', type = int, dest = 'ngroups', help = 'The starting number of groups', default = 5)
    parser.add_argument('--generations', '-g', type = int, dest = 'generations', help ='The number of generations', default = 2)
    parser.add_argument('--nrounds', '-nr', type = int, dest = 'nrounds', help ='The number rounds for each generation', default = 5)
    args = parser.parse_args()
        
    run_all(args)

if __name__ == "__main__":
    main()

