#!/bin/bash

# for i in {1..2}
# do
#     for j in {1..2}
#     do 
#         echo "Running with grooming effectiveness of : $i and gossip effectiveness of: $j .."
#         python __main__.py --nagents 100 --ngroups 20 --nrounds 75 --generations 125 --groomagents 3 --gossipagents 3 --gossipeffect $i --groomeffect $j
#         # python __main__.py --nagents 100 --ngroups 20 --nrounds 75 --generations 10 --groomagents 3 --gossipagents 3 --gossipeffect $i --groomeffect $j
#     done
# done

for i in {1..10}
do 
    echo "Running with simuluation: $i from gossip 4 and grooming 5"
    python __main__.py --nagents 100 --ngroups 20 --nrounds 75 --generations 125 --groomagents 3 --gossipagents 3 --gossipeffect 4 --groomeffect 5
done 

for i in {1..10}
do 
    echo "Running with simuluation: $i from gossip 3 and grooming 5"
    python __main__.py --nagents 100 --ngroups 20 --nrounds 75 --generations 125 --groomagents 3 --gossipagents 3 --gossipeffect 3 --groomeffect 5
done 

for i in {1..10}
do 
    echo "Running with simuluation: $i from gossip 2 and grooming 5"
    python __main__.py --nagents 100 --ngroups 20 --nrounds 75 --generations 125 --groomagents 3 --gossipagents 3 --gossipeffect 2 --groomeffect 5
done 

for i in {1..10}
do 
    echo "Running with simuluation: $i from gossip 1 and grooming 5"
    python __main__.py --nagents 100 --ngroups 20 --nrounds 75 --generations 125 --groomagents 3 --gossipagents 3 --gossipeffect 1 --groomeffect 5
done 

for i in {1..10}
do 
    echo "Running with simuluation: $i from gossip 5 and grooming 5"
    python __main__.py --nagents 100 --ngroups 20 --nrounds 75 --generations 125 --groomagents 3 --gossipagents 3 --gossipeffect 5 --groomeffect 5
done 