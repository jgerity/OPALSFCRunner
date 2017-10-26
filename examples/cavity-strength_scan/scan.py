"""
  Vary cavity voltages by 1% to assess RF stability
"""
from OPALSFCRunner import OPALSFCRunner
import numpy as np
import itertools

runner = OPALSFCRunner('SFC.in.template', inputdir='/vagrant_data/SFC/input')

CAV1 = [0.99, 1.00, 1.01]
CAV2 = [1.00]
CAV3 = [1.00]
CAV4 = [1.00]

for c1, c2, c3, c4 in itertools.product(CAV1, CAV2, CAV3, CAV4):
    runner.simargs['CAV1SCALE'] = c1
    runner.simargs['CAV2SCALE'] = c2
    runner.simargs['CAV3SCALE'] = c3
    runner.simargs['CAV4SCALE'] = c4
    runner.run()
