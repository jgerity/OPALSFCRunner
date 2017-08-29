from OPALSFCRunner import OPALSFCRunner
import numpy as np
import itertools

DEFAULT_PHIV = 5.46434243453193694729121762974294316e-3 # rad
DEFAULT_RINIT = 1.1221244734042559 * 1e3 # mm

# +/- 2% in 0.5% increments --> 5 data points
rinit = DEFAULT_RINIT * (1.0 + np.linspace(-0.02, 0.02, 5))
phiv = DEFAULT_PHIV * (1.0 + np.linspace(-0.02, 0.02, 5))

runner = OPALSFCRunner('SFC.in.template')

for r, pv in itertools.product(rinit, phiv):
    runner.simargs['rinit'] = r
    runner.simargs['phiv'] = pv
    runner.run()
