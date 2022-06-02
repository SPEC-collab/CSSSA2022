# Copyright (c) 2022 SPEC collaborative. All rights reserved.
#
# This program and the accompanying materials are made available under the
# terms of the Mozilla Public License v2.0 which accompanies this distribution,
# and is available at https://www.mozilla.org/en-US/MPL/2.0/
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

            # TODO: Implement higher order logic here.
            #
            # Define higher order logic centered at i but with collective adoption of
            # majority. Selection of i will be done using at random with sufficient
            # density to cover all the space. We use here interactants.
            
            # Obtain a random sample set corresponding to centroids
            centroids = random.sample(self.agent_list, math.ceil(self.n/self.interactants))
            
            # For all centroids, compute the neighbors, determine f and change the value of the entire
            # partition
            
            for c in centroids:
                # The partition includes itself
                partition = self.get_neighbors(c).append(c)
                
                # Compute the value of the partition
                f_part = self.compute_f(partition)
                
                # Set f and the state collectively
                new_fs.update(dict.fromkeys(partition, f_part))
                
                if f_part > self.f_threshold:
                    new_states.update(dict.fromkeys(partition, 1))
                else:
                    new_states.update(dict.fromkeys(partition, 0))

            self.agent_states = new_states
            self.agent_fs = new_fs
            
    def compute_f(self, partition: list()):
        '''
        The value of f is computed in bloc for a subset of the agents
        '''
        total = 0.0
    
        k = len(partition)
        
        if k == 0:
            return 0
        else:
            for j in partition:
                total += self.agent_states[j]
                
            total /= k
            return total
    
    def change_partition(self, partition, f, new_state):
        
        return new_state
    
    def get_opinion(self, i):
        return self.agent_states[i]
    
    def get_f(self, i):
        return self.agent_fs[i]