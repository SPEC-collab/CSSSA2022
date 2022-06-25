# Copyright (c) 2022 SPEC collaborative. All rights reserved.
#
# This program and the accompanying materials are made available under the
# terms of the Mozilla Public License v2.0 which accompanies this distribution,
# and is available at https://www.mozilla.org/en-US/MPL/2.0/
from dataclasses import dataclass
from csssa2022.selections import SimulationType, InteractionType, NetworkType

@dataclass
class Summary:
    '''
    Class that summarizes data to avoid excesive plotting time.
    '''
    uuid_exp: str
    ensemble_id: int
    step_id: int
    total_yes: int
    total_no: int
    avg_f: float