# Copyright (c) 2022 SPEC collaborative. All rights reserved.
#
# This program and the accompanying materials are made available under the
# terms of the Mozilla Public License v2.0 which accompanies this distribution,
# and is available at https://www.mozilla.org/en-US/MPL/2.0/
from dataclasses import dataclass
from csssa2022.selections import SimulationType, InteractionType, NetworkType

@dataclass
class Simulation:
    '''
    Class that represents a standard record in the database to unify matrix and ABM
    model output.
    '''
    uuid_exp: str
    ensemble_size: int
    n: int
    simulation_type: SimulationType
    interaction_type: InteractionType
    interactants: int
    initial_state: float
    network_type: NetworkType
    max_steps: int