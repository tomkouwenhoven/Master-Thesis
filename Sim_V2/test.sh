#!/bin/bash

for i in {1..2}
do
    for j in {1..2}
    do 
        echo "Running with grooming effectiveness of : $i and gossip effectiveness of: $j .."
        python __main__.py --nagents 100 --ngroups 20 --nrounds 75 --generations 125 --groomagents 3 --gossipagents 3 --gossipeffect $i --groomeffect $j
        # python __main__.py --nagents 100 --ngroups 20 --nrounds 75 --generations 10 --groomagents 3 --gossipagents 3 --gossipeffect $i --groomeffect $j
    done
done