# CSSSA 2022

This repository implements several versions of a voter model on a wide variety of
graphs and conditions. Our work departs from findings reported in

> Papanikolaou, N., Vaccario, G., Hormann, E., Lambiotte, R. and Schweitzer, F., 2022. Consensus from group interactions: An adaptive voter model on hypergraphs. arXiv preprint [arXiv:2201.06421](https://arxiv.org/abs/2201.06421).

## Model parameters

Each execution of the model computes an ensemble for a given configuration with a parameter set and stores it in a SQLite database. Each simulation is given a UUID for indexing purposes, computed from its parameter set. Parameters are as follows:

* **type:** scheduled vs instantaneous
* **interactions:** dyadic vs higher order
* **graph type:** regular 2D lattice, triangular 2D lattice, hexagonal 2D lattice, $K_n$, Watts-Strogatz, power law, hypercube, Erdos-Renyi, Barabasi-Albert
* **number of agents (log_2):** an even value $k$ such that the number of agents is $2^k$, ranging from $k=6$ to $k=12$
* **gamma**: collective magnetization threshold from 0 to 1
* **ensemble size:** defaults to 50
