# Copyright (c) 2022 SPEC collaborative. All rights reserved.
#
# This program and the accompanying materials are made available under the
# terms of the Mozilla Public License v2.0 which accompanies this distribution,
# and is available at https://www.mozilla.org/en-US/MPL/2.0/
from http.cookies import SimpleCookie
import sqlite3
from pathlib import Path
from csssa2022.record import Record
from csssa2022.simulation import Simulation
from csssa2022.summary import Summary


class Database:
    '''
    The database class takes care of storing simulation information.
    '''
    
    __simulations_sql = '''
    CREATE TABLE simulations
    (
        uuid_exp text,
        ensemble_size integer,
        n integer,
        simulation_type text,
        interaction_type text,
        interactants integer,
        initial_state real,
        network_type text,
        max_steps text
        )
    '''
    
    __records_sql = '''
    CREATE TABLE records
    (
        uuid_exp text,
        ensemble_id integer,
        step_id integer,
        agent_id integer,
        opinion integer,
        f_val real
    )
    '''
    
    __summaries_sql = '''
    CREATE TABLE summaries
    (
        uuid_exp text,
        ensemble_id integer,
        step_id integer,
        total_yes integer,
        total_no integer,
        avg_f real
    )
    '''
     
    def __init__(self, filename):
        self.filename = filename
        self.exists = Path(self.filename).is_file()
        self.con = None
        self.cur = None
        
    def connect(self):
        self.con = sqlite3.connect(self.filename)
        self.cur = self.con.cursor()
        
        if not(self.exists):
            self.cur.execute(self.__simulations_sql)
            self.cur.execute(self.__records_sql)
            self.cur.execute(self.__summaries_sql)
            self.con.commit()
    
    def insert_record(self, r: Record):
        self.cur.execute('insert into records values (?, ?, ?, ?, ?, ?)',
                         (
                             r.uuid_exp,
                             r.ensemble_id,
                             r.step_id,
                             r.agent_id,
                             r.opinion,
                             r.f_val
                        ))
        
    def insert_summary(self, s: Summary):
        self.cur.execute('insert into summaries values (?, ?, ?, ?, ?, ?)',
                         (
                             s.uuid_exp,
                             s.ensemble_id,
                             s.step_id,
                             s.total_yes,
                             s.total_no,
                             s.avg_f
                        ))
        
    def insert_simulation(self, s: Simulation):
        self.cur.execute('insert into simulations values (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                         (
                             s.uuid_exp,
                             s.ensemble_size,
                             s.n,
                             str(s.simulation_type.value),
                             str(s.interaction_type.value),
                             s.interactants,
                             s.initial_state,
                             str(s.network_type.value),
                             s.max_steps
                         ))

    def checkpoint(self):
        '''
        This function makes explicit when to send information to disk. For efficiecy,
        we want this associated per ensemble_id.
        '''
        self.con.commit()

    def close(self):
        self.con.commit()
        self.con.close()