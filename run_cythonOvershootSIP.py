#
#  run_cythonOU.py 
#  cythonOU
#
#  Created by nicain on 5/18/10.
#  Copyright (c) 2010 __MyCompanyName__. All rights reserved.
#

################################################################################
# Preamble:
################################################################################

# Import necessary packages:
from subprocess import call as call
import os
import pylab as pl
import pbsTools as pt

# Compile cython extension cythonOU.pyx:
call('python setup.py build_ext --inplace', shell=True)

################################################################################
# Call the main function, as an example:
################################################################################

# pbsTools settings:
nodes = 12          # Product of this...
procsPerNode = 8    #   and this is the number of theta vals
repsPerProc = 1
outputDir = '.batchSimResults'
runLocation = 'local'
runType = 'batch'
waitForSims = 0
wallTime = 10000
dryRun = 1
queue = 'default'
wallTimeEstCount = 3

# Job-location dependent
quickNameSuffix = os.environ['JOBLOCATION']
if quickNameSuffix != 'Hyak':
	pythonPath = ''
else:
	pythonPath = '/usr/lusers/nicain/epd-7.0-2-rh5-x86_64/bin/'

# Settings
nSims = 500
thetaMin, thetaMax, thetaN = 1,300,nodes*procsPerNode # integershere! 101, divide among jobs
maxY=245
N = 240
dt = .01
corr = .15
Coh = 6.4

# Initialize
rP = 40 + .4*Coh
rN = 40 - .4*Coh
thetaVals = pl.linspace(thetaMin,thetaMax,thetaN)


# Create the settings dictionary:
settingsDict = {}
for i in range(1,len(thetaVals)+1):
    settingsDict[i] = [rP,rN,corr,N,thetaVals[i],dt,nSims,maxY]

# Write out settings file:
settingsFileName = os.path.join(os.getcwd(),'jobSettings.settings')
pt.pickle(settingsDict, saveFileName = settingsFileName)

# Run PBS Job
pt.runPBS(pythonPath + 'python cythonOvershootSlave.py $ID',
          fileList = ['cythonOvershootSlave.py', settingsFileName, 'cythonOvershootSIP.so'],
          nodes=nodes,
          ppn=procsPerNode,
		  repspp=repsPerProc,
		  outputDir=outputDir,
          runLocation=runLocation,
		  runType=runType,
		  waitForSims=waitForSims,
          wallTime=wallTime,
		  dryRun=dryRun,
		  queue=queue,
		  wallTimeEstCount=wallTimeEstCount)


















