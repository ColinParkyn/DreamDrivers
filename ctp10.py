# This is a demo class that shows how we can utilize RVisa inside a class wrapper.

# This example class can be used to modify existing classes that our users come in with
#
# It abstracts ResourceManager from the user

import rvisa as visa
import matplotlib.pyplot as plt
import numpy as np
import time

class ctp10(object):
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
        self.instr.write('')

    #unit=DBM for dBm, unit=MW for mW
    #sets spectral units for detector
    def setpowunit(self,mod,channel,unit):
        self.instr.write(f':CTP:SENS{mod}:CHAN{channel}:UNIT:Y {unit}')

    def getpowunit(self,mod,channel):
        return(self.instr.query(f':CTP:SENS{mod}:CHAN{channel}:UNIT:Y?'))

    #returns power in dBm
    def getpow(self,mod,channel):
        return(self.instr.query(f':CTP:SENS{mod}:CHAN{channel}:POW?'))

    #unit=WAV for nm, unit=FREQ for THz
    #sets spectral units for detector
    def setwavunit(self,mod,channel,unit):
        self.instr.write(f':CTP:SENS{mod}:CHAN{channel}:UNIT:X {unit}')

    def getwavunit(self,mod,channel):
        return(self.instr.query(f':CTP:SENS{mod}:CHAN{channel}:UNIT:X?'))

    def getwav(self,mod,channel):
        return(self.instr.query(f':CTP:SENS{mod}:CHAN{channel}:WAV?'))


    ##TODO check the OPC to make sure the command went through

    def checkOPC(self):#True means task complete, false means in progress
        check=self.instr.query('*STB?')
        if check=='1':
            return(True)
        elif check=='0':
            return(False)
        else:
            print(f'*STB?={check}')

