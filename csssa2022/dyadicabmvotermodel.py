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
        self.f = 0
        
    def step(self):
        self.compute_f()
        
        if self.f > self.model.f_threshold:
            self.opinion = 1
        else:
            self.opinion = 0
    
    def compute_f(self):
        total = 0.0
        neighbors = self.model.get_neighbors(self.unique_id)
        k = len(neighbors)
        
        if k == 0:
            self.f = 0
        else:
            # Filter agents by neighbors
            filtered = filter(lambda a: a.unique_id in neighbors, self.model.schedule.agents)
            
            for ag in filtered:
                total += ag.opinion
                
            total /= k
            self.f = total
        
class DyadicABMVoterModel(AbstractVoterModel,Model):
    '''
    A dyadic ABM voter model
    '''
    def __init__(self, uuid_exp, ensemble_id, interactants, initial_state, network: Graph, n, max_steps, db, **kwargs):
        super().__init__(uuid_exp=uuid_exp,
                         ensemble_id=ensemble_id,
                         simtype=SimulationType.ABM,
                         interactions=InteractionType.DYADIC,
                         interactants=interactants, 
                         initial_state=initial_state,
                         network=network,
                         n=n,
                         max_steps=max_steps,
                         db=db,
                         **kwargs)
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
        return self.get_agent(i).opinion
    
    def get_f(self, i):
        return self.get_agent(i).f
    
    def get_agent(self, i):
        filtered = list(filter(lambda a: a.unique_id == i, self.schedule.agents))
        return filtered[0]