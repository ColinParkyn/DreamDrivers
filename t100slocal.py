import pyvisa as visa
import matplotlib.pyplot as plt
import numpy as np
import time

class t100s(object):
    # Change this to the IDN string of your instrument
    # if you do not know this, then set this to ''
    name = ''
    rm = ''
    connected = False

    # Use this init function
    def __init__(self):
        self.rm = visa.ResourceManager()
        #self.connected = self.rm.CONNECTED
        self.unit=''

    # Optional: if you want to automatically find out what addresses the instrument is on
    def find(self):
        has_instr = list()
        if self.connected:
            resources = self.rm.list_resources()
            for res in resources:
                ID = self.rm.open_resource(res).query('*IDN?')
                if ID == self.name:
                    has_instr.append(res)
            return tuple(has_instr)
        else:
            raise Exception('Not connected!')
    
    # Use this function
    def connect(self, visaAddr):
        self.instr = self.rm.open_resource(visaAddr)

    # Use this function
    def close(self, visaAddr):
        self.instr.close()

    # Optional function: returns IDN string
    def idn(self):
        return self.instr.query('*IDN?')

    def enable(self,state):
        if state==True:
            self.instr.write('ENABLE')
        elif state==False:
            self.instr.write('DISABLE')

    #'MW' or 'DBM'
    def setunit(self,unit):
        unit=str(unit)
        self.instr.write(unit)
        self.unit=unit
        #print(self.instr.query(f"Units set to {unit} "  ))

    #type power as xx.xx, sign is only for dBm
    def setpow(self,pow,sign):
        if self.unit=='DBM':
            self.instr.write('P='+str(sign)+str(pow))
        elif self.unit=='MW':
            self.instr.write('P='+str(pow))
        else:
            print('unit not set')

    def getpow(self):
        return(self.instr.query('P?'))

    #curr=xxx.x, has range from 0-400 mA
    def setcurr(self,curr):
        self.instr.write('I='+str(curr))

    def getcurr(self):
        return(self.instr.query('I?'))

    #wav=xxxx.xxx nm
    def setwav(self,wav): 
        self.instr.write('L='+str(wav))

    def getwav(self):
        return(self.instr.query('L?'))

    #end=MIN or end=MAX
    def getwavlim(self,end):
        return(self.instr.query('L? '+str(end)))

    #speed=xxx, check programming guide for values, if not a value will round automatically
    def setspeed(self,speed):
        self.instr.write('MOTOR_SPEED='+str(speed))

    def getspeed(self):
        return(self.instr.query('MOTOR_SPEED?'))
