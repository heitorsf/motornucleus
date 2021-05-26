from netpyne import specs

cfg = specs.SimConfig()

cfg.duration = .5*1e3
cfg.dt = 0.025
cfg.verbose = False
cfg.recordCells = ['all']
cfg.recordTraces = {'v_soma': {'sec':'soma', 'loc': 0.5, 'var': 'v'}}
cfg.recordStep = cfg.dt
cfg.savePickle = False        # Save params, network and sim output to pickle file
cfg.saveJson = False

cfg.analysis['plotRaster'] = True
cfg.analysis['plotTraces'] = {'include': [0], 'oneFigPer': 'pop'}
cfg.analysis['plot2Dnet'] = False #True  # Plot 2D net cells and connections
cfg.analysis['plotConn'] = False #True

# Variable parameters, used in netParams
cfg.numCells = 50
