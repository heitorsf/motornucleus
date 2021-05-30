from netpyne import sim
import numpy as np
import matplotlib.pyplot as plt
import nerlabtools as ner

from pool_cfg import cfg
from pool_netParams import netParams

from pool_modify import modify_status

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
