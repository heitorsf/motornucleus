from netpyne import specs, sim

try:
    from __main__ import cfg  # for batches, import from the workspace
except:
    from fi_cfg import cfg  # for individual sims, import from file

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
cellRule_soma = netParams.cellParams['PowersEtAl2012']['secs']['soma']
cellRule_soma['geom']['diam'] = soma_diam * cfg.soma_morph_factor
cellRule_soma['geom']['L'] = soma_diam * cfg.soma_morph_factor

##############
## Populations
##############
netParams.popParams['MN_pop'] = {
    'cellType': 'FRMotoneuron',
    'numCells': 1}

####################
## Current injection
###################
netParams.stimSourceParams['pulseCurrent'] = {
    'type': 'IClamp',
    'dur': 1e3,
    'amp': cfg.IClamp_amp,
    'delay': 100}
netParams.stimTargetParams['pulseCurrent->MN_pop'] = {
    'source': 'pulseCurrent',
    'conds': {'pop': 'MN_pop'},
    'sec': 'soma',
    'loc': 0.5}
