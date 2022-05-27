# Copyright (c) 2022 SPEC collaborative. All rights reserved.
#
# This program and the accompanying materials are made available under the
# terms of the Mozilla Public License v2.0 which accompanies this distribution,
# and is available at https://www.mozilla.org/en-US/MPL/2.0/
import networkx as nx
import math

from csssa2022.selections import NetworkType


class NetworkEnsembleFactory:
    
    def __init__(self):
        '''
        For each network type, we provide default values that can be modified. Not elegant for now
        but may be useful with more complex code.
        '''
        
        # Parameters
        self.params = {
            NetworkType.LATTICE_2D_RECTANGLE: [],
            NetworkType.LATTICE_2D_TRIANGLE: [],
            NetworkType.LATTICE_2D_HEXAGON: [],
            NetworkType.COMPLETE: [],
            NetworkType.HYPER_CUBE: [],
            NetworkType.WATTS_STROGATZ: [5, 0.4],
            NetworkType.POWER_LAW: [5, 0.6],
            NetworkType.ERDOS_RENYI: [0.1],
            NetworkType.BARABASI_ALBERT: [5]
        }
        
        # Whether the current network type admits reasonable variation, or 
        # if variation needs to come from the initial distribution of agents
        self.variates = {
            NetworkType.LATTICE_2D_RECTANGLE: False,
            NetworkType.LATTICE_2D_TRIANGLE: False,
            NetworkType.LATTICE_2D_HEXAGON: False,
            NetworkType.COMPLETE: False,
            NetworkType.WATTS_STROGATZ: True,
            NetworkType.POWER_LAW: True,
            NetworkType.HYPER_CUBE: False,
            NetworkType.ERDOS_RENYI: True,
            NetworkType.BARABASI_ALBERT: True
        }
        
    def make_ensemble(self, n, ensemble_size, nt: NetworkType):
        ensemble = {}
        
        for i in range(0, ensemble_size):
            ensemble[i] = self.make_network(n, nt)
            
        return ensemble
    
    def make_network(self, n, nt: NetworkType):
        '''
        We assume n = 2^k, k % 2 = 0
        '''
        k_half = math.isqrt(n)
        
        if nt == NetworkType.LATTICE_2D_RECTANGLE:
            return nx.grid_2d_graph(k_half, k_half, periodic=True)
        elif nt == NetworkType.LATTICE_2D_TRIANGLE:
            return nx.triangular_lattice_graph(k_half, k_half, periodic=True)
        elif nt == NetworkType.LATTICE_2D_HEXAGON:
            return nx.hexagonal_lattice_graph(k_half, k_half, periodic=True)
        elif nt == NetworkType.COMPLETE:
            return nx.complete_graph(n)
        elif nt == NetworkType.WATTS_STROGATZ:
            return nx.watts_strogatz_graph(n,
                                           k=self.params[NetworkType.WATTS_STROGATZ][0],
                                           p=self.params[NetworkType.WATTS_STROGATZ][1])
        elif nt == NetworkType.POWER_LAW:
            return nx.powerlaw_cluster_graph(n,
                                             m=self.params[NetworkType.POWER_LAW][0],
                                             p=self.params[NetworkType.POWER_LAW][1])
        elif nt == NetworkType.HYPER_CUBE:
            return nx.hypercube_graph(int(math.log2(n)))
        elif nt == NetworkType.ERDOS_RENYI:
            return nx.erdos_renyi_graph(n, p=self.params[NetworkType.ERDOS_RENYI][0])
        elif nt == NetworkType.BARABASI_ALBERT:
            return nx.barabasi_albert_graph(n, m=self.params[NetworkType.BARABASI_ALBERT][0])
        else:
            raise ValueError
        