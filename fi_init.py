from netpyne import sim

from fi_cfg import cfg
from fi_netParams import netParams

simConfig = cfg
sim.create(netParams=netParams, simConfig=cfg, output=False)

sim.simulate()
sim.analyze()
