from netpyne import sim
import numpy as np

from syn_cfg import cfg
from syn_netParams import netParams

sim.create(netParams=netParams, simConfig=cfg, output=False)

rate_min = 200.
rate_max = 2000.

ramp_half_dur = (cfg.duration/2.)/cfg.dt
ramp_up = np.linspace(rate_min, rate_max, int(ramp_half_dur))
ramp_down = np.linspace(rate_max, rate_min, int(ramp_half_dur))

ramp_rate = np.concatenate((ramp_up, ramp_down))
ramp_interval = 1000./ramp_rate

t = sim.h.Vector(np.arange(0,cfg.duration, cfg.dt))
interval = sim.h.Vector(ramp_interval)
for i in range(cfg.numCells,len(sim.net.cells)):
    interval.play(sim.net.cells[i].hPointp._ref_interval, t, True)
#rate.play(sim.net.cells[0].stims[0]['hObj']._ref_rate, t, True)

"""
ramp_half_dur = (cfg.duration/2 - cfg.delay)/cfg.dt
ramp_up = np.linspace(5,100,int(ramp_half_dur))
ramp_down = np.linspace(100,5,int(ramp_half_dur))
delay = np.zeros(int(cfg.delay/cfg.dt))
silence = np.zeros(int(cfg.delay/cfg.dt))
"""
