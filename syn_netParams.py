from netpyne import sim, specs

from syn_cfg import cfg

# Network parameters
netParams = specs.NetParams()

############################
## Cells: Specify cell types
############################
netParams.cellParams['artif_NetStim'] = {
        'cellModel': 'NetStim'}

netParams.defaultThreshold = -10.0

netParams.importCellParams(
        label='PowersEtAl2012',
        conds={'cellType': 'FRMotoneuron'},
        fileName = 'MNPowers_joe.py',
        cellName = 'FRMotoneuronNaHH',
        importSynMechs = False)

##############
## Populations
##############
netParams.popParams['MN_pop'] = {
    'cellType': 'FRMotoneuron',
    'numCells': cfg.numCells}

# Artificial spike generators (NetStims)
netParams.popParams['descDrive'] = {
        'cellType': 'artif_NetStim',
        'numCells': cfg.numNetStim,
        'rate': 30,  # Hz
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
        #'sec': 'soma',              # postsyn section
        'loc': 0.1,                 # postsyn section location
        'connFunc': 'fullConn',
  		#'probability': 0.3,
        'weight': 1.0,  # 0.5,      # synaptic weight (gmax for Exp2Syn)
        'delay': 1,        # transmission delay(ms) = 1 ms (1 synpase)
        'synMech': 'exc'}           # synaptic mechanism
