# this is the main python code which you should run from terminal

import argparse

from Agent import Agent
from helpers import select_fittest, reproduce, split_to_groups, regroup_agents, groom, gossip, get_group_values

import numpy as np
import random

from matplotlib import pyplot as plt

from datetime import datetime

from os import getcwd
import os

path = getcwd()
print(path)
today = datetime.now()

date = today.strftime("%Y-%m-%dT%H-%M-%S") #-- %d-%m-%h-%m-%s

SELECTION = True
GROUP_REJECTION = .4
MUTATION_PROB = .05

def socialize(social_agent, population, out_group, args):
    # print()
    
    #-- determine whether the social agents wants to groom or gossip
    if random.uniform(0,1) < social_agent.gossip_prob:
        #-- agent wants to be groom
        gossip(social_agent, population, out_group, args.gossipagents)

    else:
        #-- agent wants to be gossip
        groom(social_agent, population, out_group, args.groomagents)

def run_round(args, population, groups):
    #-- runs a single round where agents can engage with each other.     
    for agent in population:
        if agent.available: #-- an agents can only socialize when he is not already socializing. 
            if random.uniform(0,1) < agent.tolerance or agent.social_preference == 2:
                #-- socialize out group
                socialize(social_agent = agent, population = population, out_group = True, args = args)
            else:
                #-- socialize in group
                socialize(social_agent = agent, population = population, out_group = False, args = args)
    
    regroup_agents(args, population, groups, GROUP_REJECTION) #-- checks for each agent their INTERNAL history and updates to which groups he belongs
    groups = split_to_groups(args, population) #-- checks the GENERAL groups in the population
    
    return groups

def generate_population(args, new_phenotypes, new_sim):
    population = []

    if new_sim:
        for i in range(args.nagents):
            population.append(Agent(_name = i, _tolerance = args.tolerance, _groups = (i % args.ngroups), _gossip_prob = args.gossipprob, _gossip_effect = args.gossipeffect, _groom_effect = args.groomeffect))

    else:
        groups_phenotypes, ps_phenotypes, go_phenotypes = list(zip(*new_phenotypes))
        for i in range(args.nagents):
            population.append(Agent(_name = i, _tolerance = ps_phenotypes[i], _groups = groups_phenotypes[i],  _gossip_prob = go_phenotypes[i], _gossip_effect = args.gossipeffect, _groom_effect = args.groomeffect))

        # print([a.groups for a in population])
    groups = split_to_groups(args, population)

    return population, groups    

def run_generation(args, population, groups, selection):
    #-- run a generation of nrounds returns the new toleranceity ratings 
    group_sizes = np.zeros((args.ngroups, args.nrounds))

    for r in range(args.nrounds):
        #-- run the social rounds
        round_groups = run_round(args, population, groups)

        for agent in population: 
            #-- each agent is available at the start of the next round. 
            agent.available = True

        for key in round_groups:
            group_sizes[key][r] = len(round_groups[key])

        random.shuffle(population) #-- shuffle the population after each round so that there is no ordering effect

        # print([(a.name, a.memory) for a in population])
        # print("--------------------------------------")

    for agent in population:
        agent.calc_fitness()

    #-- after all social rounds are over, it is time for selection
    if selection: 
            #-- select fittest agents from the entire population
            fitness_agent_list = [(a, a.fitness) for a in population]
            sorted_fitness = sorted(fitness_agent_list, key = lambda x: x[1], reverse=True) #-- list sorted from high fitness to low fitness
            sorted_agents = [a for a, _ in sorted_fitness]
            
            best, rest, worst = select_fittest(sorted_agents, 0.05) #-- select the best and worst 5% of the agents. 

            new_phenotypes = reproduce(agent_list = best + best + rest, mut_prob = MUTATION_PROB)

    else:
        #-- all agents can reproduce
        new_phenotypes = reproduce(agent_list = population, mut_prob = .1)

    #-- the return statement returns the group sizes for this particular generation, the new phenotypes, and the last group setup for this generation. 
    return group_sizes, new_phenotypes

