####################################################################################################
# PYTHON STARTUP CODE #
####################################################################################################
# This code will run before presenting a command prompt after starting python/ipython.
#
# Usage:
# Export the environment variable PYTHONSTART in your shell of choice. Its value needs to be the
# path to this startup script. Example:
#
# bash $ export /home/giantmolecularcloud/.python_startup.py
#
# This script is meant to provide some examples of what can be done. Some of them might not be useful
# for you or may even crash.
#
####################################################################################################

from __future__ import division                 # fix divisions for python 2
import sys                                      # import various packages that I use in every single
import subprocess                               # project
import os
import time
import datetime
import numpy as np
from multiprocessing import Pool
import pickle
import glob
import copy
from tqdm import tqdm
import itertools


####################################################################################################
# restore execfile in python 3 to replace the ridiculous way of calling scripts
####################################################################################################

if ( sys.version_info[0] == 3 ):
    def execfile(filename, globals=None, locals=None):
        if globals is None:
            globals = sys._getframe(1).f_globals
        if locals is None:
            locals = sys._getframe(1).f_locals
        globals.update({
            "__file__": filename,
            "__name__": "__main__",
        })
        with open(filename, 'rb') as file:
            exec(compile(file.read(), filename, 'exec'), globals, locals)

    print("\x1b[0;31;40mDefined execfile to be used in python3.\x1b[0m")


####################################################################################################
# unset environment variables that cause anoying warning messages
####################################################################################################

# OMP refers to openMP, a parallelisation framework. Its environment variables can cause extremly
# annoying warning messages in some python packages.

try:
    import os
    del os.environ['OMP_STACKSIZE']
    del os.environ['GOMP_STACKSIZE']
    del os.environ['KMP_STACKSIZE']
    print("\x1b[0;31;40mUnset OMP_STACKSIZE, GOMP_STACKSIZE, KMP_STSCKSIZE environment variables to avoid annoying warnings.\x1b[0m")
except:
    print("\x1b[0;31;40mCould not unset annoying environment variables.\x1b[0m")


####################################################################################################
# append further module directories
####################################################################################################

# under Linux
if os.path.exists('/home/giantmolecularcloud/modules'):
    sys.path.append('/home/giantmolecularcloud/modules')
# under macOS
elif os.path.exists('/Users/giantmolecularcloud/modules'):
    sys.path.append('/Users/giantmolecularcloud/modules')
else:
    print("\x1b[0;31;40mCould not find module directory. Please add manually.\x1b[0m")


####################################################################################################
# astropy
####################################################################################################

try:
    from astropy.io import fits
    from astropy.coordinates import Angle
    from astropy.coordinates import SkyCoord
    from astropy import units as u
    from astropy import constants as const
    from astropy.wcs import WCS
    from astropy.io.misc import fnpickle
    from astropy.io.misc import fnunpickle
    from astropy.utils.console import ProgressBar
except:
    print("\x1b[0;31;40mCould not import astropy.\x1b[0m")


####################################################################################################
# matplotlib
####################################################################################################

try:
    import matplotlib as mpl
    # under Linux
    # Keep matplotlib not interactive by default in my servers but allow to enable it by setting an
    # environment variable. For jupyter notebooks no backend must be set!
    if os.path.exists('/home/giantmolecularcloud'):
        if 'MPL_INTERACTIVE' in os.environ:
            if str(os.environ['MPL_INTERACTIVE']) in ['TRUE','True','true']:
                mpl.use('Qt5Agg')
                import matplotlib.pyplot as plt
                plt.ion()
                print("\x1b[0;31;40mEnabled interactive matplotlib plotting!\x1b[0m")
            if str(os.environ['MPL_INTERACTIVE']) in ['jupyter','Jupyter','JUPYTER']:
                import matplotlib.pyplot as plt
                print("\x1b[0;31;40mKeep ipython setting %matplotlib widget!\x1b[0m")
            else:
                mpl.use('pdf')
                import matplotlib.pyplot as plt
                print("\x1b[0;31;40mNon-interactive matplotlib session!\x1b[0m")
        else:
            mpl.use('pdf')
            import matplotlib.pyplot as plt
            print("\x1b[0;31;40mNon-interactive matplotlib session!\x1b[0m")
    # under macOS
    elif os.path.exists('/Users/giantmolecularcloud'):
        mpl.use('Qt5Agg')
        import matplotlib.pyplot as plt
        plt.ion()
        print("\x1b[0;31;40mEnabled interactive matplotlib plotting!\x1b[0m")

    from matplotlib.ticker import MultipleLocator
    from matplotlib import rc
    rc('text',usetex=True)          # always use TeX
    from matplotlib.gridspec import GridSpec
    A4_inches = (8.267,11.692)
    mpl.rcParams['figure.max_open_warning'] = -1
    import matplotlib.colors as colors
    import matplotlib.cm as cm
except:
    print("\x1b[0;31;40mCould not import matplotlib block.\x1b[0m")


####################################################################################################
# astro plotting
####################################################################################################

try:
    import aplpy
    import easy_aplpy                   # my newer plotting code
    import aplpy_plotting as ap         # my old plotting code
except:
    print("\x1b[0;31;40mCould not import astro plotting.\x1b[0m")


####################################################################################################
# analysis
####################################################################################################

try:
    from spectral_cube import SpectralCube
    from spectral_cube import Projection
except:
    print("\x1b[0;31;40mCould not import analysis block.\x1b[0m")


####################################################################################################
# import fits convenience class
####################################################################################################

try:
    from fitsimage.fitsimage import fitsimage
except:
    print("\x1b[0;31;40mCould not import fitsimage class.\x1b[0m")


####################################################################################################
# turn off annoying warnings
####################################################################################################

try:
    from matplotlib.cbook import MatplotlibDeprecationWarning
    import warnings
    warnings.simplefilter('ignore', MatplotlibDeprecationWarning)
    warnings.filterwarnings(action='ignore', category=UserWarning, module='matplotlib')

    np.warnings.filterwarnings('ignore', r'All-NaN slice encountered')
    np.warnings.filterwarnings('ignore', r'All-NaN axis encountered')
    np.warnings.filterwarnings('ignore', r'invalid value encountered in greater_equal')

except:
    print("\x1b[0;31;40mCould not disable annoying warnings.\x1b[0m")


####################################################################################################
# other stuff
####################################################################################################

# default bbox for matplotlib
props   = {'boxstyle': "round", 'facecolor': "w", 'edgecolor': "black", 'linewidth': 0.5, 'alpha': 0.8}


####################################################################################################
# functions
####################################################################################################

try:
    from python_helpers import *
    print("\x1b[0;31;40mImported GiantMolecularCloud python_helpers.\x1b[0m")
except:
    print("\x1b[0;31;40mCould not import GiantMolecularCloud python_helpers.\x1b[0m")


####################################################################################################
# set some default dirctories for my projects
####################################################################################################

# under Linux
if os.path.exists('/home/giantmolecularcloud'):
    basescriptdir = '/home/giantmolecularcloud/scripts/'
    baseplotdir   = '/home/giantmolecularcloud/plots/'
# under macOS
elif os.path.exists('/Users/giantmolecularcloud'):
    basescriptdir = '/Users/giantmolecularcloud/scripts/'
    baseplotdir   = '/Users/giantmolecularcloud/plots/'


####################################################################################################
