from netpyne import sim, specs

from mn_cfg import cfg

# Network parameters
netParams = specs.NetParams()

############################
## Cells: Specify cell types
############################

netParams.importCellParams(
        label='PYR_HH_rule',
        conds={'cellType': 'PYR', 'cellModel': 'HH'},
        fileName='HHCellFile.py',
        cellName='HHCellClass',
        importSynMechs=False)
netParams.cellParams['PYR_HH_rule']['secs']['soma']['threshold'] = 0

netParams.cellParams['artif_NetStim'] = {
        'cellModel': 'NetStim'}

##############
## Populations
##############

netParams.popParams['HH_pop'] = {
        'cellType': 'PYR',
        'numCells': cfg.numCells,
        'cellModel': 'HH'}

# Artificial spike generators (NetStims)
netParams.popParams['descDrive'] = {
        'cellType': 'artif_NetStim',
        'numCells': 5,
        'rate': 50,  # Hz
        'noise': 0.5,
        'yRange': [0,100]}

######################
## Synaptic mechanisms
######################
# Note: gmax is determined by weight in connParams
netParams.synMechParams['exc'] = {'mod': 'Exp2Syn',
                                  'tau1': 0.1,
                                  'tau2': 5.0,
                                  'e': 0}

#####################
## Connectivity rules
#####################
netParams.connParams['descDrive->motorNucleus'] = {     #label
        'preConds': {'pop': 'descDrive'},
        'postConds': {'pop': 'HH_pop'},
        #'sec': 'dend',              # postsyn section
        #'loc': 0.5,                 # postsyn section location
        'connFunc': 'fullConn',
  		#'probability': 1.,
        'weight': 0.01,      # synaptic weight (gmax for Exp2Syn)
        'delay': 5,        # transmission delay(ms) = 1 ms (1 synpase)
        'synMech': 'exc'}           # synaptic mechanism
