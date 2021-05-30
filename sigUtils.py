import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import correlate,detrend

def hanning(t,spikes,w_size=400.):
    print("\nWARNING: fuction hanning() depracated: consider using sigUtils.instFreqHanning(). Is the same function but with a better name.\n")
    return instFreqHanning(t,spikes,w_size=400.)

def instFreqHanning(t,spikes,w_size=400.,plotOutput=False):
    """ Estimates the instantaneus frequency of spike train.
    
    Parameters:
    -----------
    t : np.array
    spikes : array-like
    w_size (optional) : float"""

    # Create zeros vector with 1/dt at impulse instants
    t = np.round(t,3)
    dt = t[1]
    spikes = spikes-(spikes%dt)
    spikes = np.round(spikes,3)
    if len(spikes.shape)==1:
        spikes = np.array([spikes])        
    impulses = np.zeros((spikes.shape[0],len(t)))
    for s,spkt in enumerate(spikes):
        for spk in spkt:
            impulses[s][t==spk] = 1./dt
    window = np.hanning(w_size/dt)
    window = window/np.trapz(window)
    
    W = len(window)
    ifreq_fft = []
    ifreq_list = []
    if plotOutput:
        plt.figure()
    for n in range(len(spikes)):
        #I = len(impulses[n])
        #C = I+W-1
        #ifreq_fft.append(np.fft.ifft(np.fft.fft(impulses[n], C)*np.fft.fft(window, C)))
        # Filtering twice (same effect as scipy.signal.filtfilt)
        ifreqMU = np.convolve(window,impulses[n],mode='same')
        ifreqMU = np.convolve(window,ifreqMU,mode='same')
        ifreqMU = ifreqMU*1000.  # convert to seconds
        #ifreq_list.append(np.convolve(window,impulses[n],mode='same')*1000)
        ifreq_list.append(ifreqMU)
        if plotOutput:
            plt.title(u'Discharge frequency [Hz]')
            plt.xlabel('t [ms]')
            plt.ylabel(r'$\hat{f} (t)$ [Hz]')
            plt.plot(t,ifreq_list[n])
    #plt.savefig('../images/inst_freqs.png')
    ifreq = np.array(ifreq_list) #/10000.
    return ifreq

def cstHanning(t,spkt,w_size=400,trim=0,plot=False):
    print("Calculating sCST...")
    #estac_idx = (t>=trimStart) & (t<t[-1]-trimEnd)
    #t_est = t[estac_idx]
    #spkt_shape = spkt.shape
    #spkflat = [spk if (spk>trimStart)&(spk<t[-1]-trimEnd) else np.nan for spk in spkt.flatten()]
    #spkt = np.array(spkflat).reshape(spkt_shape)
    import pdb
    t = np.round(t,3)
    dt = t[1]
    spkt = spkt-(spkt%dt)
    try:
        spkt = np.round(spkt,3)
    except:
        spkt = np.array([np.round(s) for s in spkt])
    # Calculate cst:
    impulses = np.zeros((spkt.shape[0],len(t)))
    for i in range(len(impulses)):
        for s in spkt[i]:
            impulses[i][np.argwhere(t==s)] = 1./dt
    cst = np.mean(impulses,axis=0)
    # Create zeros vector with 1/dt at impulse instants
    #impulses = np.zeros(len(t))
    #for s in range(len(cst)):
        #impulses[t==cst[s]] += 1./dt
    window = np.hanning(w_size/dt)
    window = window/np.trapz(window)
    W = len(window)
    ifreq_fft = []
    ifreq_list = []
    I = len(impulses)
    C = I+W-1
    #ifreq = np.convolve(window,cst,mode='same')*1000. #/mus
    ifreq = np.convolve(window,cst,mode='same')
    ifreq = np.convolve(window,ifreq,mode='same')
    ifreq = ifreq*1000.  # convert to 1/seconds
    trimid = (t>=trim) & (t<=t[-1]-trim)
    if plot:
        plt.figure()
        plt.title(u'Discharge frequency [Hz]')
        plt.xlabel('t [ms]')
        plt.ylabel(r'$\hat{f} (t)$ [Hz]')
        plt.plot(t,ifreq)
    return ifreq

