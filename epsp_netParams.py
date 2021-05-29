from netpyne import sim, specs

from mn_cfg import cfg

# Network parameters
netParams = specs.NetParams()

############################
## Cells: Specify cell types
############################
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
    'cellType': 'FRMotoneuron',
    'numCells': cfg.numCells}

# Artificial spike generators (NetStims)
netParams.popParams['descDrive'] = {
        'cellType': 'artif_NetStim',
        'numCells': 1,
        'number': 1,
        'start': 100.,
        'noise': 0}

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
        'weight': 0.5,      # synaptic weight (gmax for Exp2Syn)
        'delay': 1,        # transmission delay(ms) = 1 ms (1 synpase)
        'synMech': 'exc'}           # synaptic mechanism
