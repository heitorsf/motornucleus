from netpyne import specs

cfg = specs.SimConfig()

cfg.duration = 10.2*1e3
cfg.dt = 0.025
cfg.stimdelay = 100.  # ms
cfg.verbose = False
cfg.recordCells = ['all']
cfg.recordTraces = {
    'V_soma': {'sec':'soma', 'loc': 0.5, 'var': 'v'},
    'V_dend': {'sec':'dend', 'loc': 0.5, 'var': 'v'}}
cfg.recordStep = cfg.dt
cfg.savePickle = False        # Save params, network and sim output to pickle file
cfg.filename = 'model_output2'
cfg.saveJson = True

cfg.analysis['plotRaster'] = False
cfg.analysis['plotTraces'] = {'include': [0], 'showFig': True}
cfg.analysis['plot2Dnet'] = False #True  # Plot 2D net cells and connections
cfg.analysis['plotConn'] = False #True

# Variable parameters, used in netParams
cfg.numCells = 1
cfg.descDrive_rate = 1.
