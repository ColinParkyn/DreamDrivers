# -*- coding: utf-8 -*-
"""
Created on Wed Aug 11 13:29:19 2021

@author: Colin
"""

import pyvisa as visa
import time

class HP8163A(object):
    
    def __init__(self):
        self.connected = False
        
    def __del__(self):
        if self.connected:
            self.disconnect()
            
    def connect(self,visaAddr):    
        self.rm = visa.ResourceManager()
        self.instrument = self.rm.open_resource(visaAddr)        
        self.instrument.timeout=10000
        print(self.instrument.query("*IDN?")) #Requests the device for identification
        self.connected = True
        
    def disconnect(self):
        self.instrument.close()
        
    def query(self,command):
        return(self.instrument.query(command))
        
    def write(self,command):
        print(self.instrument.write(command))
    
    def read(self,command):
        print(self.instrument.read(command))
    
    def getPower(self,slot):
        power=self.instrument.query('FETC'+str(slot)+':POW?')
        return float(power)