def crossCorr_freq(t,ifreq,N=2):
    estac_idx2 = (t>=800)&(t<1200)
    t_est = t[estac_idx2]
    ifreq_est = ifreq[:,estac_idx2]
    ifreq_zeromean = (ifreq_est.transpose()-ifreq_est.mean(axis=1)).transpose()
    ifreq_detrend = np.array([detrend(f) for f in ifreq_zeromean])
    lags = t_est-t_est.min()-(t_est.max()-t_est.min())/2.

    freq_xc = []
    freq_id = []
    plt.figure()
    plt.title(u'Cross correlation: pairs of inst. freq')
    plt.xlabel('Lag [ms]')
    plt.ylabel(r'$R_{f_i f_j}$',fontsize=20)
    for i in range(N-1):
        for j in range(i+1,N):
            freq_xc.append(correlate(ifreq_detrend[i],ifreq_detrend[j],mode='same'))
            normalizing_term = len(ifreq_detrend[i]) * ifreq_detrend[i].std() * ifreq_detrend[j].std()
            freq_xc[-1] = freq_xc[-1]/normalizing_term
            freq_id.append((i,j))
            print(i,j)
            plt.plot(lags,freq_xc[-1],alpha=0.6)
    idx_peak = (lags>=-50)&(lags<=50)
    rho_list = [np.max(xc[idx_peak] for xc in freq_xc)]
    freqxc = np.array(freq_xc)
    freqxc_mean = freqxc.sum(axis=0)/N
    rho = np.array(rho_list)
    
    plt.plot(t_est-t_est.min()-(t_est.max()-t_est.min())/2.,freqxc_mean,'k',linewidth=2)
    plt.tight_layout()
    plt.grid()
    
    return rho,freq_id

def crossCorr(t,sig1,sig2):
    estac_idx2 = (t>=800)&(t<9500)
    t_est = t[estac_idx2]
    sig1_est = sig1[estac_idx2]
    sig1_zeromean = sig1_est - sig1_est.mean()
    sig1_detrend = detrend(sig1_zeromean)
    sig2_est = sig2[estac_idx2]
    sig2_zeromean = sig2_est - sig2_est.mean()
    sig2_detrend = detrend(sig2_zeromean)
    xcorr = correlate(sig1_detrend,sig2_detrend,mode='same')
    normalizing_term = len(sig2_detrend) * sig1.std() * sig2.std()
    xcorr = xcorr/normalizing_term
    lags = t_est-t_est.min()-(t_est.max()-t_est.min())/2.
    plt.figure()
    plt.title(u'Cross correlation: force and sCST')
    plt.xlabel('Lag [ms]')
    plt.ylabel(r'$R_{Force,Freq}}$')
    plt.plot(lags,xcorr)
    plt.grid()
    return xcorr,lags

def corrCoef(ifreq_matrix):
    ""

def SNR(sig1,sig2):
    pwr1 = np.power(sig1,2)
    pwr2 = np.power(sig2,2)
    snr = pwr1.mean()/pwr2.mean()
    return snr

def spkt2impulses(spikes,t):
    """Creates a signal in time from spike instants.
    """
    t = np.round(t,3)
    dt = t[1]
    spikes = spikes-(spikes%dt)
    spikes = np.round(spikes,3)
    if len(spikes.shape)==1:
        spikes = np.array([spikes])        
    impulses = np.zeros((spikes.shape[0],len(t)))
    for s,spkt in enumerate(spikes):
        for spk in spkt:
            impulses[s][t==spk] = 1./dt
    if impulses.shape[0]==1:
        impulses = impulses[0]
    return impulses
    
def spectrum(sig,t):
    sig_fft = np.fft.rfft(sig)
    f_dimless = np.fft.rfftfreq(len(sig))
    dt = t[1]
    N = len(sig)
    T = dt*N
    df = 1./T
    fhz = f_dimless*N*df
    return sig_fft,fhz

def powerSpectrum(sig,dt,norm=None,removeZeroFreq=True):
    """Calculates the power spectrum of a given signal.

    Parameters
    ----------
    sig : array-like
        The signal.
    dt : float
        Time step in ms
    norm : {None, "self", float}
        Normalization option.
    """
    fft = np.fft.rfft(sig)
    fhz = np.fft.rfftfreq(len(sig),dt/1000.)
    fftpwr = np.abs(fft)**2
    if removeZeroFreq:
        fftpwr = fftpwr[1:]
        fhz = fhz[1:]
    else:
        pass
    if isinstance(norm,type(None)):
        nfactor = 1.
    elif norm=="self":
        nfactor = fftpwr.max()
    elif isinstance(norm,float):
        nfactor = norm
    else:
        raise ValueError("invalid value for 'norm'.")
    fftnorm = fftpwr/nfactor
    return fftnorm,fhz

def plotPowerSpectrum(fft,fhz,newfig=False,label=""):
    if newfig:
        plt.figure()
    else:
        pass
    plt.plot(fhz,fft,label=label)
