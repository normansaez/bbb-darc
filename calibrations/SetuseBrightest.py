#!/usr/bin/env python
import FITS
import darc
import numpy
import pylab

c=darc.Control("ShackHartmann")
# funcion de prender led que setee bg, refs, subaps y todo
# con el shutter correcto
c.Set("refCentroids",None)
niter = 200
nsubaps = 500                                               # number of subaps
nBrightest = 100                                            # range of values
                                                            # to test
noise = numpy.zeros(nBrightest)
for i in range(1,nBrightest+1)
    c.Set('useBrightest',-i)
    cent = c.GetStreamBlock(cameraName+'rtcCentBuf',niter)   # niter frames - as a list
    centx2 = numpy.square(cent[:,::2])
    centy2 = numpy.square(cent[:,1::2])
    noise[i] = ((centx+centy).sum(0)/float(niter)).sum(0)/float(nsubaps)       # 

c.Set('useBrightest',noise.argmin(0))
print noise.argmin(0)
pylab.plot(noise)
pylab.show()

FITS.Write(cent.astype(numpy.float32),'cent_led_1.fits')







