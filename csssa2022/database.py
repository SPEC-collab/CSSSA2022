# Copyright (c) 2022 SPEC collaborative. All rights reserved.
#
# This program and the accompanying materials are made available under the
# terms of the Mozilla Public License v2.0 which accompanies this distribution,
# and is available at https://www.mozilla.org/en-US/MPL/2.0/
import sqlite3
from pathlib import Path
from csssa2022.record import Record


class Database:
    '''
    The database class takes care of storing simulation information.
    '''
    
    __table_sql = '''
    CREATE TABLE opinions
    (uuid text, ensemble_id integer, step_id integer, agent_id integer, opinion integer, f_val real)
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
            self.cur.execute(self.__table_sql)
            self.con.commit()
    
    def insert(self, r: Record):
        self.cur.execute('insert into opinions values (?, ?, ?, ?, ?, ?)',
                         (r.uuid, r.ensemble_id, r.step_id, r.agent_id, r.opinion, r.f_val))

    def checkpoint(self):
        '''
        This function makes explicit when to send information to disk. For efficiecy,
        we want this associated per ensemble_id.
        '''
        self.con.commit()

    def close(self):
        self.con.commit()
        self.con.close()