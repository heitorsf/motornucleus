import numpy as np
from matplotlib import pyplot as plt; plt.ion()
from neuron import h
from scipy.signal import argrelmax
import SaveParams
from interpol import cellDistrib, interpol_lin, interpol_exp, interpol_point, interpol_fit,interpol_expfit,interpol_minus_exp,interpol_rand  #interpol_expfit_ALS, interpol_minus_exp_ALS, 
import time
#from motornucleus import *

'''########## Classes ##########'''

class MotorUnitPas(object):
    """Creates a new motor unit with passive dendrite.
    
    Attributes
    ----------
    soma : NEURON Section
        Has the mechanism 'napp' inserted from napp.mod.
    dend : NEURON Section
        Has the mechanism 'pas' inserted and connected to soma.
    axon : Axon (nerlabmodel.Axon)
        Has only length and conduction velocity.
    musc : MuscUnit (nerlabmodel.MuscUnit)
        Muscular unit of the motor unit."""
    def __init__(self):
        self.type = 'S'
        self.soma = h.Section()
        self.soma.insert('napp')
        #    self.soma.insert('Constant')
        
        
        self.dend = h.Section()
        self.dend.insert('pas')
        self.dend.connect(self.soma,0,1)
        
        self.axon = Axon()
        self.musc = MuscUnit()
        
        h.load_file('stdrun.hoc')
        #    h.init(1)
        #        h.finitialize(0)
        h.v_init = 0.000
        #    self.soma.ic_Constant = -(self.soma.ina+self.soma.ik+self.soma.il_napp)

#____________________________________________________________

class MotorUnitCaL(object):
    """Creates a new motor unit with active dendrite.
    
    Attributes
    ----------
    soma : NEURON Section
        The Section has the mechanism 'napp' inserted from napp.mod.
    dend : NEURON Section
        The Section has the mechanism 'caL' inserted and connected to soma.
    axon : Axon (nerlabmodel.Axon)
        Has only length and conduction velocity.
    musc : MuscUnit (nerlabmodel.MuscUnit)
        Muscular unit of the motor unit."""
    def __init__(self):
        self.type = 'S'
        self.soma = h.Section()
        self.soma.insert('napp')
        #    self.soma.insert('Constant')
        
        self.dend = h.Section()
        self.dend.insert('caL')
        #    self.dend.insert('Constant')
        self.dend.connect(self.soma,0,1)
        
        self.axon = Axon()
        self.musc = MuscUnit()
        
        h.load_file('stdrun.hoc')
        #    h.init(1)
        #        h.finitialize(0)
        h.v_init = 0.000
        #    self.soma.ic_Constant = -(self.soma.ina+self.soma.ik+self.soma.il_napp)
        #        self.dend.ic_Constant = -(self.dend.icaL_caL+self.dend.il_caL)

#____________________________________________________________

class MotorUnit(object):
    """Creates a new motor unit with passive dendrite.
    
    Attributes
    ----------
    soma : NEURON Section
        Has the mechanism 'napp' inserted from napp.mod.
    dend : NEURON Section
        Has the mechanism 'pas' inserted and connected to soma.
    axon : Axon (nerlabmodel.Axon)
        Has only length and conduction velocity.
    musc : MuscUnit (nerlabmodel.MuscUnit)
        Muscular unit of the motor unit."""
    def __init__(self):
        self.type = 'S'
        self.soma = h.Section()
        self.soma.insert('napp')

        self.dend = h.Section()
        self.dend.insert('caL')
        self.gama_caL = 0.2
        self.dend.connect(self.soma,0,1)

        self.axon = Axon()
        self.musc = MuscUnit()

#____________________________________________________________

class Axon(object):
    """Creates a new axon.
    
    The object is a simple model of neuron axon based on
    a given length and a conduction velocity.
    
    Attributes
    ----------
    len : float
        The length of the axon in meters.
    velcon : float
        Conduction velocity in m/s."""
    def __init__(self):
        self.len = 0.5 # m, length
        self.velcon = 45.5 # m/s, conduction velocity

    def delay(self):
        """Calculates the time delay caused during axon propagation.
        
        Returns
        -------
        delay : float
            Given by len/velcon."""
        delay = self.len/self.velcon
        return delay 

