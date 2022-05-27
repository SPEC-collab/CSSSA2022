# CSSSA 2022

This repository implements several versions of a voter model on a wide variety of
graphs and conditions. Our work departs from findings reported in

> Papanikolaou, N., Vaccario, G., Hormann, E., Lambiotte, R. and Schweitzer, F., 2022. Consensus from group interactions: An adaptive voter model on hypergraphs. arXiv preprint [arXiv:2201.06421](https://arxiv.org/abs/2201.06421).

## Model parameters

Each execution of the model computes an ensemble for a given configuration with a parameter set and stores it in a SQLite database. Each simulation is given a UUID for indexing purposes, computed from its parameter set. Parameters are as follows:

* **simulation type:** matrix vs ABM
* **interactions:** dyadic vs higher order
* **number of interactants:** quantity of agents involved in a single interaction (pairwise = 2, higher order > 2)
* **initial state:** proportion of agents selected at random with opinion = 1
* **graph type:** regular 2D lattice, triangular 2D lattice, hexagonal 2D lattice, $K_n$, Watts-Strogatz, power law, hypercube, Erdos-Renyi, Barabasi-Albert
* **number of agents (log_2):** an even value $k$ such that the number of agents is $2^k$, ranging from $k=6$ to $k=12$
* **gamma**: collective magnetization threshold from 0 to 1
* **ensemble size:** defaults to 50
* **total time**: defaults to 5000


## Stored values

Each simulation appends to an SQLite database new rows per ensemble, per timestep, each $i$-th agent's current preference as well as its value for $f_i(t)$, from which average magnetization can be computed through queries.

Database fields:
* **id:** a UUID determined uniquely by the combination of relevant parameters.
* **ensemble_id:** number indicating the id of the current run per ensemble
* **step_id:** identifier of the current agent
* **agent_id:** identifier of the existing agent
* **opinion:** 0/1 value indicating voting preference
* **f_val:** current opinion fraction leading to vote switching

## Scientific aims

* Connect our interaction dynamics to real-world social processes

### Current choices

* **Network:** 2D grid (periodic)
* **Time steps:** 5000
* **Interactants:** 3
* **Number of agents:** 256
* **Ensemble size:** 50

### Contrasts

1. Determine whether magnetization differences occur depending on dyadic/higher-order interactions for each network
2. Determine whether ABM vs matrix implementations induce magnetization differences in the same graph

### Observables

* Average magnetization
* (Meta)stability
* Time to convergence

## Future work

* Determine the effect of system scaling vs Erdos-Renyi
* Analysis of cluster formation during voting (connected components)
* Determine whether different choices of graphs induce magnetization differences in the same model/across models
* Introduce scheduler differences (random, priority)
