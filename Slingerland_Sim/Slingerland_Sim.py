from Agent import Agent
from Actions import groom, gossip, observe, reproduce, select_fittest

import numpy as np
import random
import matplotlib.pyplot as plt

import sys
import argparse

n_rounds = 30
n_generations = int(sys.argv[1])
mutation_prob = .01

# go_probabilities = np.full(num_agents, .1, dtype=float)
# print(go_probabilities)

def run_generation(_go_probs, num_agents): 
    #-- run for number of rounds, with entire generation of num_agents. After the number of rounds each agent is evaluated and some are allowed to mutate. 
   
    group = []
    for i in range(num_agents):
        group.append(Agent(_name = i, _gossip_prob = _go_probs[i]))

    total_i_fitness = np.zeros((n_rounds, num_agents))
    total_s_fitness = np.zeros((n_rounds, num_agents))
    total_fitness = np.zeros((n_rounds, num_agents))

    N_EVENTS = 0

    for r in range(n_rounds):
        # print(f'---------------------- Round number: {r} ----------------------')
        for agent in group:
            agent.groom = False
            agent.gossip = False

        #-- All agents of this generation socialize for n_rounds
        sampled_agents = random.sample(group, random.randint(1, num_agents))
        grooming_agents = []
        gossiping_agents = []

        for a in sampled_agents:
        #--determine whether an agents goes gossiping or grooming
            if random.uniform(0,1) > a.gossip_prob: 
                groom(a, group, (f'event: {N_EVENTS}')) #-- GROUP?
                grooming_agents.append(a)
            else:
                gossip(a, group, (f'event: {N_EVENTS}')) #-- GROUP?
                gossiping_agents.append(a)
            N_EVENTS += 1
        
        # g_names = [agent.name for agent in gossiping_agents]
        # names = [agent.name for agent in grooming_agents]
        # print(f'Want to groom:      {names} \nWant to gossip:     {g_names}'))

        # -- Other
        # for i, agent in enumerate(group):
        #     total_s_fitness[r][i] = agent.calc_social_fitness()
        #     total_i_fitness[r][i] = agent.calc_info_fitness()
        #     total_fitness[r][i] = agent.calc_fitness()s
            # print(f'agent: :{agent.name} memory: {agent.memory}')
            # agent.calc_fitness()
            # print(f'agent: {agent.name}, fitness: {agent.fitness}, memory: {agent.memory}, groom events: {agent.groom_members_list}, Gossip events: {agent.gossip_members_list}')
    # fitness_agent_list = list(zip(group, total_fitness[-1])) #-- list (agent, fitness)


#-- Evaluation 
    #-- The fitness of each agents is calculated, sorted and the best & worst 5% are selected.
    fitness_agent_list = [(a, a.calc_fitness()) for a in group]
    sorted_fitness = sorted(fitness_agent_list, key = lambda x: x[1], reverse=True) #-- list sorted from high fitness to low fitness
    best, rest, worst = select_fittest(sorted_fitness, 0.1) #-- select the best and worst 5 % of the agents. 

    #-- This is were mutation happens, each agent reproduces a single new gossip probability. 
    r_gp_mutated = [reproduce(a, mut_prob = mutation_prob) for a, _ in rest] #-- middle group mutated gossip probabilities
    b_gp_mutated1 = [reproduce(a, mut_prob = mutation_prob) for a, _ in best] #-- best group mutated gossip probabilities for first baby 
    b_gp_mutated2 = [reproduce(a, mut_prob = mutation_prob) for a, _ in best] #-- best group mutated gossip probabilities for second baby
   
    go_p_mutated = b_gp_mutated1 + b_gp_mutated2 + r_gp_mutated #-- middle group only gets one child, high group gets two childs. 

    return go_p_mutated


# gen_go_probs = np.empty((n_generations, num_agents))
# avg_gen_go_prob = []

def run_group(size):
    go_probabilities = np.full(size, .1, dtype=float)

    gen_go_probs = np.empty((n_generations, size))
    avg_gen_go_prob = []

    for i in range(n_generations):
        # print(f'Generation: {i}', sep=' ', end='\r')
        if i == 0:
            # g_fitness_agent, mutated_go, go_probs = run_generation(go_probabilities)
            mutated_go = run_generation(go_probabilities, size)
            
        else:
            # g_fitness_agent, mutated_go, go_probs = run_generation(mutated_go)
            mutated_go = run_generation(mutated_go, size)
            # print(go_probs)
        # print(f'after: {mutated_go}')
        gen_go_probs[i] = mutated_go #-- array containing the new gossip probabilities of each agent in a single generation

        
        avg_gen_go_prob.append(np.mean(mutated_go))
    return avg_gen_go_prob[-1]

group_last_prob = []
for i in range(2,200):
    print(f'Group: {i}', sep=' ', end='\r')
    group_last_prob.append(run_group(i))

# g_avg_go_prob
# print(np.mean(gen_go_prob, axis = 1))
# g_avg_go_prop = np.mean(gen_go_prob, axis = 1)

# #-- Plotting
fig = plt.figure()
plt.plot(group_last_prob, 'bx')
plt.ylabel("Mean Gossip Probability")
plt.xlabel("Group size")
plt.title(f"Average gossip probability per group, mutation prob:{mutation_prob}")
plt.grid()
plt.savefig(f'/Users/Tom/Desktop/Thesis/Slingerland_Sim/output/30-04_avg_gp_global-{mutation_prob}-0505.png')
plt.show()



# def main(args = None):
#     parser = argparse()

# if __name__ == "__main__":
#     main()
