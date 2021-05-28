from neuron import h
import numpy as np
import matplotlib.pyplot as plt
from MNPowers_joe import FRMotoneuronNaHH
from netpyne import specs,sim

cell = FRMotoneuronNaHH()

ic = h.IClamp(cell.soma(0.5))
ic.delay = 50.
ic.amp = 30.
ic.dur = 100.

v = h.Vector()
v.record(cell.soma(0.5)._ref_v)
t = h.Vector()
t.record(h._ref_t)

h.load_file('stdrun.hoc')
h.finitialize(-65)
h.continuerun(300)

#plt.ion()
plt.plot(t,v)
plt.show()
