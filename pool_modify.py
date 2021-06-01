from netpyne import sim
import numpy as np

from pool_cfg import cfg
from pool_netParams import netParams

modify_status = False

sim.create(netParams=netParams, simConfig=cfg, output=False)

# Modify cells params
soma_diam = np.linspace(40,70,cfg.numCells,endpoint=True)
soma_g = np.linspace(1./800.,1./200.,cfg.numCells,endpoint=True)
for c,cell in enumerate(sim.net.cells[:cfg.numCells]):
    prop = {
        'conds': {'pop': 'MN_pop'},
        'secs': { 'soma': {
            'geom': {
                'diam': soma_diam[c],
                'L': soma_diam[c]},
            'mechs': {
                'pas': {'g': soma_g[c]}}}}}
    sim.net.cells[c].modify(prop)

# Play vector to NetStim interval
rate_min = 1.
rate_max = 20.
ramp_up = np.linspace(rate_min, rate_max, int(cfg.dur_up/cfg.dt))
ramp_down = np.linspace(rate_max, rate_min, int(cfg.dur_down/cfg.dt))
plato = rate_max * np.ones(int(cfg.dur_plato/cfg.dt))
ramp_rate = np.concatenate((ramp_up, plato, ramp_down))
ramp_interval = 1000./ramp_rate
t = sim.h.Vector(np.arange(0,cfg.duration, cfg.dt))
interval = sim.h.Vector(ramp_interval)
for i in range(cfg.numCells,len(sim.net.cells)):
    interval.play(sim.net.cells[i].hPointp._ref_interval, t, True)

modify_status = True
