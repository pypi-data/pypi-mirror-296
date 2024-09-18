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

    def SaturationVaporPressureWagnerPruss(self, T: float) -> float:
        '''
        Returns the saturation water vapor pressure according to Wagner
        and Pruss (https://doi.org/10.1063/1.1461829) for a given temperature.

        Parameters
        ----------
        T : float
            Temperature in K

        Returns
        -------
        float
            Saturation water vapor pressure in hPa
        '''
        
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
    
    def SaturationVaporPressureAlduchovEskridge(self, T: float) -> float:
        '''
        Returns the saturation water vapor pressure according to Alduchov
        and Eskridge (https://doi.org/10.1175/1520-0450(1996)035%3C0601:IMFAOS%3E2.0.CO;2)
        for a given temperature.

        Parameters
        ----------
        T : float
            Temperature in K

        Returns
        -------
        float
            Saturation water vapor pressure in hPa
        '''
        
        A = 17.625
        B = 243.04 # °C
        C = 6.1094 # Pa;
    
        return C * np.exp(A*(T-273.15)/(B+(T-273.15))) # hPa
    
    def SaturationVaporPressure(self, T: float) -> float:
        '''
        Returns the saturation water vapor pressure according to Alduchov
        and Eskridge (https://doi.org/10.1175/1520-0450(1996)035%3C0601:IMFAOS%3E2.0.CO;2)
        for a given temperature.
        
        Parameters
        ----------
        T : float
            Temperature in K

        Returns
        -------
        float
            Saturation water vapor pressure in hPa
        '''

        return self.SaturationVaporPressureAlduchovEskridge(T)
        
    def WaterVaporPartialPressure(self, T: float, relH: float) -> float:
        '''
        Returns the water vapor partial pressure for a given temperature and
        relative humidity.

        Parameters
        ----------
        T : float
            Temperature in K
        relH : float
            Relative humnidity [0,1]

        Returns
        -------
        float
            water vapor partial pressure in hPa
        '''
        
        return self.SaturationVaporPressure(T) * relH

    def AbsoluteHumidity(self, T: float, relH: float) -> float:
        '''
        Returns the absolute humidity for a given temperature and relative
        humidity.

        Parameters
        ----------
        T : float
            Temperature in K
        relH : float
            Relative humnidity [0,1]

        Returns
        -------
        float
            Absolute humidity in g/cm^3
        '''
        
        return 10 * self.WaterVaporPartialPressure(T, relH) / (461.52 * T)

    def DewPointLawrence(self, T: float, relH: float) -> float:
        '''
        Returns the dew point according to Lawrence
        (https://doi.org/10.1175/BAMS-86-2-225) for a given temperature and
        relative humidity.

        Parameters
        ----------
        T : float
            Temperature in K
        relH : float
            Relative humnidity [0,1]

        Returns
        -------
        float
            Dew point in K

        '''
        
        A = 17.625
        B = 243.04 # °C
        C = 610.94 # Pa

        pp = self.WaterVaporPartialPressure(T, relH) * 100

        return 273.15 + B*np.log(pp/C)/(A-np.log(pp/C));

    def DewPoint(self, T: float, relH: float) -> float:
        '''
        Returns the dew point according to Lawrence
        (https://doi.org/10.1175/BAMS-86-2-225) for a given temperature and
        relative humidity.

        Parameters
        ----------
        T : float
            Temperature in K
        relH : float
            Relative humnidity [0,1]

        Returns
        -------
        float
            Dew point in K

        '''

        return self.DewPointLawrence(T, relH)
    
    def RelativeHumidityFromAbsoluteHumidity(self, T: float, ah: float) -> float:
        '''
        Returns the relative humidity for a given temperature and absolute
        humidity.

        Parameters
        ----------
        T : float
            Temperature in K
        ah : float
            Absolute humidity in g/cm^3

        Returns
        -------
        float
            Relative humnidity [0,1]

        '''
        return 0.1 * ah * T * 461.52 / self.SaturationVaporPressure(T)
    
    def DewPointFromAbsoluteHumidity(self, T: float, ah: float) -> float:
        '''
        Returns the dew point for a given temperature and absolute humidity.

        Parameters
        ----------
        T : float
            Temperature in K
        ah : float
            Absolute humidity in 10^2 kg/m^3

        Returns
        -------
        float
            Dew point in K

        '''
        return self.DewPoint(T, self.RelativeHumidityFromAbsoluteHumidity(T, ah))
    
    def RelativeHumidityFromDewPoint(self, T: float, Td: float) -> float:
        '''
        Returns the realtive humidity for a given temperature and dew point.

        Parameters
        ----------
        T : float
            Temperature in K
        Td : float
            Dew point in K

        Returns
        -------
        float
            Relative humidity [0,1]

        '''
        pv = self.SaturationVaporPressure(T)
        pp = self.SaturationVaporPressure(Td)
        return pp/pv
    
    def AbsoluteHumidityFromDewPoint(self, T: float, Td: float) -> float:
        '''
        Returns the absolute humidity for a given temperature and dew point.

        Parameters
        ----------
        T : float
            Temperature in K
        Td : float
            Dew point in K

        Returns
        -------
        float
            Absolute humidity in 10^2 kg/m^3

        '''
        relh = self.RelativeHumidityFromDewPoint(T, Td);
        return self.AbsoluteHumidity(T, relh)
