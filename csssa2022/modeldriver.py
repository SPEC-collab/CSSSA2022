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
    
    def run_model(ensemble_size, simulation: SimulationType, interaction: InteractionType,
                  interactants, initial_state, network: NetworkType, n, max_steps, filename):
        # Generate a unique uuid1 per experiment
        uuid_exp = uuid.uuid1()
        
        # Create a new database or open an existing one at the corresponding filename
        db = Database(filename)
        db.connect()
                
        # Generate an ensemble of networks 
        network_ensemble = NetworkEnsembleFactory.make_ensemble(n, ensemble_size, network)
        
        # Interate over the ensemble to compute and store each model
        for i, net in network_ensemble:
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
        