#____________________________________________________________

class MuscUnit(object):
    """Creates a new muscular unit.
    
    The object contains paramerts of a muscular unit twitch model.

    Attributes
    ----------
    fmax : float
        Maximum twitch force [Newtons].
    tc : float
        Contraction time (or time-to-peak force) [milliseconds].
    thr : float
        Half-decay time [milliseconds].
    ftet : float
        Maximum tetanic force of the muscular unit [Newton]."""
    def __init__(self):
        self.fmax = 1.5 # N, maximum force
        self.tc = 110. # ms, contraction time
        self.thr = 92. # ms, half-decay time
        self.ftet = 10.1 # N, related to cutoff frequency

#____________________________________________________________

'''########## Functions ##########'''

def saveCellParams(fromNetpyne,data1=0,somaSec=0,dendSec=0,comb=0):
    SaveParams.saveParams(fromNetpyne,data1,somaSec,dendSec)
    print( "\nParameters are now saved.\n")

#____________________________________________________________

def loadCellParams(cellnumber,soma,dend):
    SaveParams.loadParams(cellnumber,soma,dend,comb=0)
    print("\nParameters are now loaded.\n")

#____________________________________________________________

def fitPopParams(MotorUnits,active_dend=0,distribution='exponential',add_random=True,outputParams=False,plotParams=False,comb=False):
    """Adjusts the parameters of a population of neurons.

    Changes the parameters of a population of motor neurons
    based on the parameters of 3 motor neuron models of
    types S, FR and FF.

    Parameters
    ----------
    MotorUnits : MotorUnitPas, MotorUnitCaL or list of MotorUnit_like
        Motor unit object or list of motor unit objects that will have
        the parameters changed.
    active_dend : boolean or float
        Informs whether MotorUnits is/are MotorUnitPas or MotorUnitCaL.
    outputParams : boolean, optional
        If True, returns a dict with the parameters names and values.
    plotParams : boolean, optional
        If True, calls plotParameters.
    
    Returns
    -------
    params : dict
        A dict with final parameters and values.
    """
    print("\nChanging the parameters of motor neurons...")
    start = time.time()

    numCells = len(MotorUnits)
    numS,numFR,numFF = cellDistrib(numCells)

    if distribution=='linear':
        # Soma parameters first and last
        Diam_soma = interpol_lin(120,80,85,100.25) #100.25
        Diam_soma_first,Diam_soma_last  = Diam_soma[0],Diam_soma[-1]
        L_soma = Diam_soma
        Gnabar = interpol_lin(120,0.05,0.07,0.0775)
        Gnabar_first,Gnabar_last  = Gnabar[0],Gnabar[-1]   
        Gnapbar =  interpol_point(120,.00052,.002,.004)
        Gnapbar_first,Gnapbar_last  = 0.0006,.004
        #Gnapbar_first,Gnapbar_last  = Gnapbar[0],Gnapbar[-1]  
        #Gnapbar_first,Gnapbar_last  = 0.0006,0.0007
        Gkfbar = interpol_point(120,.0028,.0040,.00135) 
        #Gkfbar_first,Gkfbar_last  = Gkfbar[0],Gkfbar[-1]  
        Gkfbar_first,Gkfbar_last  = 0.00355,0.0028
        Gksbar = interpol_point(120,.022,.0311,0.0236)
        #Gksbar_first,Gksbar_last  = Gksbar[0],Gksbar[-1] 
        Gksbar_first,Gksbar_last  = 0.022,0.0236
        #Gksbar_first,Gksbar_last  = 0.022,0.016
        #Gksbar = interpol_point(120,.018,.037,.016) 
        #Gksbar[60:75] = np.linspace(Gksbar[60],.028,15,endpoint=False)
        #Gksbar[75:90] = np.linspace(.028,Gksbar[90],15,endpoint=False)
        #Gksbar[101:110] = np.linspace(Gksbar[101],.028,9,endpoint=False)
        #Gksbar[110:118] = np.linspace(.028,Gksbar[118],8,endpoint=False)
        Mact = interpol_lin(120,13,17,19.2)
        Mact_first,Mact_last  = Mact[0],Mact[-1]  
        Rinact = interpol_lin(120,0.025,0.058,0.062,set_firstS=0.019)
        Rinact_first,Rinact_last  = Rinact[0],Rinact[-1]  
        Gls = interpol_lin(120,1./1100,1./1000,1./800,set_firstS=1./1110,set_lastFF=1./700)
        Gls_first,Gls_last  = Gls[0],Gls[-1]  
        # Dendrite parameters first and last
        Diam_dend = interpol_lin(120,52,76.469,128.91,set_firstS=48.5,set_lastFF=90.)
        #Diam_dend_first,Diam_dend_last  = Diam_dend[0],Diam_dend[-1]  
        Diam_dend_first,Diam_dend_last  = 52,128.91
        L_dend = interpol_lin(120,6150,8634.318,17947.49)
        #L_dend_first,L_dend_last  = L_dend[0],L_dend[-1]  
        L_dend_first,L_dend_last  = 6000,17947.49  
        if active_dend>0:
            GcaLbar = interpol_lin(120,0.00001056,0.0000158,0.0000062)
            #GcaLbar_first,GcaLbar_last  = GcaLbar[0],GcaLbar[-1]  
            GcaLbar_first,GcaLbar_last  = 0.00001056, 0.0000682
            Vtraub_caL = interpol_point(120, 35, 35.6, 34)
            Vtraub_caL_first,Vtraub_caL_last  = Vtraub_caL[0],Vtraub_caL[-1]  
            LTAU_caL = interpol_point(120,80,46,47)
            LTAU_caL_first,LTAU_caL_last  = LTAU_caL[0],LTAU_caL[-1]  
            Gl_caL = interpol_lin(120,1./12550,1./8825,1./6500,set_firstS=1./13000,set_lastFF=1./6000)#
            Gl_caL_first,Gl_caL_last  = Gl_caL[0],Gl_caL[-1]  
        else:
            Gld = interpol_lin(120,1./12550,1./8825,1./6500,set_firstS=1./13000,set_lastFF=1./6000)#
            Gld_first,Gld_last  = Gld[0],Gld[-1]  
        print("\nMotor nucleus: linear distribution of parameters.")

    elif distribution=='exponential':
        print("\nMotor nucleus: exponential distribution of parameters.")
        # Soma parameters
        Diam_soma = interpol_expfit(numCells,78,113.,curv=1./14) 
        #print("Diam_soma = interpol_expfit(numCells,78,113.,curv=1./14) ")
        #Diam_soma = interpol_expfit(numCells,Diam_soma_first,Diam_soma_last,curv=1./2.5)
        L_soma = Diam_soma
        #Gnabar = interpol_expfit(numCells,Gnabar_first,0.0775,curv=1./2.5) #ok
        Gnabar = interpol_expfit(numCells,0.0325,0.0775,curv=1./2.5) #ok
        #print("Gnabar = interpol_expfit(numCells,0.0325,0.0775,curv=1./2.5) #ok")
        Gnapbar = interpol_minus_exp(numCells,0.00043,0.00067,curv=1./2.1) 
        #print("Gnapbar = interpol_minus_exp(numCells,0.00043,0.00067,curv=1./2.1) ")
        #Gnapbar = interpol_minus_exp(numCells,Gnapbar_first,Gnapbar_last,curv=1./2.2)
        Gkfbar = interpol_minus_exp(numCells,0.0028,0.0015,curv=1./25) 
        #print("Gkfbar = interpol_minus_exp(numCells,0.0028,0.0015,curv=1./25) ")
        #Gkfbar = interpol_expfit(numCells,Gkfbar_first,Gkfbar_last,curv=1./2.2)
        Gksbar = interpol_minus_exp(numCells,0.020,0.016,curv=1./6) 
        #print("Gksbar = interpol_minus_exp(numCells,0.020,0.016,curv=1./6) ")
        #Gksbar = interpol_expfit(numCells,Gksbar_first,Gksbar_last,curv=1./2.2)
        #Mact = interpol_expfit(numCells,Mact_first,20.,curv=1./3) 
        Mact = interpol_expfit(numCells,13.,20.,curv=1./3) 
        #print("Mact = interpol_expfit(numCells,13.,20.,curv=1./3) ")
        #Mact = interpol_expfit(numCells,Mact_first,Mact_last,curv=1./2.5)
        Rinact = interpol_expfit(numCells,0.018,0.062,curv=1./4)
        #print("Rinact = interpol_expfit(numCells,0.018,0.062,curv=1./4)")
        #Rinact = interpol_expfit(numCells,Rinact_first,Rinact_last,curv=1./2.5)
        #Gls = interpol_expfit(numCells,Gls_first,1./650.,curv=1./2.5) #ok
        Gls = interpol_expfit(numCells,1./1050.,1./650.,curv=1./2.5) #ok
        #print("Gls = interpol_expfit(numCells,1./1050.,1./650.,curv=1./2.5) #ok")
        #Gls = interpol_expfit(numCells,1./1050.,1./650.,curv=1./15.) # gls_gld_diamden_curv15
        
        # Dendrite parameters
        #Diam_dend = interpol_expfit(numCells,42.,92.,curv=1./5) 
        Diam_dend = interpol_expfit(numCells,48.,90.,curv=1./5)  # ok_01
        #print("Diam_dend = interpol_expfit(numCells,48.,90.,curv=1./5)  # ok_01")
        #Diam_dend = interpol_expfit(numCells,48.,90.,curv=1./15)  # gls_gld_diamden_curv15
        #Diam_dend = interpol_expfit(numCells,Diam_dend_first,Diam_dend_last,curv=1./2.5)
        L_dend = interpol_expfit(numCells,5500,10600,curv=1./12) 
        #print("L_dend = interpol_expfit(numCells,5500,10600,curv=1./12) ")
        #L_dend = interpol_expfit(numCells,L_dend_first,L_dend_last,curv=1./2.5)
        if active_dend>0:
            GcaLbar = interpol_minus_exp(numCells,0.0000125,0.0000062)#ok
            #print("GcaLbar = interpol_minus_exp(numCells,0.0000125,0.0000062)#ok")
            Vtraub_caL = interpol_minus_exp(numCells,35,34,curv=1./30) 
            #print("Vtraub_caL = interpol_minus_exp(numCells,35,34,curv=1./30) ")
            #Vtraub_caL = interpol_minus_exp(numCells,Vtraub_caL_first,Vtraub_caL_last,curv=1./2.2)
            LTAU_caL = interpol_minus_exp(numCells,90,47) 
            #print("LTAU_caL = interpol_minus_exp(numCells,90,47) ")
            #LTAU_caL = interpol_minus_exp(numCells,LTAU_caL_first,LTAU_caL_last)
            #Gl_caL = interpol_expfit(numCells,Gl_caL_first,1/6050.,curv=1./2.5)#ok
            Gl_caL = interpol_expfit(numCells,1./13000.,1/6050.,curv=1./2.5) # ok_01
            #print("Gl_caL = interpol_expfit(numCells,1./13000.,1/6050.,curv=1./2.5) # ok_01")
            #Gl_caL = interpol_expfit(numCells,1./13000.,1/6050.,curv=1./15.)  # gls_gld_diamden_curv15
        else:
            Gld = interpol_lin(numCells,1./12550,1./8825,1./6500,set_firstS=1./13000,set_lastFF=1./6000)#
            Gld_first,Gld_last  = Gld[0],Gld[-1]  
            Gld = interpol_expfit(numCells,Gld_first,Gld_last,curv=1./2.5)
        print("\nMotor nucleus: exponential distribution of parameters.")
    else:
        raise ValueError("unknown distribution type: %c. Must be 'linear' or 'exponential'." % (distribution))

    # Axon parameters
    axon_len = 0.6  # meters
    Axon_velcon = interpol_lin(numCells,45.5,49.5,51.5)  # m/s

    # Add randomness to parameters
    if add_random:
        Diam_soma = interpol_rand(Diam_soma) 
        L_soma = interpol_rand(L_soma) 
        Gnabar = interpol_rand(Gnabar) 
        Gnapbar = interpol_rand(Gnapbar) 
        Gkfbar = interpol_rand(Gkfbar) 
        Gksbar = interpol_rand(Gksbar) 
        Mact = interpol_rand(Mact) 
        Rinact = interpol_rand(Rinact) 
        Gls = interpol_rand(Gls) 
        Diam_dend = interpol_rand(Diam_dend) 
        L_dend = interpol_rand(L_dend) 
        if active_dend>0:
            GcaLbar = interpol_rand(GcaLbar) 
            Vtraub_caL = interpol_rand(Vtraub_caL) 
            LTAU_caL = interpol_rand(LTAU_caL) 
            Gl_caL = interpol_rand(Gl_caL) 
        else:
            Gld = interpol_rand(Gld) 
        Axon_velcon = interpol_rand(Axon_velcon)
        print("\n  Added some randomness to parameters distribution.")


    # Set the mu.type label for each motor unit
    for i,mu in enumerate(MotorUnits):
        if i in range(0,numS):
            mu.type = 'S'
        elif i in range(numS,numS+numFR):
            mu.type = 'FR'
        elif i in range(numS+numFR,numS+numFR+numFF):
            mu.type = 'FF'

        # Fixed parameters
        mu.soma.ena = 120.0
        mu.soma.ek = -10.0
        mu.soma.el_napp = 0.0
        mu.soma.vtraub_napp = 0.0
        mu.soma.nseg = 1
        mu.soma.Ra = 70.0
        mu.soma.cm = 1.0

        # Soma parameters
        mu.soma.L = Diam_soma[i]
        mu.soma.diam = Diam_soma[i]
        mu.soma.gl_napp = Gls[i]
        mu.soma.gnabar_napp = Gnabar[i]
        mu.soma.gnapbar_napp = Gnapbar[i]
        mu.soma.gkfbar_napp = Gkfbar[i]
        mu.soma.gksbar_napp = Gksbar[i]
        mu.soma.mact_napp = Mact[i]
        mu.soma.rinact_napp = Rinact[i]

        # Dendrite parameters
        mu.dend.nseg = 1
        mu.dend.Ra = 70.0
        mu.dend.cm = 1.0
        mu.dend.L = L_dend[i]
        mu.dend.diam = Diam_dend[i]
        if active_dend>0:
            mu.dend.ecaL = 140
            mu.dend.gama_caL = active_dend
            mu.dend.gcaLbar_caL = GcaLbar[i]
            mu.dend.vtraub_caL = Vtraub_caL[i]
            mu.dend.Ltau_caL = LTAU_caL[i]
            mu.dend.gl_caL = Gl_caL[i]
            mu.dend.el_caL = 0.
        else:
            mu.dend.e_pas = 0.
            mu.dend.g_pas = Gld[i]

        # Axon parameters
        mu.axon.len = axon_len
        mu.axon.velcon = Axon_velcon[i]
    
    if outputParams or plotParams:
        if active_dend>0:
            params = {'diam_soma':Diam_soma, 'L_soma':L_soma, 'gnabar':Gnabar,
                      'gnapbar':Gnapbar, 'gkfbar':Gkfbar, 'gksbar':Gksbar,
                      'mact':Mact, 'rinact':Rinact, 'gl_soma':Gls, 'L_dend': L_dend,
                      'diam_dend': Diam_dend, 'gcaLbar': GcaLbar,'vtraub_caL': Vtraub_caL,
                      'Ltau_caL': LTAU_caL,'gl_caL': Gl_caL}
        else:
            params = {'diam_soma':Diam_soma, 'L_soma':L_soma, 'gnabar':Gnabar,
                      'gnapbar':Gnapbar, 'gkfbar':Gkfbar, 'gksbar':Gksbar,
                      'mact':Mact, 'rinact':Rinact, 'gl_soma':Gls, 'L_dend': L_dend,
                      'diam_dend': Diam_dend,'gldL': Gld}
        if plotParams:
            plotParameters(params,comb=comb)
        if outputParams:
            return params
        else:
            return 0

    end = time.time()
    elapsed_time = end-start
    print("Done; fitPopParams time: %.2f s" %elapsed_time)

