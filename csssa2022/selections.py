# Copyright (c) 2022 SPEC collaborative. All rights reserved.
#
# This program and the accompanying materials are made available under the
# terms of the Mozilla Public License v2.0 which accompanies this distribution,
# and is available at https://www.mozilla.org/en-US/MPL/2.0/
from enum import Enum


class NetworkType(Enum):
    LATTICE_2D_RECTANGLE = 'l2dr'
    LATTICE_2D_TRIANGLE = 'l2dt'
    LATTICE_2D_HEXAGON = 'l2dh'
    COMPLETE = 'k_n'
    WATTS_STROGATZ = 'ws' 
    POWER_LAW = 'pl'
    HYPER_CUBE = 'hc'
    ERDOS_RENYI = 'er'
    BARABASI_ALBERT = 'ba'

class InteractionType(Enum):
    DYADIC = 'dy',
    HIGHER_ORDER = 'ho'
    
class SimulationType(Enum):
    MATRIX = 'matrix'
    ABM = 'abm'