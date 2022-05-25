# Copyright (c) 2022 SPEC collaborative. All rights reserved.
#
# This program and the accompanying materials are made available under the
# terms of the Mozilla Public License v2.0 which accompanies this distribution,
# and is available at https://www.mozilla.org/en-US/MPL/2.0/
from networkx import Graph
from csssa2022.selections import InteractionType, SimulationType
from csssa2022.abstractvotermodel import AbstractVoterModel


class HigherOrderVoterModel(AbstractVoterModel):
    '''
    This voter model only has dyadic interactions, uses state vector to represent agents, and
    updates all state agents simultaneously at the end of one simulation step.
    '''
    def __init__(self, uuid_exp, ensemble_id, interactants, initial_state, network: Graph, n, max_steps, db):
        super().__init__(uuid_exp, ensemble_id, SimulationType.MATRIX, InteractionType.HIGHER_ORDER,
                         interactants, initial_state, network, n, max_steps, db)
        
    def step(self):
        if self.stepno == self.max_steps:
            self.running = False
        else:
            # Compute a new map for all agents and replace the old map
            new_states = {}
            
            # TODO: Implement higher order logic here.
            #
            # Define higher order logic centered at i but with collective adoption of
            # majority. Selection of i will be done using at random with sufficient
            # density to cover all the space. We use here interactants.        
            self.agent_states = new_states

            
    def compute_f(self, i):
        # TODO: compute using interactant logic
        pass
    
    def get_opinion(self, i):
        return self.agent_states[i]