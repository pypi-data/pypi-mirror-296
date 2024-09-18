#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Andreas Mussgiller
"""

import logging

import numpy as np 

import physeng as pe

class Humidity(metaclass=pe.Singleton):
    def __init__(self):
        logging.basicConfig(format="{asctime} [{levelname}:{name}]: {message}",
                        style="{",
                        datefmt="%Y-%m-%d %H:%M",
                        level=logging.INFO)
        self._logger = logging.getLogger('Humidity')

    def SaturationVaporPressureWagnerPruss(self, T):
        Tc = 647.096 # K
        Pc = 220640 # hPa

        C1 = -7.85951783
        C2 = 1.84408259
        C3 = -11.7866497
        C4 = 22.6807411
        C5 = -15.9618719
        C6 = 1.80122502

        t = 1.0 - T/Tc

        temp = C1 * t
        temp += C2 * np.power(t, 1.5)
        temp += C3 * np.power(t, 3.0)
        temp += C4 * np.power(t, 3.5)
        temp += C5 * np.power(t, 4.0)
        temp += C6 * np.power(t, 7.5)
        temp *= Tc/T

        return Pc * np.exp(temp) # hPa
    
    def SaturationVaporPressureAlduchovEskridge(self, T):
        A = 17.625
        B = 243.04 # °C
        C = 6.1094 # Pa;
    
        return C * np.exp(A*(T-273.15)/(B+(T-273.15))) # hPa
    
    def SaturationVaporPressure(self, T):
        return self.SaturationVaporPressureAlduchovEskridge(T)
    
    def WaterVaporPartialPressure(self, T, relH):
        return self.SaturationVaporPressure(T) * relH

    def AbsoluteHumidity(self, T, relH):
        return self.WaterVaporPartialPressure(T, relH) / (461.52 * T)

    def DewPointLawrence(self, T, relH):
        A = 17.625
        B = 243.04 # °C
        C = 610.94 # Pa

        pp = self.WaterVaporPartialPressure(T, relH) * 100

        return 273.15 + B*np.log(pp/C)/(A-np.log(pp/C));

    def DewPoint(self, T, relH):
        return self.DewPointLawrence(T, relH)
    
    def RelativeHumidityFromAbsoluteHumidity(self, T, ah):
        return ah * T * 461.52 / self.SaturationVaporPressure(T)
    
    def DewPointFromAbsoluteHumidity(self, T, ah):
        return self.DewPoint(T, self.RelativeHumidityFromAbsoluteHumidity(T, ah))
    
    def RelativeHumidityFromDewPoint(self, T, Td):
        pv = self.SaturationVaporPressure(T)
        pp = self.SaturationVaporPressure(Td)
        return pp/pv
    
    def AbsoluteHumidityFromDewPoint(self, T, Td):
        relh = self.RelativeHumidityFromDewPoint(T, Td);
        return self.AbsoluteHumidity(T, relh)
