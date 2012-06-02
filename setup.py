#
#  setup.py
#  DDMCubeTeraGrid
#
#  Created by nicain on 4/29/10.
#  Copyright (c) 2010 __MyCompanyName__. All rights reserved.
#

# Import necessary commands from packages
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

# Compile the cython extension "cythonOU.pyx"
import numpy as np	# Needed to compile the c numpy extensions correctly
setup(cmdclass = {'build_ext': build_ext},
      ext_modules = [Extension("cythonOvershootSIP", ['cythonOvershootSIP.pyx'],language="c++",include_dirs=[np.get_include()])])

# Do a command-line complie as well; this will generate the cythonOU.html file 
#	 in the home directory, so that we can inspect cython efficiency:
from subprocess import call as call
call('cython -a cythonOvershootSIP.pyx',shell=True)