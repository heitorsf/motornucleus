from netpyne import specs
import numpy as np

cfg = specs.SimConfig()

cfg.duration = 2.*1e3
cfg.dt = 0.025
cfg.verbose = False
cfg.recordCells = ['all']
cfg.recordTraces = {
    'V_soma': {'sec':'soma', 'loc': 0.5, 'var': 'v'}}
    #'I_IClamp': {'rampCurrent': }
cfg.recordStep = cfg.dt
cfg.savePickle = False        # Save params, network and sim output to pickle file
cfg.filename = 'f-I'
cfg.saveJson = True

cfg.analysis['plotRaster'] = False
cfg.analysis['plotTraces'] = {'include': [0], 'showFig': True}
cfg.analysis['plot2Dnet'] = False # Plot 2D net cells and connections
cfg.analysis['plotConn'] = False

# Variable parameters, used in netParams
cfg.numCells = 1
cfg.descDrive_rate = 1.

# Variable parameters, used in init
delta_amp = 30.
init_amp = -5.0
peak_amp = init_amp + delta_amp
ramp_up = np.linspace(init_amp, peak_amp, int((cfg.duration/cfg.dt)/2))
ramp_down = np.linspace(peak_amp, init_amp, int((cfg.duration/cfg.dt)/2))
triang = np.concatenate((ramp_up,ramp_down))

cfg.stimFunc = triang
cfg.soma_morph_factor = 1.
