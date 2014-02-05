#!/usr/bin/env python
import FITS
import darc

c=darc.Control("ShackHartmann")
bg = c.Get("bgImage")

niter = 1000
bg=c.SumData("rtcPxlBuf",niter,"f")[0]/float(niter)
c.Set("bgImage", bg)
FITS.Write(bg,'bg_led_1.fits',writeMode='a')
print bg.max(), bg.min()

