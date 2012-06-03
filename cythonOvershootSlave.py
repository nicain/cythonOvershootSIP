#
#  DDMCube_Slave.py
#  DDMCubeTeraGrid
#
#  Created by nicain on 4/29/10.
#  Copyright (c) 2010 __MyCompanyName__. All rights reserved.
#

################################################################################
# Preamble
################################################################################

# Import packages:
from cythonOvershootSIP import getOvershootDist
import pbsTools as pt
import pylab as pl
import sys
import time

# Grab the settings from the file:
settingsDict = pt.getFromPickleJar(loadDir = './', fileNameSubString = '.settings')[0]

# Grab the index for the current job:
thetaInd = int(sys.argv[1])

# Write down the settings for the job:
rP, rN, corr, N, theta, dt, nSims, maxY = settingsDict[thetaInd]

# Run the sim, recovering monte carlo data:
tic = time.time()
overShootTemp = getOvershootDist(rP, rN, corr, N, theta-.01, dt, nSims)
print time.time()-tic, 'sec Elapsed'

# Make the histogram:
bins = range(0,maxY)
overShootPref = overShootTemp[overShootTemp>0]-theta
mean = overShootPref.mean()
overShootHist, bin_edges = pl.histogram(overShootPref,bins=bins)
overShootHist = overShootHist*1.0/overShootHist.sum()

# Save output:
pt.pickle((overShootHist,mean),saveFileName = 'simResults_' + str(theta) + '.dat')



