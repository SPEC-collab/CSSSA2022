# Copyright (c) 2022 SPEC collaborative. All rights reserved.
#
# This program and the accompanying materials are made available under the
# terms of the Mozilla Public License v2.0 which accompanies this distribution,
# and is available at https://www.mozilla.org/en-US/MPL/2.0/
import random
import math

from abc import ABC, abstractmethod
from csssa2022.database import Database

class AbstractVoterModel(ABC):
    
    def __init__(self, uuid, ensemble_id, type, interactions, interactants,
                 initial_state, network, n, gamma, max_steps, db: Database):
        # General elements
        self.running = True
        self.stepno = 0
        self.max_steps = max_steps
        
        # Model id
        self.uuid = uuid
        
        # Voter specific attributes
        self.type = type
        self.interactions = interactions
        self.interactants = interactants
        self.initial_state = initial_state
        self.network = network
        self.n = n
        self.gamma = gamma
        self.ensemble_id = ensemble_id
        
        # Create agents, separate them into initial states of yes/no
        self.agent_list = list(range(0, self.n))
        self.initial_yes = random.sample(self.agent_list, math.ceil(n*self.initial_state))
        self.initial_no = list(set(self.agent_list) - set(self.initial_yes))
        
        # Set the database where to store elements
        self.db = db
        
    def agents(self):
        return list(self.agent_list)
    
    @abstractmethod
    def agent_at(self, i):
        pass
        
    @abstractmethod
    def step(self):
        pass
    
    @abstractmethod
    def compute_f(self, i):
        pass
    
    @abstractmethod
    def agent_to_record(self, i):
        pass
    
    def save(self, i):
        self.db.insert(self.agent_to_record(i))
    
    def save_all(self):
        '''
        Save all takes all agents and, depending on the implementation of agent_to_record,
        takes care of saving one full iteration. Commit occurs at the end of the simulation
        '''
        for i in self.agent_list:
            self.save(i)
