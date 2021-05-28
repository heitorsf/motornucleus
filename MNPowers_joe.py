from neuron import h

def range_assignment(sec, var, valrange, locrange=[0.0, 1.0], verbose=False):
    """
    linearly assign values between valrange[0] and valrange[1] to each segment between locrange[0] and locrange[1]
    """
    
    delta = (valrange[1] - valrange[0]) / (locrange[1] - locrange[0])

    if verbose:
        print()
        print('sec:', sec)
        print('var:', var)
    
    for seg in sec:
        
        if verbose:
            print('  loc:', seg.x)
            print('    orig val:', getattr(seg, var))
        
        if seg.x >= locrange[0] and seg.x <= locrange[1]:
            val = valrange[0] + ((seg.x - locrange[0]) * delta)
            setattr(seg, var, val)
            
            if verbose:
                print('     new val:', val)

        elif verbose:
            print('    orig val:', getattr(seg, var))



class FRMotoneuronNaHH(object):
    
    def __init__(self):
        self.soma = h.Section(name='soma')
        self.iseg = h.Section(name='iseg')
        self.axonhillock = h.Section(name='axonhillock')
        self.dend = h.Section(name='dend')

        self.connectSections()
        self.setPassiveMN()
        self.setFRMotoneuronNaHH()
        self.setMediumTreshMN()
        

    def connectSections(self):
        
        #self.iseg.connect(self.axonhillock,0,1)
        #self.axonhillock.connect(self.soma,0,1)
        #self.soma.connect(self.dendrite,0,1)

        # Sections connect to the soma, not the soma to sections
        # I also turned axonhillock around so it starts at the soma
        # I prefer the following form for clarity
        self.dend.connect(self.soma(1), 0)  # connect the start (0) of dend to the end (1) of soma
        self.axonhillock.connect(self.soma(0), 0) # connect the start (0) of axonhillock to the start (0) of soma
        self.iseg.connect(self.axonhillock(1), 0) # connect the start (0) of iseg to the end (1) of axonhillock



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
        range_assignment(self.axonhillock, var='diam', valrange=[13.0, 3.3])
        self.axonhillock.insert('pas')
        self.axonhillock.g_pas = 1/1000.
        self.axonhillock.e_pas = -70.0
        self.axonhillock.Ra = 70.0
        self.axonhillock.cm = 1

        self.dend.nseg = 19
        self.dend.L = 6675
        self.dend.diam = 40.0
        range_assignment(self.dend, var='diam', valrange=[40.0, 1.0], locrange=[0.3, 1.0]) 
        self.dend.insert('pas')
        self.dend.g_pas = 1/11000.
        self.dend.e_pas = -70.0
        self.dend.Ra = 70.0
        self.dend.cm = 1



    def setFRMotoneuronNaHH(self):
        """Base code as in: FRMotoneuronNaHH.hoc."""
        self.soma.insert('na3rp')
        self.soma.insert('naps')
        self.soma.insert('kdrRL')
        self.soma.gMax_kdrRL = 0.1
        self.soma.insert('mAHP')
        self.soma.gkcamax_mAHP = 0.01
        self.soma.gcamax_mAHP = 1.5e-5
        self.soma.insert('gh')
        self.soma.eca = 80
        h.theta_m_L_Ca = -40
        h.tau_m_L_Ca = 60
        
        self.axonhillock.insert('na3rp')
        self.axonhillock.insert('naps')
        self.axonhillock.insert('kdrRL')
        self.axonhillock.gMax_kdrRL = 0.15
    
        self.iseg.insert('na3rp')
        self.iseg.insert('naps')
        self.iseg.insert('kdrRL')
        self.iseg.gMax_kdrRL = 0.6

        self.dend.insert('gh')
        self.dend.insert('na3rp')
        self.dend.insert('naps')
        self.dend.insert('kdrRL')
        self.dend.insert('kca2')
        self.dend.insert('L_Ca')
        self.dend.insert('mAHP')

        self.dend.depth2_kca2 = 1000
        self.dend.taur2_kca2 = 425
        self.dend.depth1_kca2 = 0.1
        self.dend.taur1_kca2 = 2
        self.dend.eca = 80

        #self.dend.gcamax_mAHP(0:0.1)=1.5e-5:1.5e-5
        range_assignment(self.dend, var='gcamax_mAHP', valrange=[1.5e-5, 1.5e-5], locrange=[0.0, 0.1])

        #self.dend.gcamax_mAHP(0.1:1)=0:0
        range_assignment(self.dend, var='gcamax_mAHP', valrange=[0, 0], locrange=[0.1, 1.0])

        #self.dend.gkcamax_mAHP(0:0.1)=0.004:0.004
        range_assignment(self.dend, var='gkcamax_mAHP', valrange=[0.004, 0.004], locrange=[0.0, 0.1])

        #self.dend.gkcamax_mAHP(0.1:1)=0:0
        range_assignment(self.dend, var='gkcamax_mAHP', valrange=[0, 0], locrange=[0.1, 1.0])

        #self.dend.gMax_kdrRL(0:1)=0.07:0
        range_assignment(self.dend, var='gMax_kdrRL', valrange=[0.07, 0.0], locrange=[0.0, 1.0])

        #self.dend.g_kca2(0:0.3)=0:0
        range_assignment(self.dend, var='g_kca2', valrange=[0, 0], locrange=[0.0, 0.3])

        #self.dend.g_kca2(0.3:0.6)=3.8e-4:3.8e-4
        range_assignment(self.dend, var='g_kca2', valrange=[3.8e-4, 3.8e-4], locrange=[0.3, 0.6])

        #self.dend.g_kca2(0.6:1)=0:0
        range_assignment(self.dend, var='g_kca2', valrange=[0, 0], locrange=[0.6, 1.0])

        #self.dend.gcabar_L_Ca(0:0.3)=0:0
        range_assignment(self.dend, var='gcabar_L_Ca', valrange=[0, 0], locrange=[0.0, 0.3])

        #self.dend.gcabar_L_Ca(0.3:0.6)=4e-4:4e-4
        range_assignment(self.dend, var='gcabar_L_Ca', valrange=[4e-4, 4e-4], locrange=[0.3, 0.6])

        #self.dend.gcabar_L_Ca(0.6:1)=0:0
        range_assignment(self.dend, var='gcabar_L_Ca', valrange=[0, 0], locrange=[0.6, 1.0])


    def setMediumTreshMN(self):
        """As in: Medium_thresh_MN.hoc."""
        ## SOMA
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

        ## INITIAL SEGMENT
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

        ## AXON HILLOCK
        self.axonhillock.nseg = 7

        #self.axonhillock.diam(0:1) = 3.84444444444444:12.2222222222222
        range_assignment(self.axonhillock, var='diam', valrange=[12.2222222222222,3.84444444444444], locrange=[0,1])

        self.axonhillock.g_pas = 0.001
        self.axonhillock.e_pas = -72
        self.axonhillock.gbar_na3rp = 0.638888888888889
        self.axonhillock.gbar_naps = 0.0127777777777778
        self.axonhillock.sh_na3rp = -3
        self.axonhillock.sh_naps = 7
        self.axonhillock.ar_na3rp = 0.4
        self.axonhillock.ar_naps = 0.4
        self.axonhillock.gMax_kdrRL = 0.4

        ## DENDRITE
        self.dend.nseg = 25
        self.dend.L = 6422.22222222222
        
        #self.dend.diam(0:0.2) = 39.4444444444444:41.4444444444444
        range_assignment(self.dend, var='diam', valrange=[39.4444444444444,41.4444444444444], locrange=[0,0.2])
        
        #self.dend.diam(0.2:1) = 41.4444444444444:0
        range_assignment(self.dend, var='diam', valrange=[41.4444444444444,0], locrange=[0.2,1])
        
        self.dend.g_pas = 7.22222222222222e-05
        self.dend.e_pas = -72
        
        #self.dend.gbar_na3rp(0:0.04) = 0.044:0.044
        range_assignment(self.dend, var='gbar_na3rp', valrange=[0.044,0.044], locrange=[0,0.04])
        
        #self.dend.gbar_na3rp(0.04:1) = 0.00075:0.00075
        range_assignment(self.dend, var='gbar_na3rp', valrange=[0.00075,0.00075], locrange=[0.04,1])
        
        #self.dend.gbar_naps(0:0.04) = 0.00044:0.00044
        range_assignment(self.dend, var='gbar_naps', valrange=[0.00044,0.00044], locrange=[0,0.04])

        #self.dend.gbar_naps(0.04:1) = 1.5e-05:1.5e-05
        range_assignment(self.dend, var='gbar_naps', valrange=[1.5e-05,1.5e-05], locrange=[0.04,1])

        self.dend.sh_na3rp = 5
        self.dend.sh_naps = 15

        #self.dend.ar_na3rp(0:0.04) = 0.4:0.4
        range_assignment(self.dend, var='ar_na3rp', valrange=[0.4,0.4], locrange=[0,0.04])

        #self.dend.ar_naps(0:0.04) = 0.4:0.4
        range_assignment(self.dend, var='ar_naps', valrange=[0.4,0.4], locrange=[0,0.04])

        #self.dend.ar_na3rp(0.04:1) = 0.4:0.4
        range_assignment(self.dend, var='ar_na3rp', valrange=[0.4,0.4], locrange=[0.04,1])

        #self.dend.ar_naps(0.04:1) = 0.4:0.4
        range_assignment(self.dend, var='ar_naps', valrange=[0.4,0.4], locrange=[0.04,1])

        #self.dend.gMax_kdrRL(0:0.04) = 0.08:0.08
        range_assignment(self.dend, var='gMax_kdrRL', valrange=[0.08,0.08], locrange=[0,0.04])

        #self.dend.gMax_kdrRL(0.04:1) = 0.00033:0.00033
        range_assignment(self.dend, var='gMax_kdrRL', valrange=[0.00033,0.00033], locrange=[0.04,1])

        #self.dend.gcabar_L_Ca(0:0.32) = 0:0
        range_assignment(self.dend, var='gcabar_L_Ca', valrange=[0,0], locrange=[0,0.32])

        #self.dend.gcabar_L_Ca(0.32:0.56) = 0.00016:0.00016
        range_assignment(self.dend, var='gcabar_L_Ca', valrange=[0.00016,0.00016], locrange=[0.32,0.56])

        #self.dend.gcabar_L_Ca(0.56:1) = 0:0
        range_assignment(self.dend, var='gcabar_L_Ca', valrange=[0,0], locrange=[0.56,1])

        #self.dend.g_kca2(0:0.32) = 0:0
        range_assignment(self.dend, var='g_kca2', valrange=[0,0], locrange=[0,0.32])

        #self.dend.g_kca2(0.32:0.56) = 4e-05:4e-05
        range_assignment(self.dend, var='g_kca2', valrange=[4e-05,4e-05], locrange=[0.32,0.56])

        #self.dend.g_kca2(0.56:1) = 0:0
        range_assignment(self.dend, var='g_kca2', valrange=[0,0], locrange=[0.56,1])

        self.dend.depth2_kca2 = 200
        self.dend.taur2_kca2 = 120

        #self.dend.gcamax_mAHP(0:0.04) = 8e-06:8e-06
        range_assignment(self.dend, var='gcamax_mAHP', valrange=[8e-06,8e-06], locrange=[0,0.04])

        #self.dend.gcamax_mAHP(0.04:1) = 0:0
        range_assignment(self.dend, var='gcamax_mAHP', valrange=[0,0], locrange=[0.04,1])

        #self.dend.gkcamax_mAHP(0:0.04) = 0.0038:0.0038
        range_assignment(self.dend, var='gkcamax_mAHP', valrange=[0.0038,0.0038], locrange=[0,0.04])

        #self.dend.gkcamax_mAHP(0.04:1) = 0:0
        range_assignment(self.dend, var='gkcamax_mAHP', valrange=[0,0], locrange=[0.04,1])

        self.dend.taur_mAHP = 56.6666666666667
        self.dend.ghbar_gh = 0.000127777777777778
        self.dend.half_gh = -75

        h.tmin_kdrRL = 0.8
        h.taumax_kdrRL = 20
        h.qinf_na3rp = 4.8
        h.thinf_na3rp = -50.5
        h.Rd_na3rp = 0.06
        h.qd_na3rp = 1.3
        h.qg_na3rp = 1.3
        h.thi1_na3rp = -35
        h.thi2_na3rp = -35
        h.vslope_naps = 5
        h.celsius = 37
        h.theta_m_L_Ca = -43

        h.theta_m_L_Ca = -43
        h.theta_m_L_Ca = -43

        h.celsius = 37

        # V0 is used for currents in the original model
        #V0 = -3.88888888888889
