from netpyne import sim, specs

from triang_cfg import cfg

# Network parameters
netParams = specs.NetParams()

netParams.defaultThreshold = -10.0

############################
## Cells: Specify cell types
############################
netParams.importCellParams(
        label='PowersEtAl2012',
        conds={'cellType': 'FRMotoneuron'},
        fileName = 'MNPowers_joe.py',
        cellName = 'FRMotoneuronNaHH',
        importSynMechs = False)
soma_diam = netParams.cellParams['PowersEtAl2012']['secs']['soma']['geom']['diam']

##############
## Populations
##############
netParams.popParams['MN_pop'] = {
    'cellType': 'FRMotoneuron',
    'numCells': 1}

####################
## Current injection
###################
netParams.stimSourceParams['rampCurrent'] = {
    'type': 'IClamp',
    'dur': 1e9,
    'delay': 0}
netParams.stimTargetParams['rampCurrent->MN_pop'] = {
    'source': 'rampCurrent',
    'conds': {
        'pop': 'MN_pop'},
    #'conds': {'cellType': 'MNMED'},
    'sec': 'soma',
    'loc': 0.5}
