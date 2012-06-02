#  cythonOvershootSIP.pyx 
#  Created by nicain on 5/31/12.

################################################################################
# Preamble: 
################################################################################

# Import floating point division from python 3.0
from __future__ import division

# Import necessary python packages:
import random, uuid
import numpy as np
cimport numpy as np
cimport cython

# Compile-time type initialization for numpy arrays:
ctypedef np.float_t DTYPE_t    

################################################################################
# Useful C++ functions:
################################################################################

# Wrapper for the RNG:
cdef extern from "MersenneTwister.h":
    ctypedef struct c_MTRand "MTRand":
        double randDblExc()
        void seed( unsigned long bigSeed[])

# External math wrapper functions that might be needed:
cdef extern from "math.h":
    float fabs(float absMe)        # Unused in this file, but can't hurt!
    


################################################################################
# OU Process simulator:
################################################################################
@cython.boundscheck(False)
def getOvershootDist(
            float rP,
            float rN,
            float corr,
            int N,
            float theta,
            float dt,  
            int nSims):

    ################################################################################
    # Initializations:
    ################################################################################    

    # C initializations
    cdef float t, cumSum
    cdef int i, currN
    
    # RNG initializations:
    cdef unsigned long mySeed[624]        # Seed array for the RNG, length 624
    cdef c_MTRand myTwister                # RNG object construction
    
    # numpy array initializations:
    DTYPE = np.float                    # Initialize a data-type for the array
    cdef np.ndarray[DTYPE_t, ndim=1] overShoot = np.zeros(nSims, dtype=DTYPE) 
    
    # Initialization of random number generator:
    myUUID = uuid.uuid4()
    random.seed(myUUID.int)
    for i in range(624): mySeed[i] = random.randint(0,2**30)                 
    myTwister.seed(mySeed)

    ################################################################################
    # Simulation:
    ################################################################################

    for i in range(nSims):
        
        # Initilize DDM
        t = 0
        cumSum = 0
        while fabs(cumSum) < theta:
            
            # Increment time
            t += dt
            
            # Pref population:
            if myTwister.randDblExc() < dt*rP*.001*corr:
                cumSum += N
            else:
                for currN in range(N):
                    if myTwister.randDblExc() < dt*rP*.001*(1-corr):
                        cumSum += 1
            
            # Null population:
            if myTwister.randDblExc() < dt*rN*.001*corr:
                cumSum -= N
            else:
                for currN in range(N):
                    if myTwister.randDblExc() < dt*rN*.001*(1-corr):
                        cumSum -= 1

        overShoot[i] = cumSum
    
    return overShoot















