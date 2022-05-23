# Copyright (c) 2022 SPEC collaborative. All rights reserved.
#
# This program and the accompanying materials are made available under the
# terms of the Mozilla Public License v2.0 which accompanies this distribution,
# and is available at https://www.mozilla.org/en-US/MPL/2.0/
from dataclasses import dataclass


@dataclass
class Record:
    '''
    Class that represents a standard record in the database to unify matrix and ABM
    model output.
    '''
    uuid: str
    ensemble_id: int
    step_id: int
    agent_id: int
    opinion: int
    f_val: float