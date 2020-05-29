# this is the main python code which you should run from terminal

##TODO
# - Maximaal aantal groepen voor 1 agent 

import argparse

from Agent import Agent
from helpers import select_fittest, reproduce, split_to_groups, regroup_agents, groom, gossip

import numpy as np
import random

from matplotlib import pyplot as plt

from datetime import date

today = date.today()

# dd/mm/YY
date = today.strftime("%d-%m")

SELECTION = False
GROUP_REJECTION = .2
MUTATION_PROB = .1
GOSSIP_PROB = .2

def socialize(social_agent, population, out_group):
    # print()
    # print(f"{social_agent.name} wants to be outgroup social and belongs to group: {social_agent.groups[0]}")
    
    
    #-- determine whether the social agents wants to groom or gossip
    if random.uniform(0,1) < social_agent.gossip_prob:
        #-- agent wants to be groom
        gossip(social_agent, population, out_group)

    else:
        #-- agent wants to be gossip
        groom(social_agent, population, out_group)

def run_round(args, population, groups):
    #-- runs a single round where agents can engage with each other.     
    for agent in population:
        if agent.available: #-- an agents can only socialize when he is not already socializing. 
            
            # print([(a.name, a.available) for a in population])
            if random.uniform(0,1) < agent.pro_social or agent.social_preference == 2:
                #-- socialize out group

                socialize(social_agent = agent, population = population, out_group = True)
            else:
                #-- socialize in group

                socialize(social_agent = agent, population = population, out_group = False)
    
        # print([(a.name, a.history, a.memory) for a in population])
        # print("--------")
        # print()
    regroup_agents(args, population, groups, GROUP_REJECTION) #-- checks for each agent their INTERNAL history and updates to which groups he belongs
    groups = split_to_groups(args, population) #-- checks the GENERAL groups in the population
    # print()
    

    # check_groups(args, population, groups)
    
    for agent in population:
        agent.available = True
        agent.calc_social_fitness()

    # for key in groups:
    #     print(f'group {key}: {[a.name for a in groups[key]]}')
    
    return groups

def generate_population(args, new_phenotypes, new_sim):
    population = []

    if new_sim:
        for i in range(args.nagents):
            population.append(Agent(_name = i, _pro_social = args.prosocial, _groups = (i % args.ngroups), _gossip_prob = GOSSIP_PROB))
        
        # print([a.groups for a in population])
        groups = split_to_groups(args, population)

    else:
        groups_phenotypes, ps_phenotypes, go_phenotypes = list(zip(*new_phenotypes))
        for i in range(args.nagents):
            population.append(Agent(_name = i, _pro_social = ps_phenotypes[i], _groups = groups_phenotypes[i],  _gossip_prob = go_phenotypes[i]))

        # print([a.groups for a in population])
        groups = split_to_groups(args, population)

    return population, groups    

def run_generation(args, population, groups, selection):
    #-- run a generation of nrounds returns the new pro sociality ratings 
    group_sizes = np.zeros((args.ngroups, args.nrounds))

    for r in range(args.nrounds):
        #-- run the social rounds
        # print(f"round: {r}")
        gen_groups = run_round(args, population, groups)
        
        for key in gen_groups:
            group_sizes[key][r] = len(gen_groups[key])
    
        # print(f'{[(a.name, a.gossip_prob) for a in population]}')

        random.shuffle(population) #-- shuffle the population so that there is no ordering effect
        
        

    #-- after all social rounds are over, it is time for selection
    if selection: 
            #-- select fittest agents from the entire population
            fitness_agent_list = [(a, a.social_fitness) for a in population]
            sorted_fitness = sorted(fitness_agent_list, key = lambda x: x[1], reverse=True) #-- list sorted from high fitness to low fitness
            # print([(a.name, a.pro_social, a.gossip_prob) for a, _ in sorted_fitness])
            sorted_agents = [a for a, _ in sorted_fitness]
            best, rest, worst = select_fittest(sorted_agents, 0.1) #-- select the best and worst 5 % of the agents. 

            # print(f'agent fitness, pro-social: {[(a.groups[0], a.social_fitness, a.pro_social) for a in sorted_agents]}\n')

            new_phenotypes = reproduce(agent_list = best + best + rest, mut_prob = MUTATION_PROB)
            # print("-----")
            # print(new_phenotypes)
    else:
        #-- all agents can reproduce
        # print(f'agent fitness, pro-social: {[(a.groups[0], a.social_fitness, a.pro_social) for a in population]}\n')
        new_phenotypes = reproduce(agent_list = population, mut_prob = .1)
    
    # print(f'Ending group sizes: {[len(groups[key]) for key in groups]}')
    # print(f'Phenotypes: {new_phenotypes}')

    return group_sizes, new_phenotypes

