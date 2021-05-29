from netpyne import sim
import numpy as np
import matplotlib.pyplot as plt
import nerlabtools as ner

from mn_cfg import cfg
from epsp_netParams import netParams

sim.create(netParams=netParams, simConfig=cfg, output=False)
sim.simulate()
sim.analyze()

t = np.array(sim.simData['t'])
v = np.array(sim.simData['v_soma']['cell_0'])
#plt.ion()
plt.figure()
plt.title("EPSP")
plt.xlabel("Time (ms)")
plt.ylabel("Membrane potential (mV)")
plt.plot(t,v)
plt.tight_layout()
plt.show()
