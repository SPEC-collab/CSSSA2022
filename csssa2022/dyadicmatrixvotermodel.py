# Copyright (c) 2022 SPEC collaborative. All rights reserved.
#
# This program and the accompanying materials are made available under the
# terms of the Mozilla Public License v2.0 which accompanies this distribution,
# and is available at https://www.mozilla.org/en-US/MPL/2.0/
from networkx import Graph
from csssa2022.selections import InteractionType, SimulationType
from csssa2022.abstractvotermodel import AbstractVoterModel


class DyadicMatrixVoterModel(AbstractVoterModel):
    '''
    This voter model only has dyadic interactions, uses state vector to represent agents, and
    updates all state agents simultaneously at the end of one simulation step.
    '''
    def __init__(self, uuid_exp, ensemble_id, interactants, initial_state, network: Graph, n, max_steps, db):
        super().__init__(uuid_exp, ensemble_id, SimulationType.MATRIX, InteractionType.DYADIC,
                         interactants, initial_state, network, n, max_steps, db)
        
        # We represent the agent store as a dictionary
        self.agent_states = {}
        
        # Add agents depending on their initial opinion
        for i in self.initial_yes:
            self.agent_store[i] = 1
            
        for i in self.initial_no:
            self.agent_store[i] = 0
            
    def step(self):
        if self.stepno == self.max_steps:
            self.running = False
        else:
            # Compute a new map for all agents and replace the old map
            new_states = {}
            
            for i in self.agent_states.values():
                if self.compute_f(i) > self.__f_threshold:
                    new_states[i] = 1
                else:
                    new_states[i] = 0
                    
            self.agent_states = new_states
            
    def compute_f(self, i):
        total = 0.0
        neighbors = list(self.network.neighbors(i))
        k = len(neighbors)
        
        if k == 0:
            return 0
        else:
            for j in neighbors:
                total += self.agent_states[j]
                
            total /= k
            return total
            
    def get_opinion(self, i):
        return self.agent_states[i]