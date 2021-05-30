from netpyne import sim
import numpy as np

from pool_cfg import cfg
from pool_netParams import netParams

modify_status = False

sim.create(netParams=netParams, simConfig=cfg, output=False)

soma_diam = np.linspace(45,65,cfg.numCells,endpoint=True)

for c,cell in enumerate(sim.net.cells[:cfg.numCells]):
    prop = {
        'conds': {'pop': 'MN_pop'},
        'secs': { 'soma': {
            'geom': { 'diam': soma_diam[c]}}}}
    sim.net.cells[c].modify(prop)

modify_status = True