#____________________________________________________________

def plotParameters(params,comb=0):
    """Plots the values of parameters along a neuron pool.
    
    Tool to visualize how the parameters change along the pool.
    
    Parameter
    ---------
    params : dict
        Each key is a parameter of the neuron model."""
    from math import ceil
    '''
    for x in params.keys():
        plt.figure()
        plt.title(x)
        plt.plot(params[x],'g-')
        #plt.plot([0,59,89,119],params[x][[0,59,89,119]],'rx')
        #plt.plot([30,75,105],params[x][[30,75,105]],'g.')
        plt.plot([0,100,117,119],params[x][[0,100,117,119]],'rx')
        plt.plot([50,109,118,119],params[x][[50,109,118,119]],'g.')
    '''

    fig = plt.figure(figsize=(15,8))
    plt.suptitle("")
    n = len(params.keys())
    loc = 0
    for i,x in enumerate(params.keys()):
        loc +=1
        plt.subplot(3,ceil(n/3.),loc)
        plt.xlabel("Motor Neuron")
        plt.ylabel(x)
        plt.plot(params[x],'-',color='0.7')
        plt.plot(params[x],'.')
    plt.tight_layout(rect=(0,0,1,0.98))
    if comb:
        plt.savefig('params'+comb+'.png')

#____________________________________________________________

