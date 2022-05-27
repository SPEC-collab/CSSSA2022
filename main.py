# Copyright (c) 2022 SPEC collaborative. All rights reserved.
#
# This program and the accompanying materials are made available under the
# terms of the Mozilla Public License v2.0 which accompanies this distribution,
# and is available at https://www.mozilla.org/en-US/MPL/2.0/
import click

from csssa2022.selections import NetworkType, InteractionType, SimulationType
from csssa2022.modeldriver import ModelDriver

network_opts_map = {
    'l2dr': NetworkType.LATTICE_2D_RECTANGLE,
    'l2dt': NetworkType.LATTICE_2D_TRIANGLE,
    'l2dh': NetworkType.LATTICE_2D_HEXAGON,
    'k_n': NetworkType.COMPLETE,
    'ws': NetworkType.WATTS_STROGATZ,
    'pl': NetworkType.POWER_LAW,
    'hc': NetworkType.HYPER_CUBE,
    'er': NetworkType.ERDOS_RENYI, 
    'ba': NetworkType.BARABASI_ALBERT
}

interaction_opts_map = {
    'dy': InteractionType.DYADIC,
    'hord': InteractionType.HIGHER_ORDER
}

simulation_opts_map = {
    'matrix': SimulationType.MATRIX,
    'abm': SimulationType.ABM
}


def main():
    pass

if __name__ == "__main__":
    main()