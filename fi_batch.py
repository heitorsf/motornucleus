from netpyne import specs
from netpyne.batch import Batch
import numpy as np

def batchMorphFI():
    # Create variable of type ordered dictionary (NetPyNE's customized version)
    params = specs.ODict()
    
    # fill in with parameters to explore and range of values (key has to coincide with a variable in simConfig)
    #params['synMechTau2'] = [3.0, 5.0, 7.0]
    params['soma_morph_factor'] = [0.9, 1.0, 1.1]
    #params['IClamp_amp'] = [amp for amp in np.linspace(1,30,20,endpoint=True)]
    params['IClamp_amp'] = [i for i in np.linspace(5,30,40)]
    
    # create Batch object with parameters to modify, and specifying files to use
    b = Batch(params=params, cfgFile='fi_cfg.py', netParamsFile='fi_netParams.py',)
    
    # Set output folder, grid method (all param combinations), and run configuration
    b.batchLabel = 'somaMorph'
    b.saveFolder = 'fi_data'
    b.method = 'grid'
    b.runCfg = {'type': 'mpi_bulletin',
                        'script': 'fi_init.py',
                        'skip': True}
    
    # Run batch simulations
    b.run()

# Main code
if __name__ == '__main__':
    batchMorphFI()
