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
niter = float(100)
finalniter = float(1000)
nsubaps = 416                                               # number of subaps
nstars = 53                                                 # number of stars
maxShutter = float(4095)                                    # maximum shutter time
SHsat = float(65532)                                        # SH saturation value
cameraName = 'ShackHartmann'
shutter = maxShutter

#Auxiliary arrays                                    
cent = numpy.zeros([niter,nsubaps])
bgImage = c.SumData("rtcPxlBuf",1,"f")[0]
auxImage = bgImage
auxImageMax = numpy.amax(auxImage)

#1- Setting useBrightest, as found with ~/bbb-darc/calibrations/SetuseBrightest.py
c.Set('useBrightest',-85)

#Main loop. Calibrates for each star
for star_id in range(1,nstars+1):
    print '\nCalibrating star:%3.0f ' %star_id
    #2-3 bgImage & fwShutter iteration
    auxImageMax = SHsat/float(3)                            # /3 so that the while condition is true
    shutter = maxShutter/float(6)                           # /6 so that in the first iteration shutter = maxShutter*0.3
    while(numpy.absolute(auxImageMax/SHsat-0.6)>0.1):
        shutter = shutter*(SHsat*float(0.6))/auxImageMax
        c.Set('bgImage',None)
        c.Set('fwShutter',int(shutter))
        bgImage = c.SumData('rtcPxlBuf',niter,'f')[0]/niter
        c.Set('bgImage',bgImage)
        bbbc.star_on(star_id)
        auxImage = c.SumData('rtcPxlBuf',niter,'f')[0]/niter
        bbbc.star_off(star_id)
        auxImageMax = amax(auxImage)
    
    shutter = shutter*(SHsat*float(0.6))/auxImageMax
    c.Set('bgImage',None)
    c.Set('fwShutter',int(shutter))
    bgImage = c.SumData('rtcPxlBuf',finalniter,'f')[0]/finalniter

    #Saving values found
    FITS.Write(bgImage,'/home/dani/BG/bg_led_%d_shutter_%d.fits'%(star_id,int(shutter)),writeMode='a')

    #4- Subaps
    c.Get('subapLocation')

    #5- Ref Cent
    bbbc.star_on(star_id)
    c.Set("refCentroids",None)
    cent = c.SumData("rtcCentBuf",finalniter,"f")[0]/finalniter
    FITS.Write(cent.astype(numpy.float32),'/home/dani/RefCent/cent_led_%d.fits'%(star_id))
    bbbc.star_off(star_id)


###############################
###############################
###############################


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
