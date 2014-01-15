#!/usr/bin/env python
import FITS
import darc
import numpy

c=darc.Control("ShackHartmann")
#cent = c.Get("refCentroids")
# setear centroides de referencia on-axis c.Set("refCentroids",None)
niter = 500
cent = c.GetStreamBlock(cameraName+'rtcPxlBuf',niter)#niter frames - as a list

FITS.Write(cent.astype(numpy.float32),'cent_led_1.fits')