def run_all(args):
    
    all_generations_group_sizes = []
    gen_numbers = []
    gossip_probabilities = []


    for num_gen in range(args.generations):
        #-- Run a single generation
        print(f"Generation {num_gen}")

        

        if num_gen == 0:
            population, groups = generate_population(args, [], new_sim = True)
        
        else:
            population, groups = generate_population(args, new_phenotypes, new_sim = False)

        # print(f'{[(a.name, a.groups[0], a.pro_social) for a in population]}')

        group_sizes, new_phenotypes = run_generation(args, population , groups, selection = SELECTION)
        
        _, _, gossip_prob = list(zip(*new_phenotypes))
        gossip_probabilities.append(gossip_prob)

        #-- filter out those that are inactive, meaning that they have 0 members
        active_group_sizes = list(filter(lambda x: (x>0).any(), group_sizes)) 

        #-- only store the numbers occasionally
        if num_gen % int(args.generations/3) == 0 or num_gen == args.generations - 1:
            gen_numbers.append(num_gen)
            all_generations_group_sizes.append(np.mean(active_group_sizes, axis=0))

        # print(f'{[(a.name, a.gossip_prob) for a in population]}')

    # print(gossip_probabilities)    
    avg_gossip_probs = np.mean(gossip_probabilities, axis = 1)

    # plt.plot(avg_gossip_probs)
    # plt.show()

    #-- plotting the results
    fig, axs = plt.subplots(1,3, figsize=(15, 4))

    #-- plot the course of the last generations' group sizes
    for i, line in enumerate(group_sizes):
        axs[0].plot(line, label=i)
    axs[0].set_ylabel("Group size")
    axs[0].set_xlabel("Rounds")
    axs[0].set_title(f"Group size last generation")
    axs[0].grid()
    axs[0].legend(bbox_to_anchor=(1.01,1), loc="upper left")
   
    #-- plot the average generation groups size in a single line
    for i, line in enumerate(all_generations_group_sizes):
        axs[1].plot(line, label=f'gen{gen_numbers[i]}')

    axs[1].set_title(f"Average group size, agents: {args.nagents}")
    axs[1].set_xlabel("Rounds")
    axs[1].set_xlim(0, args.nrounds)
    axs[1].grid()
    axs[1].legend(bbox_to_anchor=(1.01,1), loc="upper left")
    
    axs[1].set_title(f"Average gossip probability")
    axs[2].plot(avg_gossip_probs)
    axs[2].set_xlabel("Generation")
    axs[2].set_xlim(0, args.generations)
    axs[2].set_ylabel("Gossip Probability")

    #-- postprocess and save plots
    fig.suptitle(f'Agents: {args.nagents}, Groups: {args.ngroups}, Selection: {SELECTION}, Mutation prob: {MUTATION_PROB}')
    plt.subplots_adjust(left=0.05, right=0.95, wspace=0.50)
    plt.savefig(f'/Users/Tom/Desktop/Thesis/Sim_V2/output/{date}-{args.nagents}-{args.ngroups}-{args.nrounds}-{args.generations}-{SELECTION}')
    plt.show()
    


def main(args = None):
    #-- This part runs when the code starts, it parses the arguments given. 

    parser = argparse.ArgumentParser(description="process some values")
    parser.add_argument('--nagents', '-na', type = int, dest = 'nagents', help = 'The starting population size', default = 10)
    parser.add_argument('--prosocial', '-ps', type = float, dest = 'prosocial', help = 'The starting pro sociality chance for each agent', default = 0.2)
    parser.add_argument('--ngroups', '-ng', type = int, dest = 'ngroups', help = 'The starting number of groups', default = 5)
    parser.add_argument('--generations', '-g', type = int, dest = 'generations', help ='The number of generations', default = 3)
    parser.add_argument('--nrounds', '-nr', type = int, dest = 'nrounds', help ='The number rounds for each generation', default = 5)
    args = parser.parse_args()
        
    run_all(args)

if __name__ == "__main__":
    main()

