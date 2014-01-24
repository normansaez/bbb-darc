#!/usr/bin/env python
import FITS
import darc
import numpy
import pylab

c=darc.Control("ShackHartmann")
niter = 5000 
cent = c.GetStreamBlock(cameraName+'rtcCentBuf',niter)   # niter frames - as a list
FITS.Write(cent.astype(numpy.float32),'Slopes_Noise.fits')
pylab.plot(cent)
pylab.show()