def getSpikes(t, v, axDelay=False, mu=[], output=True, plotRaster=False, newFigure=True):
    """Detects spikes from time courses of membrane potentials.

    Parameters
    ----------
    t : 1-D array_like
        Time array. The shape must be (x), (x,) or (x,1)
    v : array_like
        Membrane potential array. Expected shape: (numberOfCells, timeVectorLength)
    axDelay : boolean, optional
        If True, calls axonDelay(spkt,mu), including the delay caused by axon
        conduction on spikes instants.
    mu : MotorUnit_like list, optional
        Needed when 'axDelay' is True.
    output : boolean, optional
        If False, supress the returning of spike trains and voltages
    plotRaster : boolean, optional
        If True, generates a raster plot of spike trains.
    newFigure : boolean, optional
        If True, the raster plot is generated in a new matplotlib.pyploy.figure().

    Returns
    -------
    spkt : ndarray
        Array of spikes instants.
        The shape is: (number of neurons, max number of spikes).
        Elements with no spikes are numpy.nan.
    spkv : ndarray
        Array of peaks membrane potentials.
        The shape is: (number of neurons, max number of spikes).
        Elements with no spikes are numpy.nan."""
    start = time.time()
    print("  Detecting spikes instants...")
    if not axDelay and len(mu)>0:
        print("\nWarning: To get spikes with axons delays please use axDelay=True and pass a munit list as argument (mu).\n")
    if not isinstance(t, np.ndarray):
        t = np.array(t)
    if not isinstance(v, np.ndarray):
        v = np.array(v)
    if len(v.shape)<2:
        v.shape = (1,v.shape[0])
    dvdt = np.diff(v, axis=1)
    dt = t[1]
    
    ''' Detect Spikes '''
    numCells = v.shape[0]
    spkt_list = []
    spkv_list = []
    for cell_id in range(numCells):
        maxima_ids = argrelmax(v[cell_id,:])
        spkt_list_cell_ids = [i for i in maxima_ids[0] if (v[cell_id,i]>=50 and v[cell_id,i]<=100)]
        spkt_cell_t = t[spkt_list_cell_ids]
        spkt_cell_v = v[cell_id,spkt_list_cell_ids]

        spkt_list.append(spkt_cell_t)
        spkv_list.append(spkt_cell_v)
    
    ''' Create spiketrain times (spkt) and volts (spkv) matrices '''
    # Set matrices size according to the neuron that fired the biggest number of spikes
    numPAs = np.array([])
    for i in range(numCells):
        numPAs = np.append(numPAs, len(spkt_list[i]))
    maxPAs = int(numPAs.max())
    
    # Create and fill the matrices
    spkt = np.zeros((numCells, maxPAs))*np.nan
    spkv = np.zeros(spkt.shape)*np.nan
    for i in range(numCells):
        for j in range(len(spkt_list[i])):
            spkt[i,j] = spkt_list[i][j]
            spkv[i,j] = v[i,:][t==spkt_list[i][j]]

    if axDelay:
        spkt = axonDelay(spkt,mu)
    elapsed_time = time.time() - start
    print ("  Done; getSpikes time: %.2f s" %elapsed_time)

    ''' Plot Raster '''
    if plotRaster:
        if newFigure:
            plt.figure()
        plotSpikes(spkt)
    if output:
        return spkt, spkv

