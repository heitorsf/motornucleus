from neuron import h

class AlphaMotorNeuron(object):
    def __init__(self):
        self.soma = h.Section()
        self.dend = h.Section()
        self.soma.insert('napp')
        self.dend.insert('caL')
        self.dend.connect(self.soma,0,1)
        self.mus()

    def mus(self):
        # soma parameters
        self.soma.L = 80
        self.soma.nseg = 1
        self.soma.diam = 80
        self.soma.Ra = 70.0 #resistividade citoplasmatica
        self.soma.cm = 1.0
    
        self.soma.gnabar_napp = 0.05
        self.soma.gnapbar_napp = .00052
        self.soma.gkfbar_napp = 0.0028
        self.soma.gksbar_napp = 0.018
        self.soma.mact_napp = 13.0
        self.soma.rinact_napp = 0.025
        self.soma.ena = 120.0
        self.soma.ek = -10.0
        self.soma.el_napp = 0.0
        self.soma.vtraub_napp = 0.0
        self.soma.gl_napp = 1/1100.0
    
        # dendrite parameters
        self.dend.L = 6150.0
        self.dend.nseg = 1
        self.dend.diam = 52
        self.dend.Ra = 70.0
        self.dend.cm = 1.0
        
        self.dend.gcaLbar_caL = 0.00001056
        self.dend.ecaL = 140
        self.dend.vtraub_caL = 35
        self.dend.gama_caL = 1
        self.dend.Ltau_caL = 80
        self.dend.gl_caL = 1/12550.0
        self.dend.el_caL = 0.0
