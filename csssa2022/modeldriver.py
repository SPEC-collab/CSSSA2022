# Copyright (c) 2022 SPEC collaborative. All rights reserved.
#
# This program and the accompanying materials are made available under the
# terms of the Mozilla Public License v2.0 which accompanies this distribution,
# and is available at https://www.mozilla.org/en-US/MPL/2.0/
import uuid

from csssa2022.database import Database
from csssa2022.network import NetworkEnsembleFactory
from csssa2022.selections import InteractionType, NetworkType, SimulationType
from csssa2022.dyadicmatrixvotermodel import DyadicMatrixVoterModel
from csssa2022.dyadicabmvotermodel import DyadicABMVoterModel
from csssa2022.higherordermatrixvotermodel import HigherOrderMatrixVoterModel
from csssa2022.higherorderabmvotermodel import HigherOrderABMVoterModel

class ModelDriver:
    '''
    This class takes care of executing a model within an ensemble.
    '''
    
    @staticmethod
    def run_model(simulation: SimulationType, interaction: InteractionType, network: NetworkType,
                  interactants, n, max_steps, ensemble_size, initial_state, filename):
        # Generate a unique uuid1 per experiment
        uuid_exp = str(uuid.uuid1())
        
        # Report
        print(f'Running: {uuid_exp} - {simulation.value}, {interaction.value}, {network.value} - S: {n} <M>: {initial_state}')
                
        # Create a new database or open an existing one at the corresponding filename
        db = Database(filename)
        db.connect()
                
        # Generate an ensemble of networks
        nef = NetworkEnsembleFactory()
        network_ensemble = nef.make_ensemble(n, ensemble_size, network)
        
        # Interate over the ensemble to compute and store each model
        for i, net in network_ensemble.items():
            # Report start of ensemble point
            print(f'Computing ensemble point {i}')
            
            # Instantiate the right type of model
            model = None
            
            if simulation == SimulationType.MATRIX:
                if interaction == InteractionType.DYADIC:
                    model = DyadicMatrixVoterModel(uuid_exp, i, interactants, initial_state, net, n, max_steps, db)
                else:
                    model = HigherOrderMatrixVoterModel(uuid_exp, i, interactants, initial_state, net, n, max_steps, db)
            else:
                if interaction == InteractionType.DYADIC:
                    model = DyadicABMVoterModel(uuid_exp, i, interactants, initial_state, net, n, max_steps, db)
                else:
                    model = HigherOrderABMVoterModel(uuid_exp, i, interactants, initial_state, net, n, max_steps, db)
                    pass
                
            # Run the model
            model.run()
            
            # Commit the outcomes of the current ensemble
            db.checkpoint()
        
        # Close the database
        db.close()
        
        # Report finalization
        print('Ensemble computed')
        