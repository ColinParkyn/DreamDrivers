# This is a demo class that shows how we can utilize RVisa inside a class wrapper.

# This example class can be used to modify existing classes that our users come in with
#
# It abstracts ResourceManager from the user

import rvisa as visa
import matplotlib.pyplot as plt
import numpy as np
import time

class t100s(object):
    # Change this to the IDN string of your instrument
    # if you do not know this, then set this to ''
    name = ''
    rm = ''
    api = ''
    connected = False

    # Use this init function
    def __init__(self, api_addr=''):
        self.rm = visa.ResourceManager(api_addr)
        self.api = api_addr
        self.connected = self.rm.CONNECTED
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
        print(self.instr.query(f'Units set to {unit}'))

    #type power as xx.xx, sign is only for dBm
    def setpow(self,pow,sign):
        if self.unit=='DBM':
            self.instr.write(f'P={sign}{pow}')
        elif self.unit=='MW':
            self.instr.write(f'P={pow}')
        else:
            print('unit not set')

    def getpow(self):
        return(self.instr.query('P?'))

    #curr=xxx.x, has range from 0-400 mA
    def setcurr(self,curr):
        self.instr.write(f'I={curr}')

    def getcurr(self):
        return(self.instr.query('I?'))

    #wav=xxxx.xxx nm
    def setwav(self,wav): 
        self.instr.write(f'L={wav}')

    def getwav(self,wave):
        return(self.instr.query('L?'))

    #end=MIN or end=MAX
    def getwavlim(self,end):
        return(self.instr.query(f'L? {end}'))

    #speed=xxx, check programming guide for values, if not a value will round automatically
    def setspeed(self,speed):
        self.instr.write(f'MOTOR_SPEED={speed}')

    def getspeed(self):
        return(self.instr.query('MOTOR_SPEED?'))

    ##TODO check the OPC to make sure the command went through

    def checkOPC(self):#True means task complete, false means in progress
        check=self.instr.query('*STB?')
        if check=='1':
            return(True)
        elif check=='0':
            return(False)
        else:
            print(f'*STB?={check}')
