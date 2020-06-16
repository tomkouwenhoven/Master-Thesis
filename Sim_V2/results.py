
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from os import listdir
from os.path import isfile, join
from os import getcwd

sns.set(style="darkgrid")

path = getcwd()
print(path)

files = [f for f in listdir(f'{path}/output/data') if isfile(join(f'{path}/output/data', f))]

files.remove('.DS_Store') #-- stupid Mac file

def calc_mean(files):
    all_arrays = []
    for file in files:
        # print(file)
        # print(np.load(f'{path}/output/data/{file}'))
        all_arrays.append(np.load(f'{path}/output/data/{file}'))
    
    arrays = np.array(all_arrays)

    return np.mean(arrays, axis=0)

average_group_sizes_over_all = calc_mean(files)
print(average_group_sizes_over_all.shape)

df = pd.DataFrame(data=average_group_sizes_over_all, index=list(range(0, 2)), columns=list(range(0,5)))
print(df)
# df = pd.DataFrame(data=numpy_data, index=["row1", "row2"], columns=["column1", "column2"])

# sns.relplot(x="timepoint", y="signal", kind="line", data=fmri);


    # #-- plotting the results
    # fig, axs = plt.subplots(2,3, figsize=(15, 7.5))

    # #-- plot the average generation groups size in a single line
    # for i, line in enumerate(all_generations_group_sizes):
    #     axs[0][0].plot(line, label=f'gen{gen_numbers[i]}')

    # axs[0][0].set_title(f"Average group size")
    # axs[0][0].set_xlabel("Rounds")
    # # axs[0][0].set_xlim(0, args.nrounds)
    # axs[0][0].grid()
    # axs[0][0].legend(bbox_to_anchor=(1.01,1), loc="upper left")
    
    # #-- plot the average gossip and pro social probability. 
    # axs[1][0].set_title(f"Average gossip & pro-social probability")
    # axs[1][0].plot(avg_gossip_probs, label = "gp")
    # axs[1][0].plot(avg_pro_social_probs, label = "ps")
    # axs[1][0].set_xlabel("Generation")
    # # axs[1][0].set_xlim(0, args.generations)
    # axs[1][0].set_ylabel("Probability")
    # axs[1][0].grid()
    # axs[1][0].legend(bbox_to_anchor=(1.01,1), loc="upper left")

    # #-- plot the course of the last generations' group sizes
    # for i, line in enumerate(group_sizes):
    #     axs[0][1].plot(line, label=i)
    # # axs[0][1].set_ylabel("Group size")
    # axs[0][1].set_xlabel("Rounds")
    # axs[0][1].set_title(f"Group size last generation")
    # axs[0][1].grid()
    # axs[0][1].legend(bbox_to_anchor=(1.01,1), loc="upper left")

    # #-- plot per group average gossip probability
    # for i, line in enumerate(group_by_generation_gp):
    #     axs[1][1].plot(line, label=i)
    # # axs[1][1].set_ylabel("Prabability")
    # axs[1][1].set_xlabel("Generation")
    # axs[1][1].set_title(f"Gossip probability per group")
    # axs[1][1].grid()
    # axs[1][1].legend(bbox_to_anchor=(1.01,1), loc="upper left")

    # #-- plot per group average pro sociality
    # for i, line in enumerate(group_by_generation_gs):
    #     axs[1][2].plot(line, label=i)
    # # axs[1][2].set_ylabel("Prabability")
    # axs[1][2].set_xlabel("Generation")
    # axs[1][2].set_title(f"Pro sociality per group")
    # axs[1][2].grid()
    # axs[1][2].legend(bbox_to_anchor=(1.01,1), loc="upper left")

    # #-- postprocess and save plots
    # fig.suptitle(f'Agents: {args.nagents}, Groups: {args.ngroups}, Selection: {SELECTION}, Mutation prob: {MUTATION_PROB}')
    # plt.subplots_adjust(bottom=0.075, left=0.075, right=0.9, wspace=0.50, hspace=0.30, top=0.9)
    # plt.savefig(f'/Users/Tom/Desktop/Thesis/Sim_V2/output/{date}-{args.nagents}-{args.ngroups}-{args.nrounds}-{args.generations}-{str(args.prosocial).replace(".", "")}-{str(args.gossipprob).replace(".", "")}-{SELECTION}')
    # plt.show()