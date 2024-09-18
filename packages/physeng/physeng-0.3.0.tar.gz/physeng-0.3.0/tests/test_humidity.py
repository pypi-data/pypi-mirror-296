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

test_humidity()