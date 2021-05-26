from netpyne import sim, specs

from mn_cfg import cfg
from nappCell_file import alphaMotorNeuron

# Network parameters
netParams = specs.NetParams()

############################
## Cells: Specify cell types
############################
netParams.cellParams['alphaMN'] = alphaMotorNeuron

netParams.cellParams['artif_NetStim'] = {
        'cellModel': 'NetStim'}

##############
## Populations
##############
netParams.popParams['MN_pop'] = {
    'cellType': 'alphaMN',
    'numCells': cfg.numCells}

# Artificial spike generators (NetStims)
netParams.popParams['descDrive'] = {
        'cellType': 'artif_NetStim',
        'numCells': 400,
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
                                  'e': 70.}

#####################
## Connectivity rules
#####################
netParams.connParams['descDrive->motorNucleus'] = {     #label
        'preConds': {'pop': 'descDrive'},
        'postConds': {'pop': 'MN_pop'},
        'sec': 'dend',              # postsyn section
        'loc': 0.5,                 # postsyn section location
        #'connFunc': 'fullConn',
  		'probability': 0.3,
        'weight': 0.05,      # synaptic weight (gmax for Exp2Syn)
        'delay': 1,        # transmission delay(ms) = 1 ms (1 synpase)
        'synMech': 'exc'}           # synaptic mechanism
