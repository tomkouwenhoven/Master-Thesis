



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