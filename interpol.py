#usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Set 28 2017

@author: heitor
"""

import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
numCells = 120

def cellDistrib(numCells, ascending=True):
    return 101,17,2
    '''
    numS = int(numCells/2)
    numFF = int((numCells - numS)/2)
    numFR = numCells - numS - numFF
    if numCells==1:
        if ascending:
            return 1,0,0
        else:
            return 0,0,1
    else:
        if ascending:
            return numS, numFR, numFF
        else:
            return numFF, numFR, numS
    '''

def linDistrib(numCells,mid, d_range):
    low = mid - d_range
    high = mid + d_range
    Param = np.linspace(low,high,numCells)
    return Param

def interpol_lin(numCells,midS,midFR,midFF,set_firstS=False,set_lastFF=False):
    
    midS = midS*1.
    midFR = midFR*1.
    midFF = midFF*1.

    case = 'None'
    
    if (midS<=midFR) & (midFR<=midFF):
        numS, numFR, numFF = cellDistrib(numCells, ascending=True)
        case = 'rising'
    elif (midS>=midFR) & (midFR>=midFF):
        numS, numFR, numFF = cellDistrib(numCells, ascending=False)
        aux = midS
        midS = midFF
        midFF = aux
        case = 'falling'
    elif (midS<midFR) & (midFR>midFF):
        numS, numFR, numFF = cellDistrib(numCells, ascending=True)
        case = 'peak'

    elif (midS>midFR) & (midFR<midFF):
        numS, numFR, numFF = cellDistrib(numCells, ascending=True)
        case = 'valley'
    else:
        raise ValueError("interpol_lin cannot compute this case, use interpol_point.")

    if case=='rising' or case=='falling':
        a = abs(midFR-midS)
        b = abs(midFF-midFR)
    
        #          a                b 
        # (midS)-------(midFR)-------------(midFF)
    
        if a>=b:
            range1 = b/2.
            range2 = a - range1
            lowS = midS - range2
            lowFR = midFR - range1
            lowFF = midFF - range1
            highFF = midFF + range1
    
        #     range2        range2      range1      range1   range1      range1
        # |------------(S)------------|--------(FR)--------|--------(FF)--------|
        #
        #                 \---------a---------/    \-------b-------/
    
        else: # b>a
            range1 = a/2.
            range2 = b - range1
            lowS = midS - range1
            lowFR = midFR - range1
            rising = 1
            if midFF < midFR:
                rising = -1
            lowFF = midFF - range2*rising
            highFF = midFF + range2*rising
    
        #   range1     range1   range1      range1     range2         range2
        # |--------(S)--------|--------(FR)--------|------------(FF)------------|
        #
        #             \-------a-------/    \---------b---------/

    elif case=='peak':
        range1 = (midFR - midS)/2.
        firstS = midS - range1
        firstFR = midFR - range1
        
        range2 = (midFR- midFF)/2.
        lastFR = midFR - range2
        lastFF = midFF - range2
        
    elif case=='valley':
        range1 = (midS - midFR)/2.
        firstS = midS + range1
        firstFR = midFR + range1

        range2 = (midFF - midFR)/2.
        lastFR = midFR + range2
        lastFF = midFF + range2
        
    else:
        raise ValueError("Case not understood.")

    # create the final arrays:

    if case=='rising' or case=='falling':
        if lowS<0:
            lowS = midS*0.5
        if set_firstS:
            numSmid = int(numS/2.)
            S1 = np.linspace(set_firstS,midS,numSmid,endpoint=False)
            S2 = np.linspace(midS,lowFR,numS-numSmid,endpoint=False)
            S = np.concatenate((S1,S2))
        else:
            S = np.linspace(lowS,lowFR,numS,endpoint=False)
        FR = np.linspace(lowFR,lowFF,numFR,endpoint=False)
        if set_lastFF:
            numFFmid = int(numFF/2.)
            FF1 = np.linspace(lowFF,midFF,numFFmid,endpoint=False)
            FF2 = np.linspace(midFF,set_lastFF,numFF-numFFmid,endpoint=True)
            FF = np.concatenate((FF1,FF2))
        else:
            FF = np.linspace(lowFF,highFF,numFF)
    elif case=='peak' or case=='valley':
        if firstS<0:
            firstS = midS*0.5
        if lastFF<0:
            lastFF = midFF*0.5
        if set_firstS:
            numSmid = int(numS/2.)
            S1 = np.linspace(set_firstS,midS,numSmid,endpoint=False)
            S2 = np.linspace(midS,firstFR,numS-numSmid,endpoint=False)
            S = np.concatenate((S1,S2))
        else:
            S = np.linspace(firstS,firstFR,numS,endpoint=False)
        numFRmid = int(numFR/2.)
        FR1 = np.linspace(firstFR,midFR,numFRmid,endpoint=False) 
        FR2 = np.linspace(midFR,lastFR,numFR-numFRmid,endpoint=False)
        FR = np.concatenate((FR1,FR2))
        if set_lastFF:
            numFFmid = int(numFF/2.)
            FF1 = np.linspace(lastFR,midFF,numFFmid,endpoint=False)
            FF2 = np.linspace(midFF,set_lastFF,numFF-numFFmid,endpoint=True)
            FF = np.concatenate((FF1,FF2))
        else:
            FF = np.linspace(lastFR,lastFF,numFF)

#        if firstS<(midS/2.):
#            wehavemidS = True
#            firstS = midS/2.

    else:
        raise ValueError("Case not understood.")

    if numS==1:
        S = np.array([midS])
    if numFR==1:
        FR = np.array([midFR])
    if numFF==1:
        FF = np.array([midFF])

    Param = np.concatenate((S,FR,FF))

#    raise ValueError()

    if case=='rising' or case=='peak' or case=='valley':
        return (Param)
    elif case=='falling':
        return (np.flip(Param,axis=0))
    else:
        raise ValueError("Case not understood")


def interpol_point(numCells,midS,midFR,midFF):
    numS, numFR, numFF = cellDistrib(numCells)
    
    midS = midS*1.
    midFR = midFR*1.
    midFF = midFF*1.

    firstS = midS
    firstFR = firstS + (midFR-midS)/2
    midFR = midFR
    firstFF = midFR - (midFR-midFF)/2
    lastFF = midFF

    numFRmid = int(numFR/2)
    S = np.linspace(firstS,firstFR,numS,endpoint=False)
    FR1 = np.linspace(firstFR,midFR,numFRmid,endpoint=False)
    FR2 = np.linspace(midFR,firstFF,numFR-numFRmid,endpoint=False)
    FF = np.linspace(firstFF,lastFF,numFF)
    Param = np.concatenate((S,FR1,FR2,FF))

    return(Param)
    
def interpol_exp(n,xmin,xmax,ascending):
    xmin *= 1.
    xmax *= 1.

    rp = xmax/xmin
    b = np.log(rp)/n
    I = np.arange(1,n+1,1)

    if ascending:
        Param = xmin * np.exp(b*I)
    else:
        Param = xmax * np.exp(-b*I)

    return Param

def interpol_fit(numCells,midS,midFR,midFF,degree=4):
    numS, numFR, numFF = cellDistrib(numCells)
    x = np.array([numS/2., numS+numFR/2., numS+numFR+numFF/2.])
    y = np.array([midS, midFR, midFF])
    z = np.polyfit(x,y,degree)
    p = np.poly1d(z)
    out = p(np.arange(1,numCells+1,1))
    return out

def exp_crescent(x, a, b, c):
    return a * np.exp(b * x) + c

def exp_decrescent(x, a, b, c):
    return a * np.exp(-b * x) + c

def interpol_expfit(n,first,last,curv=1./3.):
    x = np.linspace(0,4,3)
    #x = np.logspace(np.log(0.01),np.log(4),3)
    xp = np.linspace(0,4,n)
    if first <= last:
        y = exp_crescent(x, 1., 1., 0.5)
        #import pdb
        #pdb.set_trace()
        yn = np.array([first,first+(last-first)*curv,last])/first
        popt, pcov = curve_fit(exp_crescent, x, yn)
        #raise IOError
        param = exp_crescent(xp,*popt)*first
    else:
        y = exp_decrescent(x, 1., 1., 0.5)
        yn = np.array([first,last+(first-last)*curv,last])/last
        popt, pcov = curve_fit(exp_decrescent, x, yn)
        param = exp_decrescent(xp,*popt)*last
    #print("Expfit")
    #print(popt)
    #plt.figure()
    #plt.plot(x, yn, 'ko', label="Sampled Data")
    return param
 
def interpol_minus_exp(n,first,last,curv=1./3.):
    x = np.linspace(0,4,3)
    xp = np.linspace(0,4,n)
    if last <= first:
        y = exp_crescent(x, 1., 1., 0.5)
        yn = np.array([first,first+(last-first)*curv,last])/first
        popt, pcov = curve_fit(exp_crescent, x, yn)
        param = exp_crescent(xp,*popt)*first
    else:
        y = exp_decrescent(x, 1., 1., 0.5)
        yn = np.array([first,last+(first-last)*curv,last])/last
        popt, pcov = curve_fit(exp_decrescent, x, yn)
        param = exp_decrescent(xp,*popt)*last
    #print("Minus_exp")
    #print(popt)
    return param

def interpol_rand(param,sigma_perc=.03,seed=1):
    np.random.seed(seed)
    mu = 0
    sigma = sigma_perc*(param.max()-param.min())
    param_n = param + np.random.normal(mu,sigma,size=len(param))
    #param_n = param + np.random.normal(mu,sigma_perc*param)
    try:
        if any(param_n < param.min()/2.):
            raise ValueError
        else:
            pass
    except ValueError:
        param_n = interpol_rand(param,sigma_perc=sigma_perc*0.9)
    return param_n
