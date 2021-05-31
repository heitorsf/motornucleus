from netpyne import specs

cfg = specs.SimConfig()

cfg.dt = 0.025
cfg.duration = 20.*1e3
cfg.verbose = False
cfg.recordCells = ['all']
cfg.recordTraces = {
    'V_soma': {'sec':'soma', 'loc': 0.5, 'var': 'v'},
    'V_dend': {'sec':'dend', 'loc': 0.5, 'var': 'v'}}
cfg.recordStep = cfg.dt
cfg.filename = "syn_output"
cfg.saveJson = True

cfg.analysis['plotRaster'] = True
cfg.analysis['plotTraces'] = {'include': [0], 'showFig': True}
cfg.analysis['plot2Dnet'] = False #True  # Plot 2D net cells and connections
cfg.analysis['plotConn'] = False #True

# Variable parameters, used in netParams
cfg.numCells = 1 
cfg.numNetStim = 1
cfg.descDrive_rate = 100.
