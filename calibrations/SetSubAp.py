#!/usr/bin/env python
import FITS
import darc

if __name__ == '__main__':
    c=darc.Control("ShackHartmann")
    subapLocation = FITS.Read("/home/dani/git/canaryLaserCommissioning/ShackHartmannsubapLocation_led0.fits")[1].astype("f")
    #sal = c.Get("subapLocation")
    c.Set("subapLocation", sal)

