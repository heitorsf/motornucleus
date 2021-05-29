from netpyne import specs

cfg = specs.SimConfig()

cfg.duration = 1.1*1e3
cfg.dt = 0.025
cfg.verbose = False
cfg.recordCells = ['all']
cfg.recordTraces = {'V_soma': {'sec':'soma', 'loc': 0.5, 'var': 'v'}}
cfg.recordStep = cfg.dt
cfg.filename = 'fI'
cfg.saveJson = True

cfg.analysis['plotRaster'] = False
cfg.analysis['plotTraces'] = {'include': [0], 'showFig': False}

cfg.saveDataInclude = ['simData', 'simConfig', 'netParams', 'net']

# Variable parameters, used in netParams
cfg.numCells = 1
cfg.soma_morph_factor = 1.
cfg.IClamp_amp = 20.
