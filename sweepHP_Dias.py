# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 12:18:06 2021

@author: Colin
"""
import sys
print(sys.executable)
import numpy
import time
import matplotlib.pyplot as plt
import scipy.io as sio
import pandas as pd
from t100slocal import t100s
from datetime import datetime #Added by Dias
t100 = t100s()
t100.connect('GPIB0::11::INSTR')#, reset=0, forceTrans=1)

from HP8163A import HP8163A
HP = HP8163A()
HP.connect('GPIB0::21::INSTR')

def max(data,maxval):
    for i in range(len(data)):
        if data[i]>maxval:
            maxval=data[i]
        else:
            pass
    return(maxval)
    
def interpolate_gaps(values, limit=None):
    """
    Fill gaps using linear interpolation, optionally only fill gaps up to a
    size of `limit`.
    """
    values = numpy.asarray(values)
    i = numpy.arange(values.size)
    valid = numpy.isfinite(values)
    filled = numpy.interp(i, i[valid], values[valid])

    if limit is not None:
        invalid = ~valid
        for n in range(1, limit+1):
            invalid[:-n] &= invalid[n:]
        filled[invalid] = numpy.nan

    return filled

def P_w(wi,wf,steps,filename,wave=1240,power=1):
    #Don't use this bit as documentation yet
    #wi=initial wavelength in nm
    #wf=final wavelength in nm
    #steps=number of steps inbetween wi and wf
    #filename=name of file to save data
    #wave=wavelength in nm
    #power=optical power in mw
    plt.clf()
    OpticalPower=[]
    domain=numpy.linspace(wi,wf,steps)
    t100.setwav(wave)
    t100.setunit('DBM')
    t100.setpow(power,'+')
    t100.enable(True)
    time.sleep(1)
    for i in range(len(domain)):
        t100.setwav(domain[i])
        #Edited to .01
        time.sleep(.001)#can remove if this takes too long, idk how long it will take to change wavelength
        Data=HP.getPower(2)
        #if Data>99 or Data<-99:
           # Data=OpticalPower[-1]
        OpticalPower.append(Data)
        #print("WaveLength: ",t100.getwav())
        #print("Optical Power: ",Data)#," ,Total List: ", OpticalPower)
    t100.enable(False)
    t100.setwav(1270)
    time.sleep(.001) #Edited to .01
    #sio.savemat(filename+str('asdfadsf'),{"wavelength":domain,"Power":OpticalPower})
    writer=open((filename+".csv"),'w')
    for i in range(len(OpticalPower)):
        writer.write(str(domain[i])+','+str(OpticalPower[i]))
        writer.write('\n')

    df = pd.DataFrame(OpticalPower, columns=['Power'])
    df = df[(df < 999) & (df > -999)]
    now = datetime.now()    
    sio.savemat(filename+'_loopback_'+now.strftime("%d-%m-%Y_%H-%M-%S"),{"wavelength":domain,"Power":df.Power.values.tolist()})
    plt.plot(domain, df.Power.values.tolist())    
    plt.xlim(1240,1380)
    plt.savefig(filename+'_loopback_'+now.strftime("%d-%m-%Y_%H-%M-%S")+'.png') 

P_w(1240,1380,1400,'bumptesting')