#____________________________________________________________

def plotSpikes(spkt):
    """Plot spikes instants."""
    start_plot = time.time()
#    if len(spkt[:,:]) > 0:
    try:
        print("\n  Plotting Raster...")
        for i in range(len(spkt[:,0])):
            plt.plot(spkt[i,:], np.ones(len(spkt[i,:]))*i, 'b|', markeredgewidth=1.5)
        plt.title("Spike Trains")
        plt.xlabel("Time [ms]")
        plt.ylabel("# Motor neuron")
        plt.show()
        elapsed_time = time.time() - start_plot
        print("  Done; plotRaster time: %.2f s" %elapsed_time)
    except IndexError:
        print("\n*****\n\nWarning: 'spkt' has no length, aparently no spikes were fired.\n\n*****\n")

#____________________________________________________________

def spktFromList(spkt_list):
    """Returns a rectangular np.array."""
    numCells = len(spkt_list)
    # Set matrices size according to the neuron that fired more spikes
    numAPs = np.array([])
    for i in range(numCells):
        numAPs = np.append(numAPs, len(spkt_list[i]))
    maxPAs = int(numAPs.max())
    
    # Create and fill the matrices
    spkt = np.zeros((numCells, maxPAs))*np.nan
    for i in range(numCells):
        for j in range(len(spkt_list[i])):
            spkt[i,j] = spkt_list[i][j]
    return spkt

