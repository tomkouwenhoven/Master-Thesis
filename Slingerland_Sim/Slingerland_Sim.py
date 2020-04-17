from Agent import Agent
from Actions import groom, gossip, observe, reproduce, select_fittest

import numpy as np
import random
import matplotlib.pyplot as plt

import sys

print (f'The script ran with {sys.argv[1]} agents and for {sys.argv[2]} generations.')

num_agents = int(sys.argv[1])
n_rounds = 30
n_generations = int(sys.argv[2])
mutation_prob = .01


go_probabilities = np.full(num_agents, .1, dtype=float)
# print(go_probabilities)

def run_generation(_go_probs): #-- run for number of rounds, with entire generation
    # print(go_probs)
    
    group = []
    for i in range(num_agents):
        group.append(Agent(_name = i, _gossip_prob = _go_probs[i]))

    total_i_fitness = np.zeros((n_rounds, num_agents))
    total_s_fitness = np.zeros((n_rounds, num_agents))
    total_fitness = np.zeros((n_rounds, num_agents))

    for r in range(n_rounds):
        # print(f'---------------------- Round number: {r} ----------------------')
        for agent in group:
            agent.groom = False
            agent.gossip = False

        #-- All agents of this generation socialize for n_rounds
        sampled_agents = random.sample(group, random.randint(1, num_agents))
        # grooming_agents = [agent for agent in sampled_agents if random.uniform(0,1) > agent.gossip_prob]
        # gossiping_agents = [agent for agent in sampled_agents if agent not in grooming_agents]

        grooming_agents = []
        gossiping_agents = []

        for a in sampled_agents:
        #--determine whether an agents goes gossiping or grooming
            if random.uniform(0,1) > a.gossip_prob: 
                groom(a, group)
                grooming_agents.append(a)
            else:
                gossip(a, group)
                gossiping_agents.append(a)
        
        # g_names = [agent.name for agent in gossiping_agents]
        # names = [agent.name for agent in grooming_agents]
        # print(f'Want to groom:      {names} \nWant to gossip:     {g_names}')

        # gossip_all(gossiping_agents, group)
        # groom_all(grooming_agents, group)
        

        # -- Other
        # for i, agent in enumerate(group):
        #     total_s_fitness[r][i] = agent.calc_social_fitness()
        #     total_i_fitness[r][i] = agent.calc_info_fitness()
        #     total_fitness[r][i] = agent.calc_fitness()
            # print(f'agent: :{agent.name} memory: {agent.memory}')
            # print(f'agent: {agent.name}, fitness: {agent.fitness}, groom events: {agent.groom_events}, Gossip events: {agent.gossip_events}')
    # fitness_agent_list = list(zip(group, total_fitness[-1])) #-- list (agent, fitness)


#-- Evaluation 
    fitness_agent_list = [(a, a.calc_fitness()) for a in group]
    sorted_fitness = sorted(fitness_agent_list, key = lambda x: x[1], reverse=True) #-- list sorted from high fitness to low fitness
    best, rest, worst = select_fittest(sorted_fitness, 0.1) #-- select the best and worst 5 % of the agents. 

    r_gp_mutated = [reproduce(a, mut_prob = mutation_prob, mut_rate = 5) for a, _ in rest] #-- middle group mutated gossip probabilities
    b_gp_mutated1 = [reproduce(a, mut_prob = mutation_prob, mut_rate = 5) for a, _ in best] #-- high group mutated gossip probabilities for first baby 
    b_gp_mutated2 = [reproduce(a, mut_prob = mutation_prob, mut_rate = 5) for a, _ in best] #-- high group mutated gossip probabilities for second baby
    
    go_probs = [a.gossip_prob for a in group]
    # print(f'Before mutation: {go_probs}')

    go_p_mutated = b_gp_mutated1 + b_gp_mutated2 + r_gp_mutated #-- middle group only gets one child, high group gets two childs. 

    # return fitness_agent_list, go_p_mutated, go_probs
    return go_p_mutated


gen_go_probs = np.empty((n_generations, num_agents))
avg_gen_go_prob = []

# mutated_go = [0,0,0,0,0,0,0,0,0,0]
for i in range(n_generations):
    print(f'Generation: {i}')
    # print(f'Before: {mutated_go}')
    if i == 0:
        # g_fitness_agent, mutated_go, go_probs = run_generation(go_probabilities)
        mutated_go = run_generation(go_probabilities)
        # print(mutated_go)
    else:
        # g_fitness_agent, mutated_go, go_probs = run_generation(mutated_go)
        mutated_go = run_generation(mutated_go)
        # print(go_probs)
    # print(f'after: {mutated_go}')
    gen_go_probs[i] = mutated_go #-- array containing the new gossip probabilities of each agent in a single generation

    
    avg_gen_go_prob.append(np.mean(mutated_go))


# g_avg_go_prob
# print(np.mean(gen_go_prob, axis = 1))
# g_avg_go_prop = np.mean(gen_go_prob, axis = 1)

# # test = simulate_gen()

# #-- Plotting
fig = plt.figure()
ax = plt.subplot(111)
ax.plot(avg_gen_go_prob)
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.90, box.height])
ax.legend(labels = list(range(n_generations)), loc='center left', bbox_to_anchor=(1, 0.5))

# plt.title("Fitness per agent")
plt.ylabel("Mean Gossip Probability")
plt.xlabel("Number of generations")
plt.title(f"Average gossip probability, n_agents:{num_agents}, mutation prob:{mutation_prob}")
plt.grid()


# plt.savefig(f'/Users/Tom/Desktop/Thesis/Slingerland_Sim/output/17-0_avg_gp_{num_agents}-{n_generations}-{mutation_prob}.png')
plt.show()