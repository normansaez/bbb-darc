#!/usr/bin/env python
import FITS
import darc
import numpy
import pylab
from BeagleDarc.Controller import Controller

#Darc Controller instance
c = darc.Control("SH")
#Beagle Controller instance
bbbc = Controller()

#Parameters
niter = int(5)
finalniter = int(10)
nsubaps = 416                                               # number of active subaps
nstars = 53                                                 # number of stars
maxShutter = float(4095)                                    # maximum shutter time. when shutter time is set outside
                                                            # the range [0:4095] it is taken as the modulus of tShutter/4095
SHsat = float(65532)                                        # SH saturation value
cameraName = 'SH'
shutter = maxShutter

#Auxiliary arrays & variables                               
cent = numpy.zeros([niter,nsubaps])
centx = 0.0
centy = 0.0
bgImage = c.SumData("rtcPxlBuf",1,"f")[0]
auxImage = bgImage
auxImageMax = numpy.amax(auxImage)

#1- Setting useBrightest, as found with ~/bbb-darc/calibrations/SetuseBrightest.py
c.Set('useBrightest',-85)

#Main loop. Calibrates for each star
for star_id in range(1,nstars+1):
    print '\nCalibrating star:%3.0f ' %star_id
    #2-3 bgImage & fwShutter iteration
    shutter = maxShutter*0.3
    print 'shutter: ',
    print shutter
    c.Set('bgImage',None)
    c.Set('fwShutter',int(shutter))
    bgImage = c.SumData('rtcPxlBuf',niter,'f')[0]/float(niter)
    c.Set('bgImage',bgImage)
    bbbc.star_on(star_id)
    auxImage = c.SumData('rtcPxlBuf',niter,'f')[0]/float(niter)
    bbbc.star_off(star_id)
    auxImageMax = numpy.amax(auxImage)

    while(numpy.absolute(auxImageMax/SHsat-0.6)>0.05):
        # The while condition is set so that the maximum value found in the image
        # is around 60% of the saturation value
        shutter = shutter*(SHsat*float(0.6))/auxImageMax
        if(shutter>maxShutter):
            # Protection
            shutter = maxShutter
        c.Set('bgImage',None)
        print 'auxImageMax: ',
        print auxImageMax
        print "shutter: ",
        print shutter
        c.Set('fwShutter',int(shutter))
        bgImage = c.SumData('rtcPxlBuf',niter,'f')[0]/float(niter)
        c.Set('bgImage',bgImage)
        bbbc.star_on(star_id)
        auxImage = c.SumData('rtcPxlBuf',niter,'f')[0]/float(niter)
        bbbc.star_off(star_id)
        auxImageMax = numpy.amax(auxImage)
        if(shutter>=maxShutter):
            # Escape while
            auxImageMax = SHsat*0.6
    
    c.Set('bgImage',None)
    bgImage = c.SumData('rtcPxlBuf',finalniter,'f')[0]/float(finalniter)
    c.Set('bgImage',bgImage)

    #Saving values found
    FITS.Write(bgImage,'/home/dani/BG/SH_bg_led_%d_shutter_%d.fits'%(star_id,int(shutter)),writeMode='a')

    #4- Subaps
    bbbc.star_on(star_id)
    subapLocation = FITS.Read('/home/dani/subapLocation/SH_subapLocation_led_%d.fits'%(star_id))[1]
    c.Set('subapLocation',subapLocation)
    c.Set("refCentroids",None)
    cent = c.SumData("rtcCentBuf",finalniter,"f")[0]/float(finalniter)
    subapLocation[:,0:1] -= round(cent[::2].mean())
    subapLocation[:,4:5] -= round(cent[1::2].mean())
    FITS.Write(subapLocation,'/home/dani/subapLocation/SH_subapLocation_led_%d.fits'%(star_id),writeMode='a')    

    #5- Ref Cent
    c.Set('subapLocation',subapLocation)
    cent = c.SumData("rtcCentBuf",finalniter,"f")[0]/float(finalniter)
    FITS.Write(cent.astype(numpy.float32),'/home/dani/RefCent/SH_RefCent_led_%d.fits'%(star_id))
    bbbc.star_off(star_id)
