from netpyne import sim
import numpy as np
import matplotlib.pyplot as plt
import nerlabtools as ner
import sigUtils as sg

from syn_cfg import cfg
from syn_netParams import netParams

import syn_modiify

sim.simulate()
sim.analyze()

spkt_nrn = np.array(sim.simData['spkt'])
spkid_nrn = np.array(sim.simData['spkid'])
t = np.array(sim.simData['t'])

spkt = np.array([spkt_nrn[spkid_nrn==0]])
ifreq = sg.instFreqHanning(t,spkt,w_size=300)[0]
plt.figure();plt.plot(t,ifreq)

v_soma = np.array(sim.simData['V_soma']['cell_0'])
v_dend = np.array(sim.simData['V_dend']['cell_0'])
t = np.array(sim.simData['t'])
plt.figure()
plt.xlabel("Time (s)")
plt.ylabel("Memb. potential (mV)")
plt.plot(t/1e3,v_soma,label="soma")
plt.plot(t/1e3,v_dend,label="dend")
plt.legend()
#plt.set_xlim((0,10))

"""
spkt_list = []
for cell_id in range(cfg.numCells):
    spkt_list.append(spkt_nrn[spkid_nrn == cell_id])

spkt = ner.spktFromList(spkt_list)
force = ner.muscularForce(spkt, t, plotForce=True)
"""
