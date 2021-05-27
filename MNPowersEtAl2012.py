from neuron import h

class FRMotoneuronNaHH(object):
    def __init__(self):
        self.soma = h.Section()
        self.iseg = h.Section()
        self.axonhillock = h.Section()
        self.dend = h.Section()

        self.connectSections()

        self.setPassiveMN()

        self.setFRMotoneuronNaHH()

        self.setMediumTreshMN()
        


    def connectSections(self):
        self.iseg.connect(self.axonhillock,0,1)
        self.axonhillock.connect(self.soma,0,1)
        self.soma.connect(self.dendrite,0,1)

    def setPassiveMN(self):
        """Set passive MN as in: FRcablepas.hoc."""
        self.soma.nseg = 1
        self.soma.L = 48.8
        self.soma.diam = 48.8
        self.soma.insert('pas')
        self.soma.g_pas = 1./225.
        self.soma.e_pas = -70.0
        self.soma.Ra = 70.0
        self.soma.cm = 1

        self.iseg.nseg = 5
        self.iseg.L = 30
        self.iseg.diam = 3.3
        self.iseg.insert('pas')
        self.iseg.g_pas = 1/1000.
        self.iseg.e_pas = -70.0
        self.iseg.Ra = 70.0
        self.iseg.cm = 1

        self.axonhillock.nseg = 11
        self.axonhillock.L = 15
        self.axonhillock.diam(0:1) = 3.3:13
        self.axonhillock.insert('pas')
        self.axonhillock.g_pas = 1/1000.
        self.axonhillock.e_pas = -70.0
        self.axonhillock.Ra = 70.0
        self.axonhillock.cm = 1

        self.dendrite.nseg = 11
        self.dendrite.L = 15
        self.dendrite.diam(0.3:1) = 40:1
        self.dendrite.insert('pas')
        self.dendrite.g_pas = 1/1000.
        self.dendrite.e_pas = -70.0
        self.dendrite.Ra = 70.0
        self.dendrite.cm = 1

    def setFRMotoneuronNaHH(self):
        """Base code as in: FRMotoneuronNaHH.hoc."""
        self.soma.insert('na3rp')
        self.soma.insert('naps')
        self.soma.insert('kdrRL')
        self.soma.insert('mAHP')
        self.soma.insert('gh')
        self.soma.gMax_kdrRL=0.1
        self.soma.gkcamax_mAHP=0.01
        self.soma.gcamax_mAHP=1.5e-5
        self.soma.eca=80
        self.soma.theta_m_L_Ca=-40
        self.soma.tau_m_L_Ca=60
        
        self.axonhillock.insert('na3rp')
        self.axonhillock.insert('naps')
        self.axonhillock.insert('kdrRL')
        self.axonhillock.gMax_kdrRL=0.15
    
        self.iseg.insert('na3rp')
        self.iseg.insert('naps')
        self.iseg.insert('kdrRL')
        self.iseg.gMax_kdrRL=0.6

        self.dendrite.insert('gh')
        self.dendrite.insert('na3rp')
        self.dendrite.insert('naps')
        self.dendrite.insert('kdrRL')
        self.dendrite.insert('kca2')
        self.dendrite.insert('L_Ca')
        self.dendrite.insert('mAHP')
        self.dendrite.gcamax_mAHP(0:0.1)=1.5e-5:1.5e-5
        self.dendrite.gcamax_mAHP(0.1:1)=0:0
        self.dendrite.gkcamax_mAHP(0:0.1)=0.004:0.004
        self.dendrite.gkcamax_mAHP(0.1:1)=0:0
        self.dendrite.gMax_kdrRL(0:1)=0.07:0
        self.dendrite.g_kca2(0:0.3)=0:0
        self.dendrite.g_kca2(0.3:0.6)=3.8e-4:3.8e-4
        self.dendrite.g_kca2(0.6:1)=0:0
        self.dendrite.gcabar_L_Ca (0:0.3)=0:0
        self.dendrite.gcabar_L_Ca(0.3:0.6)=4e-4:4e-4
        self.dendrite.gcabar_L_Ca (0.6:1)=0:0
        self.dendrite.depth2_kca2=1000
        self.dendrite.taur2_kca2=425
        self.dendrite.depth1_kca2=0.1
        self.dendrite.taur1_kca2=20
        self.dendrite.eca=80

    def setMediumTreshMN(self):
        """As in: Medium_thresh_MN.hoc."""
        self.soma.diam = 53.8888888888889
        self.soma.L = 53.8888888888889
        self.soma.g_pas = 0.00291666666666667
        self.soma.e_pas = -72
        self.soma.gbar_na3rp = 0.044
        self.soma.gbar_naps = 0.00044
        self.soma.sh_na3rp = 5
        self.soma.sh_naps = 15
        self.soma.ar_na3rp = 0.4
        self.soma.ar_naps = 0.4
        self.soma.gMax_kdrRL = 0.07
        self.soma.gcamax_mAHP = 8e-06
        self.soma.gkcamax_mAHP = 0.0076
        self.soma.taur_mAHP = 56.6666666666667
        self.soma.ghbar_gh = 0.000127777777777778
        self.soma.half_gh = -75

        self.iseg.nseg = 9
        self.iseg.diam = 3.84444444444444
        self.iseg.g_pas = 0.001
        self.iseg.e_pas = -72
        self.iseg.gbar_na3rp = 0.638888888888889
        self.iseg.gbar_naps = 0.0127777777777778
        self.iseg.sh_na3rp = -3
        self.iseg.sh_naps = 7
        self.iseg.ar_na3rp = 0.4
        self.iseg.ar_naps = 0.4
        self.iseg.gMax_kdrRL = 0.4

        self.axonhillock.nseg = 7
        self.axonhillock.diam(0:1) = 3.84444444444444:12.2222222222222
        self.axonhillock.g_pas = 0.001
        self.axonhillock.e_pas = -72
        self.axonhillock.gbar_na3rp = 0.638888888888889
        self.axonhillock.gbar_naps = 0.0127777777777778
        self.axonhillock.sh_na3rp = -3
        self.axonhillock.sh_naps = 7
        self.axonhillock.ar_na3rp = 0.4
        self.axonhillock.ar_naps = 0.4
        self.axonhillock.gMax_kdrRL = 0.4

        self.dendrite.nseg = 25
        self.dendrite.L = 6422.22222222222
        self.dendrite.diam(0:0.2) = 39.4444444444444:41.4444444444444
        self.dendrite.diam(0.2:1) = 41.4444444444444:0
        self.dendrite.g_pas = 7.22222222222222e-05
        self.dendrite.e_pas = -72
        self.dendrite.gbar_na3rp(0:0.04) = 0.044:0.044
        self.dendrite.gbar_na3rp(0.04:1) = 0.00075:0.00075
        self.dendrite.gbar_naps(0:0.04) = 0.00044:0.00044
        self.dendrite.gbar_naps(0.04:1) = 1.5e-05:1.5e-05
        self.dendrite.sh_na3rp = 5
        self.dendrite.sh_naps = 15
        self.dendrite.ar_na3rp(0:0.04) = 0.4:0.4
        self.dendrite.ar_naps(0:0.04) = 0.4:0.4
        self.dendrite.ar_na3rp(0.04:1) = 0.4:0.4
        self.dendrite.ar_naps(0.04:1) = 0.4:0.4
        self.dendrite.gMax_kdrRL(0:0.04) = 0.08:0.08
        self.dendrite.gMax_kdrRL(0.04:1) = 0.00033:0.00033
        self.dendrite.gcabar_L_Ca(0:0.32) = 0:0
        self.dendrite.gcabar_L_Ca(0.32:0.56) = 0.00016:0.00016
        self.dendrite.gcabar_L_Ca(0.56:1) = 0:0
        self.dendrite.g_kca2(0:0.32) = 0:0
        self.dendrite.g_kca2(0.32:0.56) = 4e-05:4e-05
        self.dendrite.g_kca2(0.56:1) = 0:0
        self.dendrite.depth2_kca2 = 200
        self.dendrite.taur2_kca2 = 120
        self.dendrite.gcamax_mAHP(0:0.04) = 8e-06:8e-06
        self.dendrite.gcamax_mAHP(0.04:1) = 0:0
        self.dendrite.gkcamax_mAHP(0:0.04) = 0.0038:0.0038
        self.dendrite.gkcamax_mAHP(0.04:1) = 0:0
        self.dendrite.taur_mAHP = 56.6666666666667
        self.dendrite.ghbar_gh = 0.000127777777777778
        self.dendrite.half_gh = -75
        self.tmin_kdrRL = 0.8
        self.taumax_kdrRL = 20
        self.qinf_na3rp = 4.8
        self.thinf_na3rp = -50.5
        self.Rd_na3rp = 0.06
        self.qd_na3rp = 1.3
        self.qg_na3rp = 1.3
        self.thi1_na3rp = -35
        self.thi2_na3rp = -35
        self.vslope_naps = 5
        self.celsius = 37
        self.theta_m_L_Ca = -43
        self.V0 = -3.88888888888889
