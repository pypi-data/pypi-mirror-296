#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Andreas Mussgiller
"""

import pytest
import physeng as pe

def test_ISO286():
    iso286hole = pe.ISO286Hole()
    iso286shaft = pe.ISO286Shaft()
    
    dm6 = iso286shaft.DimensionsForGrade('m6')
    assert dm6 == (0.0, 400.0)
    
    t4m6 = iso286shaft.Tolerance(4.0, 'm6')
    assert t4m6 == (4.0, 12.0)
    
    dH7 = iso286hole.DimensionsForGrade('H7')
    assert dH7 == (0.0, 400.0)
    
    t16H7 = iso286hole.Tolerance(16.0, 'H7')
    assert t16H7 == (0.0, 18.0)
