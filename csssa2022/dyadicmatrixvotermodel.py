# Copyright (c) 2022 SPEC collaborative. All rights reserved.
#
# This program and the accompanying materials are made available under the
# terms of the Mozilla Public License v2.0 which accompanies this distribution,
# and is available at https://www.mozilla.org/en-US/MPL/2.0/
import uuid

from csssa2022.selections import NetworkType, InteractionType, SimulationType
from csssa2022.abstractvotermodel import AbstractVoterModel


class DyadicMatrixVoterModel(AbstractVoterModel):
    '''
    This voter model only has dyadic interactions, uses state vector to represent agents, and
    updates all state agents simultaneously at the end of one simulation step.
    '''
    def __init__(self, uuid_exp, ensemble_id, interactants, initial_state, network, n, gamma, max_steps, db):
        super().__init__(uuid_exp, ensemble_id, SimulationType.ABM, InteractionType.DYADIC,
                         interactants, initial_state, network, n, gamma, max_steps, db)