#____________________________________________________________

def axonDelay(spkt_soma,mu):
    """Add axon conduction delay to spike instants."""
    if spkt_soma.shape[0] != len(mu):
        raise ValueError("Number of spike trains differs from number of motor units.")
    spkt_endplate = np.zeros(spkt_soma.shape)
    for i in range(spkt_soma.shape[0]):
        spkt_endplate[i] = spkt_soma[i] + mu[i].axon.delay() 
    return spkt_endplate

#____________________________________________________________

def sig(f,c):
    """Saturate data using a sigmoidal function.

    Parameters
    ----------
    f : array_like
        Data to saturate.
    c : float
        Parameter to adjust the shape of the sigmoid.

    Returns
    -------
    out : array
        Saturated data."""
    b = 1.2#1.385#1.2
    expcf = np.exp(-c*(f-b))
    sat = (1-expcf) / (1+expcf)
    out = (sat - sat[0]) / (1-sat[0])
    return out

def calculateTetTwt(C):
    """Calculate tetanus/twitch ratio.
    
    Calculate the tetanus/twitch ratio for every sigmoid with
    parameter c in vector C.
    
    Parameters
    ----------
    C : 1-D array, float
        Sequence of values to be used as parameter of a sigmoid function.
    
    Returns
    -------
    ttnp : numpy array
        Value of a sigmoid curve at the index where a straight line of the same
        size is at 1, meaning the tetanus/twitch ratio. It it:
        fsat: sigmoid
        fmu: straight line (from 0 to 10)
            ttnp = 1/fsat[fmu==1]"""
    tt = []
    fmu = np.arange(0,10,0.01)
    for c in C:
        fsat = sig(fmu,c)
        tt.append(1./fsat[fmu==1])
    ttnp = np.array(tt)
    return ttnp

