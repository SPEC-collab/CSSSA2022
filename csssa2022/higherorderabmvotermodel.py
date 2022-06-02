# Copyright (c) 2022 SPEC collaborative. All rights reserved.
#
# This program and the accompanying materials are made available under the
# terms of the Mozilla Public License v2.0 which accompanies this distribution,
# and is available at https://www.mozilla.org/en-US/MPL/2.0/
import math
import random

from networkx import Graph
from csssa2022.selections import InteractionType, SimulationType
from csssa2022.abstractvotermodel import AbstractVoterModel
from mesa import Agent, Model
from mesa.time import RandomActivation


class HigherOrderABMVoterAgent(Agent):
    def __init__(self, unique_id: int, initial_opinion:int, model):
        super().__init__(unique_id, model)
        # Agents are not active unless the scheduler activates them during each model step
        self.active = False
        self.opinion = initial_opinion
        self.f = 0
        
    def step(self):
        if self.active:
            # Partition the graph based on current id
            partition = self.model.get_neighbors(self.unique_id) + [self.unique_id]
                
            # Compute the value of the partition
            f_part, interactants = self.compute_f(partition, self.model.interactants)
            
            if f_part > self.model.f_threshold:
                self.propagate(interactants, 1, f_part)
            else:
                self.propagate(interactants, 0, f_part)
            
            self.active = False
            
    def compute_f(self, partition, interactants):
        total = 0.0
    
        k = len(partition)
        
        # Take a subset of interactants when possible
        if k > interactants:
            sample = random.sample(partition, interactants)
            k = interactants
        else:
            sample = partition
        
        for j in sample:
            total += self.model.get_opinion(j)
            
        total /= k
        return total, sample
    
    def propagate(self, interactants, opinion, f):
        for i in interactants:
            self.model.get_agent(i).opinion = opinion
            self.model.get_agent(i).f = f
        
class HigherOrderABMVoterModel(AbstractVoterModel,Model):
    '''
    A higher-order ABM voter model
    '''
    def __init__(self, uuid_exp, ensemble_id, interactants, initial_state, network: Graph, n, max_steps, db, **kwargs):
        super().__init__(uuid_exp=uuid_exp,
                         ensemble_id=ensemble_id,
                         simtype=SimulationType.ABM,
                         interactions=InteractionType.HIGHER_ORDER,
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
            yes_agent = HigherOrderABMVoterAgent(i, 1, self)
            self.schedule.add(yes_agent)
            
        for i in self.initial_no:
            no_agent = HigherOrderABMVoterAgent(i, 0, self)
            self.schedule.add(no_agent)
            
    def step(self):
        if self.stepno == self.max_steps:
            self.running = False
        else:
           # Obtain a random sample set corresponding to centroids
           centroids = random.sample(self.agent_list, math.ceil(self.n/self.interactants))
           
           # Activate only these agents
           for a in filter(lambda a: a.unique_id in centroids, self.schedule.agents):
               a.active = True
            
           self.schedule.step()
           
    def compute_f(self, i):
        pass
    
    def get_opinion(self, i):
        return self.get_agent(i).opinion
    
    def get_f(self, i):
        filtered = list(filter(lambda a: a.unique_id == i, self.schedule.agents))
        return filtered[0].f
    
    def get_agent(self, i):
        filtered = list(filter(lambda a: a.unique_id == i, self.schedule.agents))
        return filtered[0]