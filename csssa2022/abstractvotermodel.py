# Copyright (c) 2022 SPEC collaborative. All rights reserved.
#
# This program and the accompanying materials are made available under the
# terms of the Mozilla Public License v2.0 which accompanies this distribution,
# and is available at https://www.mozilla.org/en-US/MPL/2.0/
import random


class AbstractVoterModel:
    
    def __init__(self, type, interactions, interactants, initial_state,
                 network, n, gamma, ensemble, max_steps):
        # General elements
        self.running = True
        self.stepno = 0
        self.max_steps = max_steps
        
        # Voter specific attributes
        self.type = type
        self.interactions = interactions
        self.interactants = interactants
        self.network = network
        self.n = n
        self.gamma = gamma
        self.ensemble = ensemble
        
        # Create agents and store their opinion as a map
        self.agents = {}
        all_agents = list(range(0, self.n))
        
       
        
    def agents(self):
        return list(self.agents)
    
    def agent_at(self, i):
        if i in self.agents:
            return self.agents[i]
        else:
            raise ValueError
        
    def step(self):
        pass
    
    def save(self):
        pass
    
    def run_model(self):
        if self.running:
            while self.stepno < self.max_steps:
                self.step()
