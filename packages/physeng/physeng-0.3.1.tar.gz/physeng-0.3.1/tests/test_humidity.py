#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Andreas Mussgiller
"""

import pytest
import numpy as np
import physeng as pe

def test_humidity():
    h = pe.Humidity()
    
    assert np.isclose(h.SaturationVaporPressure(293),
                      23.118590600388863) == True

    assert np.isclose(h.DewPoint(293, 0.6),
                      285.0088776258169) == True
    
    T = 293.15
    ah1 = h.AbsoluteHumidity(T, 0.6)
    assert np.isclose(ah1,
                      0.0010348265917773552) == True
    
    relh = h.RelativeHumidityFromAbsoluteHumidity(T, ah1)
    assert np.isclose(relh,
                      0.6) == True

    dp = h.DewPointFromAbsoluteHumidity(T, ah1)
    assert np.isclose(dp,
                      285.14989461574544) == True
    
    ah2 = h.AbsoluteHumidityFromDewPoint(T, dp)
    assert np.isclose(ah1, ah2) == True
