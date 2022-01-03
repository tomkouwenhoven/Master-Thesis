# for i in {1..40}
# do 
#     echo "Running with simuluation: $i from gossipeffect 4 and groomingeffect 5 and grooming with 1 other and gossip with up to 3 others"
#     python __main__.py --nagents 100 --ngroups 20 --nrounds 75 --generations 125 --groomagents 1 --gossipagents 3 --gossipeffect 4 --groomeffect 5

# done 

for i in {1..40}
do 
    echo "Running with simuluation: $i from gossipeffect 5 and groomingeffect 5 and grooming with 1 other and gossip with up to 3 others"
    python __main__.py --nagents 100 --ngroups 20 --nrounds 75 --generations 125 --groomagents 1 --gossipagents 3 --gossipeffect 5 --groomeffect 5

done 

for i in {1..40}
do 
    echo "Running with simuluation: $i from gossipeffect 5 and groomingeffect 5 and grooming with 2 other and gossip with up to 2 others"
    python __main__.py --nagents 100 --ngroups 20 --nrounds 75 --generations 125 --groomagents 2 --gossipagents 2 --gossipeffect 5 --groomeffect 5

done 