def run_all(args):
    all_generations_group_sizes = []
    gen_numbers = []
    gossip_probabilities = []
    tolerance_probabilities = []

    per_generation_group_gp = []
    per_generation_group_tol = []

    for num_gen in range(args.generations):
        #-- Run a single generation
        # print(f'Generation {num_gen}')

        if num_gen == 0:
            population, groups = generate_population(args, [], new_sim = True)
        
        else:
            population, groups = generate_population(args, new_phenotypes, new_sim = False)

         #-- this part is done to check average probabilities per group
         #-- it is important that this is done before running the rounds, otherwise each agent can contribute towards the averages of multiple groups. 
        avg_gp_per_group, avg_tol_per_group = get_group_values(groups)

        per_generation_group_gp.append(avg_gp_per_group)
        per_generation_group_tol.append(avg_tol_per_group)

        #-- Run single generation
        group_sizes, new_phenotypes = run_generation(args, population , groups, selection = SELECTION)
        
        _, tol_prob, gossip_prob = list(zip(*new_phenotypes))
        gossip_probabilities.append(gossip_prob)
        tolerance_probabilities.append(tol_prob)
        
        #-- filter out those groups that are inactive, meaning that they have 0 members
        active_group_sizes = list(filter(lambda x: (x>0).any(), group_sizes)) 

        #-- only store the numbers occasionally
        # if num_gen % int(args.generations/5) == 0 or num_gen == args.generations - 1:
        gen_numbers.append(num_gen)
        all_generations_group_sizes.append(np.mean(active_group_sizes, axis=0))

    #-- reshape the vectors to a 2d matrix of colomns = generations and rows = groups
    group_by_generation_gp = list(map(list, zip(*per_generation_group_gp)))
    group_by_generation_tol = list(map(list, zip(*per_generation_group_tol)))
   
    avg_gossip_probs = np.mean(gossip_probabilities, axis = 1)
    avg_tolerance_probs = np.mean(tolerance_probabilities, axis = 1)

    return np.array(all_generations_group_sizes), np.array(gen_numbers), np.array(group_sizes), np.array(avg_gossip_probs), np.array(avg_tolerance_probs), np.array(group_by_generation_gp), np.array(group_by_generation_tol)

def main(args = None):
    #-- This part runs when the code starts, it parses the arguments given. 
    print("Running simulation..")

    parser = argparse.ArgumentParser(description="process some values")
    parser.add_argument('--nagents', '-na', type = int, dest = 'nagents', help = 'The starting population size', default = 10)
    parser.add_argument('--tolerance', '-tol', type = float, dest = 'tolerance', help = 'The starting tolerance chance for each agent', default = 0.5)
    parser.add_argument('--gossipprob', '-gp', type = float, dest = 'gossipprob', help = 'The starting gossip probability for each agent', default = 0.5)
    parser.add_argument('--ngroups', '-ng', type = int, dest = 'ngroups', help = 'The starting number of groups', default = 5)
    parser.add_argument('--generations', '-g', type = int, dest = 'generations', help ='The number of generations', default = 3)
    parser.add_argument('--nrounds', '-nr', type = int, dest = 'nrounds', help ='The number rounds for each generation', default = 5)
    parser.add_argument('--groomagents', '-grooma', type = int, dest = 'groomagents', help='The number of agents one can invite to groom', default = 1)
    parser.add_argument('--gossipagents', '-gossipa', type = int, dest = 'gossipagents', help='The number of agents one can invite to gossip', default = 3)
    parser.add_argument('--gossipeffect', '-gossipe', type = int, dest = 'gossipeffect', help='The effectiveness of a gossiping event on social fitness', default = 4)
    parser.add_argument('--groomeffect', '-groome', type = int, dest = 'groomeffect', help='The effectiveness of a grooming event on social fitness', default = 5)
    args = parser.parse_args()
        
    #-- run the simulation      
    #-- all_generation_group_sizes is an array that contains the average group size of the entire population per generation. Each row represents a generation and each column is a round. 
    all_generations_group_sizes, generation_labels, group_sizes, average_gossip_probabilities, average_tolerance_probabilities, group_gossip_prob, group_tolerance_prob = run_all(args)

    zipped_list = np.array(list(zip(generation_labels, all_generations_group_sizes)), dtype=object)
    zipped_phenotypes = np.array(list(zip(average_gossip_probabilities, average_tolerance_probabilities)))
    zipped_group_probabilities = np.array(list(zip(group_gossip_prob, group_tolerance_prob)))
    # run_all(args)

    # newpath = path + '/output/gridsearch/' + f'{args.nagents}-{args.ngroups}-{args.nrounds}-{args.generations}-{str(args.tolerance).replace(".", "")}-{str(args.gossipprob).replace(".", "")}-{SELECTION}-{args.groomagents}-{args.gossipagents}'
    newpath = path + '/output/gridsearch/' + f'{args.gossipeffect}-{args.groomeffect}'
    if not os.path.exists(newpath):
        print(f"create path: {newpath}")
        os.makedirs(newpath)

    np.save(f'{newpath}/{date}-avg-groupsize-over-pop.npy', zipped_list) #--saves the average group size of the ENTIRE population for each round in a generation
    np.save(f'{newpath}/{date}-last_generation_groups.npy', group_sizes) #--saves the group sizes of the last generation. 
    np.save(f'{newpath}/{date}-avg_phenotypes_over_pop.npy', zipped_phenotypes) #--saves the average phenotypes over the population . 
    np.save(f'{newpath}/{date}-avg_phenotypes_per_group.npy', zipped_group_probabilities) #--saves the average phenotypes per group . 

if __name__ == "__main__":
    main()

