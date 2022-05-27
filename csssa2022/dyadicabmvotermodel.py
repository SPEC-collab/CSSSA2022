# Copyright (c) 2022 SPEC collaborative. All rights reserved.
#
# This program and the accompanying materials are made available under the
# terms of the Mozilla Public License v2.0 which accompanies this distribution,
# and is available at https://www.mozilla.org/en-US/MPL/2.0/
from networkx import Graph
from csssa2022.selections import InteractionType, SimulationType
from csssa2022.abstractvotermodel import AbstractVoterModel
from mesa import Agent, Model
from mesa.time import RandomActivation


class DyadicABMVoterAgent(Agent):
    def __init__(self, unique_id: int, initial_opinion:int, model: Model):
        super().__init__(unique_id, model)
        self.opinion = initial_opinion
        
    def step(self):
        if self.compute_f() > self.__f_threshold:
            self.opinion = 1 # Majority
        else:
            self.opinion = 0 # Stay the same
    
    def compute_f(self):
        total = 0.0
        neighbors = list(self.model.network.neighbors(self.unique_id))
        k = len(neighbors)
        
        if k == 0:
            return 0
        else:
            # Filter agents by neighbors
            filtered = [a for a in self.model.schedule.agents() if (a.unique_id in filtered)]
            
            for ag in filtered:
                total += ag.opinion
                
            total /= k
            return total
        
class DyadicABMVoterModel(Model,AbstractVoterModel):
    '''
    A dyadic ABM voter model
    '''
    def __init__(self, uuid_exp, ensemble_id, interactants, initial_state, network: Graph, n, max_steps, db):
        super(AbstractVoterModel, self).__init__(uuid_exp, ensemble_id, SimulationType.ABM, InteractionType.DYADIC,
                         interactants, initial_state, network, n, max_steps, db)
        # Create a scheduler
        self.schedule = RandomActivation(self)
        
        # Add agents based on precomputed proportions of initial opinions
        for i in self.initial_yes:
            yes_agent = DyadicABMVoterAgent(i, 1, self)
            self.schedule.add(yes_agent)
            
        for i in self.initial_no:
            no_agent = DyadicABMVoterAgent(i, 0, self)
            self.schedule.add(no_agent)

    def step(self):
        if self.stepno == self.max_steps:
            self.running = False
        else:
           self.schedule.step()
           
    def compute_f(self, i):
        # This is not defined for dyadic ABM models.
        pass
    
    def get_opinion(self, i):
        # Mesa does not have an elegant way to access one agent. We build it here.
        # Ideally, a function should exist that accesses the internal dictionary.
        filtered = [a for a in self.model.schedule.agents() if (a.unique_id == i)]
        return filtered[0]