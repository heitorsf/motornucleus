from netpyne import sim
import numpy as np
import matplotlib.pyplot as plt; plt.ion()
import nerlabtools as ner

from mn_cfg import cfg
from mn_netParams import netParams

output = sim.create(netParams=netParams, simConfig=cfg, output=True)
sim.simulate()
sim.analyze()

spkt_nrn = np.array(sim.simData['spkt'])
spkid_nrn = np.array(sim.simData['spkid'])
t = np.array(sim.simData['t'])

spkt_list = []
for cell_id in range(cfg.numCells):
    spkt_list.append(spkt_nrn[spkid_nrn == cell_id])

spkt = ner.spktFromList(spkt_list)
force = ner.muscularForce(spkt, t, plotForce=True)
