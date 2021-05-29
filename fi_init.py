from netpyne import sim
import numpy as np
import matplotlib.pyplot as plt
import nerlabtools as ner

#plt.ion()

from fi_cfg import cfg
from fi_netParams import netParams

simConfig = cfg
sim.create(netParams=netParams, simConfig=cfg, output=False)

sim.simulate()
sim.analyze()
