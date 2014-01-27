#!/usr/bin/env python
import FITS
import darc
import numpy
import pylab

c=darc.Control("ShackHartmann")
niter = 5000
nsubaps = 416                                            
c.Set('useBrightest',-85)
                                          
cameraName = 'ShackHartmann'
frames = numpy.zeros([niter,nsubaps])

cent = c.GetStreamBlock(cameraName+'rtcCentBuf',niter)   # niter frames - as a dict
cent = cent[cent.keys()[0]]
for j in range(0,niter):
    frames[j,:] = cent[j][0]

#pylab.plot(noise)
#pylab.show()

FITS.Write(frames.astype(numpy.float32),'static_slope_noise.fits')







