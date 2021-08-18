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
from datetime import datetime #Added by Dias
from t100slocal import t100s
t100 = t100s()
t100.connect('GPIB0::11::INSTR')#, reset=0, forceTrans=1)

from AQ6317B import AQ6317B
AQ = AQ6317B('GPIB0::15::INSTR')

def max(data,maxval):
    for i in range(len(data)):
        if data[i]>maxval:
            maxval=data[i]
        else:
            pass
    return(maxval)
    
def P_w(wi,wf,steps,filename,wave=1240,power=1):
    #Don't use this bit as documentation yet
    #wi=initial wavelength in nm
    #wf=final wavelength in nm
    #steps=number of steps inbetween wi and wf
    #filename=name of file to save data
    #wave=wavelength in nm
    #power=optical power in mw
    #Set centre to where wavelength is and have a small wavelength 
    OpticalPower=[]
    domain=numpy.linspace(wi,wf,steps)
    t100.setwav(wave)
    t100.setunit('DBM')
    t100.setpow(power,'+')
    t100.enable(True)
    AQ.setReference(-4)
    #print(AQ.query('REFL?'))
    time.sleep(3)
    for i in range(len(domain)):
        maxval=-99999999999999999999
        t100.setwav(domain[i])
        time.sleep(.1)#can remove if this takes too long, idk how long it will take to change wavelength
        AQ.SingleSweep()
        OpticalPower.append(max(AQ.getPower(),maxval))
        print(t100.getwav(),max(AQ.getPower(),maxval))
        print("Optical Power: ", OpticalPower)
    t100.enable(False)
    t100.setwav(1270)
    
    for i in range(len(OpticalPower)):
        if OpticalPower[i]<-99:
            OpticalPower[i]=0
            OpticalPower[i]=(OpticalPower[i+1]+OpticalPower[i-1])/2
        print(domain[i],": ",OpticalPower[i])
    now = datetime.now()    
    sio.savemat(filename+'_loopback_'+now.strftime("%d-%m-%Y_%H-%M-%S"),{"wavelength":domain,"Power":OpticalPower})
    plt.plot(domain, OpticalPower)    
    plt.savefig(filename+'_loopback_'+now.strftime("%d-%m-%Y_%H-%M-%S")+'.png') 
    print("Final Data: ", OpticalPower)
    #plt.plot(domain,OpticalPower)
    #plt.show()
P_w(1240,1380,14,'test_modular_pw')
