# Master-Thesis

Make sure you use python 3.7 or higher. 
Other requirements:
- Numpy installed
- Matplotlib installed

To activate the virtual environment by running ```source env/bin/activate``` at the located folder.

To run the Slingerland code run ```python Slingerland_Sim.py 200``` and a simulation with 200 generations will start. 

To run the Sim_V1 or Sim_V2 code run ```python __main__.py``` in your terminal.
Provide arbitrary starting parameters in the following way:

- ```--nagents 50```
- ```--nrounds 100```
- ```--prosocial 0.2```
- ```--ngroups 5``` (Make sure that it can equally devide the number of agents)
- ```--ngenerations 1```
- ```--groomagents 2```
- ```--gossipagents 3```

Or run ```python __main__.py --help``` to see the options available.

The difference between V1 and V2 is that observations are not implemented in V1. Hence it's mechanism is not yet equal to that of Slingerland. 
