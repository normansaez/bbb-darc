#!/usr/bin/env python
import FITS
import darc
import numpy

c=darc.Control("ShackHartmann")
#cent = c.Get("refCentroids")
c.Set("refCentroids",None)
niter = 14
cent = c.SumData("rtcCentBuf",niter,"f")[0]/float(niter)
print cent.max(), cent.min()
c.Set("refCentroids", cent)
FITS.Write(cent.astype(numpy.float32),'cent_led_1.fits')

