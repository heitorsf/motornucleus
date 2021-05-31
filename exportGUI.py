from netpyne import specs,sim

cfg = specs.SimConfig()
netParams = specs.NetParams()

netParams.importCellParams(
        label='PowersNoMechs',
        conds={'cellType': 'FRMotoneuron'},
        fileName = 'MNPowersNoMechs.py',
        cellName = 'FRMotoneuronNaHH',
        importSynMechs = False)

netParams.popParams['MN_pop'] = {
    'cellType': 'FRMotoneuron',
    'numCells': 1}

cfg.dt = 0.025
cfg.duration = .2*1e3
cfg.verbose = False
cfg.filename = "exportGUI"
cfg.saveJson = True

sim.createSimulateAnalyze(netParams=netParams, simConfig=cfg)
