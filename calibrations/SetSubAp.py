#!/usr/bin/env python
import FITS
import darc
import sys

if __name__ == '__main__':
    led = None
    subapLocation = None
    try:
        led = sys.argv[1]
    except:
        print "\nA number of led is needed as argument!\nexample\npython %s 1" % __file__
        sys.exit(-1)
    c=darc.Control("SH")
    try:
        subapLocation = FITS.Read("/home/dani/git/canaryLaserCommissioning/SHsubapLocation_led%d.fits"% (int(led)))[1].astype("f")
    except:
        print "THIS FILE DOESN'T EXISTS:\n%s" %("/home/dani/git/canaryLaserCommissioning/SHsubapLocation_led%d.fits"% (int(led)))
        sys.exit(-1)        
    c.Set("subapLocation",subapLocation)

