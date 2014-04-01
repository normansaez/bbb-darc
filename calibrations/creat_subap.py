"""
Creats fits files with the subapLocation array for each valid star

Author: Nicolas S. Dubost
        nsdubost@uc.cl
Last update: April the 1st, 2014 (don't worry, this works)
"""

#!/usr/bin/env python
import FITS
import darc
import numpy
import pylab
import random
from BeagleDarc.Controller import Controller
from BeagleDarc.Model import Camera
from BeagleDarc.Model import Star
import ConfigParser

#Darc Controller instance
c = darc.Control('SH')
#Beagle Controller instance
bbbc = Controller()
#Darc camera instance
SHCamera = Camera('camera')

#Parameters
nsubaps = 16*16                    #Active+Inactive subaps
nstars = SHCamera.nstars
subapLocation = numpy.zeros((nsubaps,6))
subapLocation[:,2] += 1
subapLocation[:,5] += 1
Row = numpy.arange(-5,-5+16)
Xwidth = 42
Ywidth = 39
Xgap = 37
Ygap = 37

for row in range(1,16+1):
    subapLocation[16*(row-1):16*(row),0] = Ygap*(row-1)-round(Ywidth/2)
    subapLocation[16*(row-1):16*(row),1] = subapLocation[16*(row-1):16*(row),0] + Ywidth
    subapLocation[16*(row-1):16*(row),3] = Xgap*Row-round(Xwidth/2)
    subapLocation[16*(row-1):16*(row),4] = subapLocation[16*(row-1):16*(row),3] + Xwidth

#for i in range(32):
#   print subapLocation[i,:]
    

  
