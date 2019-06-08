#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 15:25:56 2019

@author: rafael
"""

import numpy as np
import wave, math

s_rate = 44100
n_samples = s_rate * 5
x = np.arange(n_samples) / float(s_rate)
vals = np.sin(2.0 * math.pi * 220.0 * x)
data = np.array(vals * 32767, 'int16').tostring()
file = wave.open('sine220.wav', 'wb')
file.setparams((1, 2, s_rate, n_samples, 'NONE', 'uncompressed'))
file.writeframes(data)
file.close()