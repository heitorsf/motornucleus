from netpyne import sim
import numpy as np
import matplotlib.pyplot as plt
import nerlabtools as ner
import sigUtils as sg

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

ifreq = sg.instFreqHanning(t,spkt,w_size=400)

fig1, ax1 = plt.subplots()
ax1.set_ylabel("Firing rate (Hz)")
ax1.set_xlabel("Time (s)")
for i,iiff in enumerate(ifreq[:-5][::2]):
    idcut = (iiff>5)
    #idcut = (t>np.sort(spkt[i])[0]) & (t<np.nanmax(spkt[i]))
    #idcut = (t>np.nanmin(spkt[i])) & (t<np.nanmax(spkt[i]))
    ax1.plot(t[idcut]/1e3,iiff[idcut])

fig2, ax2 = plt.subplots()
ax2.set_ylabel("Firing rate (Hz)")
ax2.set_xlabel("Time (s)")
for i,iiff in enumerate(ifreq):
    idcut = (t>np.sort(spkt[i])[2]) & (t<np.nanmax(spkt[i]))
    #idcut = (t>np.nanmin(spkt[i])) & (t<np.nanmax(spkt[i]))
    ax2.plot(t[idcut]/1e3,iiff[idcut])
axx2 = ax2.twinx()
axx2.plot(t/1e3,force.sum(axis=0),'k')
axx2.set_ylabel("Force (N)")
