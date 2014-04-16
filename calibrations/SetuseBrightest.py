'''
Finds the useBrightest parameter producing the lowest slope noise

Author: Nicolas S. Dubost
        nsdubost@uc.cl
Last update: March 18, 2014
'''

#!/usr/bin/env python
import FITS
import darc
import numpy
import pylab

from BeagleDarc.Controller import Controller

#Darc Controller instance
c = darc.Control("SH")
#Beagle Controller instance
bbbc = Controller()

# funcion de prender led que setee bg, refs, subaps y todo
# con el shutter correcto. Si todo ya esta seteado y la GUI ya prendio el led,
# entonces no-problemo
# c.Set("refCentroids",None)
niter = 100
nsubaps = 416                                               # number of subaps
nBrightest = 100                                            # range of values
                                                            # to test
noise = numpy.zeros(nBrightest)
cameraName = 'SH'
frames = numpy.zeros([niter,nsubaps])
for i in range(0,nBrightest):
    print '\nRecording with useBrightest:%3.0f ' %i
    c.Set('useBrightest',-i)
    cent = c.GetStreamBlock(cameraName+'rtcCentBuf',niter)   # niter frames - as a dict
    cent = cent[cent.keys()[0]]
    for j in range(0,niter):
        frames[j,:] = cent[j][0]
    centx2 = numpy.square(frames[:,::2])
    centy2 = numpy.square(frames[:,1::2])
    noise[i] = ((centx2+centy2).sum(0)/float(niter)).sum(0)/float(nsubaps)       #

print noise.argmin(0)
c.Set('useBrightest',-float(noise.argmin(0)))
pylab.plot(noise)
pylab.show()

FITS.Write(noise.astype(numpy.float32),'noise_vs_useBrightest.fits')







