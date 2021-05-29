from netpyne import sim
import numpy as np
import matplotlib.pyplot as plt
import nerlabtools as ner

#plt.ion()

from triang_cfg import cfg
from triang_netParams import netParams

simConfig = cfg
sim.create(netParams=netParams, simConfig=cfg, output=False)

delta_amp = 30.
init_amp = -3.0
peak_amp = init_amp + delta_amp
ramp_up = np.linspace(init_amp, peak_amp, int((simConfig.duration/simConfig.dt)/2))
ramp_down = np.linspace(peak_amp, init_amp, int((simConfig.duration/simConfig.dt)/2))
triang = np.concatenate((ramp_up,ramp_down))
t = sim.h.Vector(np.arange(0,simConfig.duration, simConfig.dt))
amp = sim.h.Vector(triang)
amp.play(sim.net.cells[0].stims[0]['hObj']._ref_amp, t, True)

sim.simulate()
sim.analyze()

v = np.array(sim.simData['V_soma']['cell_0'])
spkt = np.array(sim.simData['spkt'])
isi = np.diff(spkt)
ifreq = 1000./isi
plt.figure();
plt.plot(ifreq) 
