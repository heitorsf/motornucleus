from neuron import h
import os

def writeToFile(cell,soma,dend):
    basewd = os.getcwd()
    os.chdir("./Cells/")
    f = open("Cell_"+str(cell)+".txt","w")
    f.write(str(soma.L))
    f.write("\n")
    f.write(str(soma.diam))
    f.write("\n")
    f.write(str(soma.nseg))
    f.write("\n")
    f.write(str(soma.Ra))
    f.write("\n")
    f.write(str(soma.cm))
    f.write("\n")
    f.write(str(soma.gnabar_napp))
    f.write("\n")
    f.write(str(soma.gnapbar_napp))
    f.write("\n")
    f.write(str(soma.gkfbar_napp))
    f.write("\n")
    f.write(str(soma.gksbar_napp))
    f.write("\n")
    f.write(str(soma.mact_napp))
    f.write("\n")
    f.write(str(soma.rinact_napp))
    f.write("\n")
    f.write(str(soma.ena))
    f.write("\n")
    f.write(str(soma.ek))
    f.write("\n")
    f.write(str(soma.el_napp))
    f.write("\n")
    f.write(str(soma.vtraub_napp))
    f.write("\n")
    f.write(str(soma.gl_napp))
    f.write("\n")
    f.write(str(dend.L))
    f.write("\n")
    f.write(str(dend.diam))
    f.write("\n")
    f.write(str(dend.nseg))
    f.write("\n")
    f.write(str(dend.Ra))
    f.write("\n")
    f.write(str(dend.cm))
    f.write("\n")
    try:
        x = dend.g_pas
    except NameError:
        f.write(str(dend.ecaL))
        f.write("\n")
        f.write(str(dend.gama_caL))
        f.write("\n")
        f.write(str(dend.gcaLbar_caL))
        f.write("\n")
        f.write(str(dend.vtraub_caL))
        f.write("\n")
        f.write(str(dend.Ltau_caL))
        f.write("\n")
        f.write(str(dend.gl_caL))
        f.write("\n")
        f.write(str(dend.el_caL))
    else:
        f.write(str(dend.g_pas))
        f.write("\n")
        f.write(str(dend.e_pas))
    f.close()
    os.chdir(basewd)
    

def saveParams(fromNetpyne,data1=0,somaSec=0,dendSec=0):
    if fromNetpyne:
        for cell in xrange(len(data1)):
            soma = data1[cell].secs.soma.hSec
            dend = data1[cell].secs.dend.hSec
            writeToFile(cell,soma,dend)
    else:
        cell = 0
        soma = somaSec
        dend = dendSec
        writeToFile(cell,soma,dend)


def loadParams(cellnumber,soma,dend):
    basewd = os.getcwd()
    os.chdir("./Cells/")
    f = open("Cell_"+str(cellnumber)+".txt","r")
    soma.L = float(f.readline())
    soma.diam = float(f.readline())
    soma.nseg = int(f.readline())
    soma.Ra = float(f.readline())
    soma.cm = float(f.readline())
    soma.gnabar_napp = float(f.readline())
    soma.gnapbar_napp = float(f.readline())
    soma.gkfbar_napp = float(f.readline())
    soma.gksbar_napp = float(f.readline())
    soma.mact_napp = float(f.readline())
    soma.rinact_napp = float(f.readline())
    soma.ena = float(f.readline())
    soma.ek = float(f.readline())
    soma.el_napp = float(f.readline())
    soma.vtraub_napp = float(f.readline())
    soma.gl_napp = float(f.readline())
    dend.L = float(f.readline())
    dend.diam = float(f.readline())
    dend.nseg = int(f.readline())
    dend.Ra = float(f.readline())
    dend.cm = float(f.readline())
    try:
        x = dend.g_pas
    except NameError:
        dend.ecaL = float(f.readline())       
        dend.gama_caL = float(f.readline())
        dend.gcaLbar_caL = float(f.readline())
        dend.vtraub_caL = float(f.readline()) 
        dend.Ltau_caL = float(f.readline()) 
        dend.gl_caL = float(f.readline())
        dend.el_caL = float(f.readline())
    else:
        dend.g_pas = float(f.readline())
        dend.e_pas = float(f.readline())
    f.close()
    os.chdir(basewd)
