from netpyne import specs

cfg = specs.SimConfig()

cfg.dur_up = 6.*1e3
cfg.dur_plato = 1.*1e3
cfg.dur_down = 6.*1e3
cfg.duration = cfg.dur_up + cfg.dur_plato + cfg.dur_down
cfg.dt = 0.025
cfg.verbose = False
cfg.recordCells = ['all']
cfg.recordTraces = {'V_soma': {'sec':'soma', 'loc': 0.5, 'var': 'v'}}
cfg.recordStep = cfg.dt
cfg.filename = "pool_output"
cfg.saveJson = True

cfg.analysis['plotRaster'] = True
cfg.analysis['plotTraces'] = {'include': [0], 'showFig': True}
cfg.analysis['plot2Dnet'] = False #True  # Plot 2D net cells and connections
cfg.analysis['plotConn'] = False #True

# Variable parameters, used in netParams
cfg.numCells = 20 
cfg.numNetStim = 400
cfg.connProb = 0.3
cfg.descDrive_rate = 100.