def muscularForce(spkt, t, plotForce=False, newFigure=True, fitStyle='exponential'):
    """Generate muscle force signal from spike trains.

    Use digital filter to generate summations of twitches in response
    to spike trains.
    
    Parameters
    ----------
    spkt : array
        Spike train(s). If not 1-D, first dimension is motor unit number.
    t : array
        Time array.
    plotForce : boolean, optional
        Choose whether to plot force signals or not.
    newFigure : boolean, optional
        If True, creates a new matplotlib.pyploy.figure() when plotForce is True.
    fitStyle : string, optional
        Decides how the parameters will vary. Accepts "exponential" (default)
        or "linear".
    
    Returns
    -------
    forces : array
        An array with shape (spkt.shape[0], t.size) containing force signal
        for each spike train. 
        """

    print("\n  Generating muscular force data...")
    print("    Setting muscular force parameters.")
    start = time.time()

    from scipy.signal import lfilter

    # Here we assume that every cell generated a spike train:
    numCells = spkt.shape[0] 

    dt = t[1]
    forces = np.zeros(t.size)
    
    if fitStyle=="linear":
        Fmaxmu = interpol_lin(numCells,1.7,1.9,2.15)  # N
        Tc = interpol_lin(numCells,110.,73.5,55.)  # ms
        Ftet = interpol_lin(numCells,10.1,15.2,19.3)  # N
    elif fitStyle=="exponential": #(enoka, fuglevand,2001)
        fmax = 260.0*1e-3  # N # 130 # heitor parametrizou com 260 pra dissertacao 220
        fmin = 1.*1e-3  # N
        Fmaxmu = interpol_exp(numCells,fmin,fmax,ascending=True)
        tcmin = 30.  # ms
        tcmax = 100.  # ms
        Tc = interpol_exp(numCells,tcmin,tcmax,ascending=False)
    else:
        raise ValueError("fitStyle not understood, must be \"linear\" or \"exponential\"")

    print("    Calculating auxiliary arrays.")
    A = np.array([])
    B = np.array([])
    for i in range(numCells):
        A = np.concatenate((A, np.array([1, -2*np.exp(-(dt/Tc[i])), np.exp(-2*(dt/Tc[i]))])))
        B = np.concatenate((B, np.array([0, 1*((dt**2)/Tc[i])*np.exp(1-dt/Tc[i])])))
    A = A.reshape((numCells,3))
    B = B.reshape((numCells,2))

    print("    Computing force.")
    C = interpol_exp(numCells,xmin=1.68,xmax=2.25,ascending=False)  # Fsat from 15 to 65 Hz
    TetTwt = calculateTetTwt(C)
    for cell_index in range(spkt.shape[0]):  # For every cell (or for every spike train):
        Fmu = np.zeros(t.size)
        spkt_cell = spkt[cell_index][spkt[cell_index]>0]
        spikes = np.zeros(t.size)
        for instant in spkt_cell:  # For every spike of this cell:
            spikes[int(instant/dt)] = 1./dt
        F = lfilter(B[cell_index],A[cell_index],spikes)
        Fsat = sig(F,C[cell_index]) * TetTwt[cell_index] * Fmaxmu[cell_index]
        forces = np.vstack((forces, Fsat))

    if plotForce:
        print("    Plotting...")
        if newFigure:
            plt.figure()
        plotForces(t,forces)

    elapsed_time = time.time() - start
    print("  Done; muscularForce time: %.2f s\n" %elapsed_time)
    return forces[1:,] #, TetTwt, C,Fmaxmu

#____________________________________________________________

def plotForces(t,forces):
    """Plot force signal."""
    plt.title("FDI Muscular Force")
    plt.xlabel("Time [ms]")
    plt.ylabel("Muscular Force [N]")
    plt.plot(t,forces.sum(axis=0))
    plt.show()

#____________________________________________________________

def instFreq(spkt):
    """Returns instantaneous frequency and midtimes from spike trains."""
    ifreq = 1000./np.diff(spkt) # 1/s (Hz)
    midtimes = spkt[:,1:] - np.diff(spkt)/2. # put the point in the middle of the time samples pairs
    return ifreq,midtimes

#____________________________________________________________
