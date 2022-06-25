# Copyright (c) 2022 SPEC collaborative. All rights reserved.
#
# This program and the accompanying materials are made available under the
# terms of the Mozilla Public License v2.0 which accompanies this distribution,
# and is available at https://www.mozilla.org/en-US/MPL/2.0/
import random
import math

from networkx import Graph
from abc import ABC, abstractmethod
from operator import itemgetter

from numpy import average
from csssa2022.record import Record
from csssa2022.summary import Summary
from csssa2022.database import Database
from csssa2022.network import NetworkUtil


class AbstractVoterModel(ABC):
    
    def __init__(self, uuid_exp, ensemble_id, simtype, interactions, interactants,
                 initial_state, network: Graph, n, max_steps, db: Database, **kwargs):
        # Constants
        self.f_threshold = 0.5
        
        # General elements
        self.running = True
        self.stepno = 0
        self.max_steps = max_steps
        
        # Model id
        self.uuid_exp = uuid_exp
        
        # Voter specific attributes
        self.simtype = simtype
        self.interactions = interactions
        self.interactants = interactants
        self.initial_state = initial_state
        self.network = network
        self.n = n
        self.ensemble_id = ensemble_id
        
        # Create agents, separate them into initial states of yes/no        
        self.agent_list = list(range(0, self.n))
        self.initial_yes = random.sample(self.agent_list, math.ceil(self.n*self.initial_state))    
        self.initial_no = list(set(self.agent_list) - set(self.initial_yes))
        
        # Set the database where to store elements
        self.db = db
        
        # Obtain the respective id to node translators
        self.n_to_node, self.node_to_n = NetworkUtil.make_rosetta(network)
        
    def agents(self):
        return list(self.agent_list)
        
    @abstractmethod
    def step(self):
        pass
    
    @abstractmethod
    def compute_f(self, i):
        pass
    
    @abstractmethod
    def get_opinion(self, i):
        pass
    
    @abstractmethod
    def get_f(self, i):
        pass
    
    def get_neighbors(self,i):
        '''
        In this method, we make use of the node-id translation services constructed so far
        '''
        node = self.n_to_node[i]
        neighbors = self.network.neighbors(node)
        
        if neighbors is None:
            neighbors = []
        else:
            return list(itemgetter(*neighbors)(self.node_to_n))
    
    def agent_to_record(self, i):
        return Record(self.uuid_exp,
                      self.ensemble_id,
                      self.stepno,
                      i,
                      self.get_opinion(i),
                      self.get_f(i))
    
    def step_to_summary(self):
        return Summary(self.uuid_exp,
                      self.ensemble_id,
                      self.stepno,
                      self.count_yes(),
                      self.count_no(),
                      self.average_f())
    
    def count_yes(self):
        return self.count_opinion(1)
        
    def count_no(self):
        return self.count_opinion(0)
    
    def count_opinion(self, opinion):
        total = 0
        
        for i in self.agent_list:
            if self.get_opinion(i) == opinion:
                total += 1
                
        return total
    
    def average_f(self):
        total = 0
        
        for i in self.agent_list:
            total += self.get_f(i)
                
        return total/self.n
    
    def save(self, i):
        self.db.insert_record(self.agent_to_record(i))
    
    def save_all(self):
        '''
        Save all takes all agents and, depending on the implementation of agent_to_record,
        takes care of saving one full iteration. Commit occurs at the end of the simulation
        '''
        #for i in self.agent_list:
        #    self.save(i)
            
        self.db.insert_summary(self.step_to_summary())

    def run(self):
        while self.running:
            # Perform the step
            self.step()
            
            # Save all agent states
            self.save_all()
            
             # Update the step counter
            self.stepno += 1