"""
    A Python class for running multiple OPAL jobs based on an input template.
"""

import os
from datetime import datetime
import string
import subprocess
import numpy as np

T_OFFSET = -4.27285889623020639999745562670770232e-9 # s
NOMINAL_FREQ = 116.4e6 # Hz

SIM_DEFAULTS = {
    'phiv': 5.46434243453193694729121762974294316e-3, # rad
    'rinit': 1.1221244734042559 * 1e3, # mm
    # nominally, offset by the dt between my clock and Dior's
    'phi_correction': 2*np.pi * NOMINAL_FREQ * T_OFFSET  
}

class OPALSFCRunner():
    """
    A class for managing SFC runs

    Given a template file and set of parameters, create a directory for the
    new simulation, do the appropriate substitutions, and run the simulation.
    """
    # TODO: 
    #   flags for controlling diagnostic information
    #   point out errors easily missed in OPAL output
    #   metadata about input files?
    def __init__(self, template_file, **simargs):
        """
        template_file - path to SFC.in.template

        --optional named arguments--
        inputdir - path to input/ (fieldmaps, dist.dat)
            (if not provided, look for an "input/" directory adjacent to
            template_file)
        rinit - initial radius (mm)
        phiv - initial CLOCKWISE velocity angle from azimuth (rad)
        phi_correction - RF phase offset applied to all cavities on top of -25 deg and transit factor
        """
        if 'inputdir' not in simargs:
            print("looking for input/ in the same directory as %s" % template_file)
            path = os.path.dirname(template_file)
            path = os.path.abspath(path)
            inputdir = os.path.join(path, "input")

        self.simargs = SIM_DEFAULTS.copy()
        self.simargs['INPUTDIR'] = inputdir
        self.simargs.update({k:v for k,v in simargs.items() if v is not None})
        self.prefix = os.path.splitext(template_file)[0]

        with open(template_file, 'r') as infile:
            self.template = string.Template(infile.read())
        
    @property
    def simtext(self):
        return self.template.substitute(**self.simargs)

    def run(self):
        """ Perform the simulation """
        self.lastrun = datetime.now()
        timestamp = self.lastrun.strftime("%m%d%Y-%H%M%S")
        outfn = "%s.in" % timestamp
        workdir = "{fn}_{ts}".format(fn=self.prefix, ts=timestamp)
        # TODO: what should be done if directory already exists?
        # (e.g. if we want to re-run a simulation)
        os.mkdir(workdir)

        olddir = os.getcwd()
        os.chdir(workdir)
        with open(outfn, 'w') as outfile:
            outfile.write(self.simtext)

        subprocess.call(['opal', outfn], env=os.environ) #, stdout=foo, stderr=bar)
        os.chdir(olddir)

    def postprocess(self):
        """ Make plots, calculate phases, etc. """
        raise NotImplementedError
