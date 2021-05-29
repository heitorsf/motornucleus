from netpyne import sim, specs

from mn_cfg import cfg
from nappCellFile import alphaMotorNeuron

# Network parameters
netParams = specs.NetParams()

############################
## Cells: Specify cell types
############################
#netParams.defaultThreshold = 50.0
netParams.cellParams['alphaMN_netpyne'] = alphaMotorNeuron

netParams.importCellParams(
        label = 'alphaMN_py',
        conds = {'cellType': 'alphaMN_py'},
        fileName = 'MotorNeuron.py',
        cellName = 'AlphaMotorNeuron',
        importSynMechs = False)
netParams.cellParams['alphaMN_py']['secs']['soma']['vinit'] = 0.0
netParams.cellParams['alphaMN_py']['secs']['dend']['vinit'] = 0.0

netParams.importCellParams(
        label='PowersEtAl2012',
        conds={'cellType': 'FRMotoneuron'},
        fileName = 'MNPowers_joe.py',
        cellName = 'FRMotoneuronNaHH',
        importSynMechs = False)

netParams.cellParams['artif_NetStim'] = {
        'cellModel': 'NetStim'}

##############
## Populations
##############
netParams.popParams['MN_pop'] = {
    #'cellType': 'alphaMN_netpyne',
    #'cellType': 'alphaMN_py',
    'cellType': 'FRMotoneuron',
    'numCells': cfg.numCells}

# Artificial spike generators (NetStims)
netParams.popParams['descDrive'] = {
        'cellType': 'artif_NetStim',
        'numCells': 1,
        'rate': cfg.descDrive_rate,  # Hz
        'noise': 0.5,
        'yRange': [0,100]}

######################
## Synaptic mechanisms
######################
# Note: gmax is determined by weight in connParams
netParams.synMechParams['exc'] = {'mod': 'Exp2Syn',
                                  'tau1': 0.2,
                                  'tau2': 0.2,
                                  'e': 0.}

#####################
## Connectivity rules
#####################
netParams.connParams['descDrive->motorNucleus'] = {     #label
        'preConds': {'pop': 'descDrive'},
        'postConds': {'pop': 'MN_pop'},
        'sec': 'dend',              # postsyn section
        'loc': 0.5,                 # postsyn section location
        'connFunc': 'fullConn',
  		#'probability': 0.3,
        'weight': 0.5,      # synaptic weight (gmax for Exp2Syn)
        'delay': 1,        # transmission delay(ms) = 1 ms (1 synpase)
        'synMech': 'exc'}           # synaptic mechanism
