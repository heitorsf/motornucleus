from netpyne import sim
import numpy as np
import matplotlib.pyplot as plt
import sigUtils as sg
import os

from syn_cfg import cfg
from syn_netParams import netParams

import syn_modiify

sim.simulate()
sim.analyze()

spkt_nrn = np.array(sim.simData['spkt'])
spkid_nrn = np.array(sim.simData['spkid'])
t = np.array(sim.simData['t'])

v_soma = np.array(sim.simData['V_soma']['cell_0'])
v_dend = np.array(sim.simData['V_dend']['cell_0'])
t = np.array(sim.simData['t'])

spkt = np.array([spkt_nrn[spkid_nrn==0]])
ifreq = sg.instFreqHanning(t,spkt,w_size=400)[0]
nsspkt = np.array([spkt_nrn[spkid_nrn==1]])
nsifreq = sg.instFreqHanning(t,nsspkt,w_size=100)[0]

fig, ax = plt.subplots(3,1)
fig.set_size_inches((7,9))

ax[0].set_ylabel("Memb. potential (mV)")
ax[0].plot(t/1e3,v_soma,label="soma")
ax[0].plot(t/1e3,v_dend,label="dend")
ax[0].legend()
ax[0].set_xlim((-2,22))

ax[1].set_ylabel("Neuron Firing rate (Hz)")
ax[1].plot(t/1e3,ifreq)
ax[1].set_xlim((-2,22))

ax[2].set_ylabel("NetStim firing rate (Hz)")
ax[2].plot(t/1e3,nsifreq)
ax[2].set_xlabel("Time (s)")
ax[2].set_xlim((-2,22))

fig.tight_layout()

figdir = "Figures"
if not os.path.isdir(figdir):
    os.mkdir(figdir)
plt.savefig(os.path.join(figdir,"MN_syn_triang.png"))
