# Copyright (c) 2022 SPEC collaborative. All rights reserved.
#
# This program and the accompanying materials are made available under the
# terms of the Mozilla Public License v2.0 which accompanies this distribution,
# and is available at https://www.mozilla.org/en-US/MPL/2.0/
from copy import deepcopy
import random
import math

from networkx import Graph
from csssa2022.selections import InteractionType, SimulationType
from csssa2022.abstractvotermodel import AbstractVoterModel


class HigherOrderMatrixVoterModel(AbstractVoterModel):
    '''
    This voter model only has dyadic interactions, uses state vector to represent agents, and
    updates all state agents simultaneously at the end of one simulation step.
    '''
    def __init__(self, uuid_exp, ensemble_id, interactants, initial_state, network: Graph, n, max_steps, db, **kwargs):
        super().__init__(uuid_exp=uuid_exp,
                         ensemble_id=ensemble_id,
                         simtype=SimulationType.MATRIX,
                         interactions=InteractionType.HIGHER_ORDER,
                         interactants=interactants,
                         initial_state=initial_state,
                         network=network,
                         n=n,
                         max_steps=max_steps,
                         db=db,
                         **kwargs)
        # We represent the agent store as a dictionary
        self.agent_states = {}
        self.agent_fs = {}
        
        # Add agents depending on their initial opinion, start with
        # a trivial value of f
        for i in self.initial_yes:
            self.agent_states[i] = 1
            self.agent_fs[i] = 0
            
        for i in self.initial_no:
            self.agent_states[i] = 0
            self.agent_fs[i] = 0
        
    def step(self):
        if self.stepno == self.max_steps:
            self.running = False
        else:
            # Compute a new map for all agents and replace the old map
            new_states = {}
            new_fs = {}
            
            # Obtain a random sample set corresponding to centroids
            centroids = random.sample(self.agent_list, math.ceil(self.n/self.interactants))
            
            # For all centroids, compute the neighbors, determine f and change the value of the entire
            # partition
            
            for c in centroids:
                # The partition includes itself
                partition = self.get_neighbors(c) + [c]
                
                # Compute the value of the partition
                f_part, interactants = self.compute_f(partition, self.interactants)
                
                # Set f and the state collectively
                new_fs.update(dict.fromkeys(interactants, f_part))
                
                if f_part > self.f_threshold:
                    new_states.update(dict.fromkeys(interactants, 1))
                else:
                    new_states.update(dict.fromkeys(interactants, 0))

            # Update new states and fs manually
            for a, op in new_states.items():
                self.agent_states[a] = op
                
            for a, op in new_fs.items():
                self.agent_fs[a] = op
            
    def compute_f(self, partition: list(), interactants: int):
        '''
        The value of f is computed in bloc for a subset of the agents
        '''
        total = 0.0
    
        k = len(partition)
        
        # Take a subset of interactants when possible
        if k > interactants:
            sample = random.sample(partition, interactants)
        else:
            sample = partition
        
        for j in sample:
            total += self.agent_states[j]
            
        total /= k
        return total, sample
    
    def get_opinion(self, i):
        return self.agent_states[i]
    
    def get_f(self, i):
        return self.agent_fs[i]