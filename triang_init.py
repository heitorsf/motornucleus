from netpyne import sim
import numpy as np
import matplotlib.pyplot as plt
import nerlabtools as ner
import os

plt.ion()

from triang_cfg import cfg
from triang_netParams import netParams

simConfig = cfg
sim.create(netParams=netParams, simConfig=cfg, output=False)

delta_amp = 30.  # for a rate of 6nA/s over 5s
init_amp = -10.0
peak_amp = init_amp + delta_amp

ramp_up = np.linspace(init_amp, peak_amp, int((5e3/simConfig.dt)))
ramp_down = np.linspace(peak_amp, init_amp, int((5e3/simConfig.dt)))
delay = np.zeros(int(cfg.stimdelay/cfg.dt))
silence = np.zeros(int(cfg.stimdelay/cfg.dt))
triang = np.concatenate((delay, ramp_up, ramp_down, silence))

t = sim.h.Vector(np.arange(0,simConfig.duration, simConfig.dt))
amp = sim.h.Vector(triang)
amp.play(sim.net.cells[0].stims[0]['hObj']._ref_amp, t, True)

sim.simulate()
sim.analyze()

figdir = "Figures"

fig, ax = plt.subplots(4,1,figsize=(6,9))

v_soma = np.array(sim.simData['V_soma']['cell_0'])
v_dend = np.array(sim.simData['V_dend']['cell_0'])
t = np.array(sim.simData['t'])
#plt.figure()
#plt.xlabel("Time (s)")
ax[0].set_ylabel("Memb. potential (mV)")
ax[0].plot(t/1e3,v_soma,label="soma")
ax[0].plot(t/1e3,v_dend,label="dend")
ax[0].legend()
ax[0].set_xlim((0,10))
#plt.tight_layout()
#if not os.path.isdir(figdir):
    #os.mkdir(figdir)
#plt.savefig(os.path.join(figdir,"MedFR_membr_potential.png"))

import sigUtils as sg
spkt = np.array(sim.simData['spkt'])
t = t[:-1]
freqest = sg.instFreqHanning(t,spkt,w_size=400)
freqest = freqest[0]
idcut = (t>spkt[0])&(t<spkt[-1])
#
isi = np.diff(spkt)
ifreq = 1000./isi
spkt = spkt.round(3)
t = t.round(3)
currspkt = [triang[i] for i in range(len(t)) if t[i] in spkt]
currspkt = np.array(currspkt)
#ax[1].plot(spkt[:-1]/1e3,ifreq,'k')

#plt.figure()
ax[1].set_ylabel("Firing rate (Hz)")
ax[1].plot(t[idcut]/1e3, freqest[idcut])
ax[1].set_xlim((0,10))

idcur = (t>100)&(t<cfg.duration-101)
ax[2].set_xlabel("Time (s)")
ax[2].set_ylabel("Current (nA)")
ax[2].plot(t[idcur]/1e3,triang[idcur])
ax[2].set_xlim((0,10))

#plt.figure()
#ax[1].set_xlabel("Injected urrent (nA)")
ax[3].set_ylabel("Firing rate (Hz)")
#ax[3].plot(currspkt[:-1],ifreq,'k')
ax[3].plot(triang[idcut], freqest[idcut])
ax[3].set_xlim((-10,30))
ax[3].set_xlabel("Injected Current (nA)")
#plt.tight_layout()
#if not os.path.isdir(figdir):
    #os.mkdir(figdir)
#plt.savefig(os.path.join(figdir,"MedFR_fI_histeresis.png"))

fig.tight_layout()
if not os.path.isdir(figdir):
    os.mkdir(figdir)
plt.savefig(os.path.join(figdir,"MN_fI_analysis.png"))
