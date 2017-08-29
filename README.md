# OPALSFCRunner

A Python class for running multiple OPAL jobs based on an input template.

### Notes
* Templating is done using Python's `string.Template()` with the default `$`
token. For example, the explicit `inputdir` simulation argument controls the
`$INPUTDIR` variable (see below), allowing the specification of a directory for
simulation input files (which may be large enough to discourage making many
copies). In a future revision, this argument will probably be less explicit so
that the end-user may use whatever naming scheme(s) they prefer.

```
// OPAL.in.template
...
Dist1: DISTRIBUTION, DISTRIBUTION = FROMFILE, FNAME = "$INPUTDIR/dist.dat";
...
```

* When `OPALSFCRunner.run()` is called, a new directory labeled with the name
of the input file and the current timestamp is created to contain the final
input file and output files.

### Example usage
The example below serially runs 25 simulations to scan combinations of two
parameters with 5 distinct values each. More sophisticated optimization (e.g.
a genetic algorithm) could take advantage of post-processing of the results of
the run once it is finished.

```python
from OPALSFCRunner import OPALSFCRunner
import numpy as np
import itertools

DEFAULT_PHIV = 5.5e-3 # rad
DEFAULT_RINIT = 1.1 * 1e3 # mm

# +/- 2% in 0.5% increments --> 5 data points
rinit = DEFAULT_RINIT * (1.0 + np.linspace(-0.02, 0.02, 5))
phiv = DEFAULT_PHIV * (1.0 + np.linspace(-0.02, 0.02, 5))

runner = OPALSFCRunner('SFC.in.template')

for r, pv in itertools.product(rinit, phiv):
    runner.simargs['rinit'] = r
    runner.simargs['phiv'] = pv
    runner.run()
```
