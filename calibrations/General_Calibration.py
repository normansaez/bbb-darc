#!/usr/bin/env python
import FITS
import darc
import numpy
import pylab
from BeagleDarc.Controller import Controller

#Darc Controller instance
c=darc.Control("ShackHartmann")
#Beagle Controller instance
bbbc = Controller.__init__()

#Parameters
niter = 100
finalniter = 1000
nsubaps = 416                                               # number of subaps
nBrightest = 100                                            # range of values
nstars = 53                                                 # number of stars
maxshutter = 4095                                           # maximum shutter time
SHsat = 65532                                               # SH saturation value
cameraName = 'ShackHartmann'

#Auxiliary arrays                                    
cent = numpy.zeros([niter,nsubaps])
bgImage = c.SumData("rtcPxlBuf",1,"f")[0]

#1- Setting useBrightest, as found with ~/bbb-darc/calibrations/SetuseBrightest.py
c.Set('useBrightest',-85)

#Main loop. Calibrates for each star
for star_id in range(1,nstars):
    bbbc.star_on(star_id)
    

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







#!/usr/bin/env python
import FITS
import darc

c=darc.Control("ShackHartmann")
bg = c.Get("bgImage")

niter = 100
bg=c.SumData("rtcPxlBuf",niter,"f")[0]/float(niter)
c.Set("bgImage", bg)
FITS.Write(bg,'bg_led_1.fits',writeMode='a')

#!/usr/bin/env python
import FITS
import darc
import numpy

c=darc.Control("ShackHartmann")
#cent = c.Get("refCentroids")
c.Set("refCentroids",None)
niter = 100
cent = c.SumData("rtcCentBuf",niter,"f")[0]/float(niter)
print cent.max(), cent.min()
c.Set("refCentroids", cent)
FITS.Write(cent.astype(numpy.float32),'cent_led_1.fits')

