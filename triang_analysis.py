"""
analysis.py

Functions to read and plot figures from the batch simulation results.
"""

import json
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
import pickle
import numpy as np
from pylab import *
from itertools import product
from pprint import pprint
from netpyne import specs
from collections import OrderedDict

def simDataFromFile(filename):
    with open(filename, 'r') as fileObj:
        dataLoad = json.load(fileObj, object_pairs_hook=OrderedDict)
    simData = dataLoad['simData']
    return simData

def plotInstFreq(simData,filename,newFigure=True):
    v = np.array(simData['V_soma']['cell_0'])
    t = np.array(simData['t'])
    spkt = np.array(simData['spkt'])
    isi = np.diff(spkt)
    ifreq = 1000./isi  # estimates instantaneus frequency
    if newFigure:
        plt.figure();
    else:
        pass
    plt.ylabel("Inst. Freq (imp/s)")
    plt.plot(ifreq,label=filename) 
    plt.legend()

# Main code
if __name__ == '__main__':
    files = ['output_soma_0', 'output_soma_1']
    for f, filename in enumerate(files):
        full_filename = filename+'.json'
        simData = simDataFromFile(full_filename)
        if f==0:
            newFigure = True
        else:
            newFigure = False 
        plt.ion()
        plotInstFreq(simData,filename,newFigure=newFigure)
    #plot.show()
