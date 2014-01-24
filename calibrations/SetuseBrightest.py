#!/usr/bin/env python
import FITS
import darc
import numpy
import pylab

c=darc.Control("ShackHartmann")
# funcion de prender led que setee bg, refs, subaps y todo
# con el shutter correcto. Si todo ya esta seteado y la GUI ya prendio el led,
# entonces no-problemo
# c.Set("refCentroids",None)
niter = 100
nsubaps = 416                                               # number of subaps
nBrightest = 100                                            # range of values
                                                            # to test
noise = numpy.zeros(nBrightest)
cameraName = 'ShackHartmann'
frames = numpy.zeros([niter,nsubaps])
for i in range(1,nBrightest+1):
    print '\nRecording with useBrightest:%3.0f ' %i
    c.Set('useBrightest',-i)
    cent = c.GetStreamBlock(cameraName+'rtcCentBuf',niter)   # niter frames - as a dict
    cent = cent[cent.keys()[0]]
    for j in range(0,niter):
        frames[j,:] = cent[j][0]
    centx2 = numpy.square(frames[:,::2])
    centy2 = numpy.square(frames[:,1::2])
    noise[i] = ((centx2+centy2).sum(0)/float(niter)).sum(0)/float(nsubaps)       #

c.Set('useBrightest',noise.argmin(0))
print noise.argmin(0)
pylab.plot(noise)
pylab.show()

FITS.Write(noise.astype(numpy.float32),'noise_vs_useBrightest.fits')







