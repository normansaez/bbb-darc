"""
Recalibration of useBrightes, backgrounds, shutter times, subaps locations
and reference centroids.

Author: Nicolas S. Dubost
        nsdubost@uc.cl
Last update: March 14, 2014
"""

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
finalniter = int(100)
nsubaps = 416                                               # number of active subaps
nstars = 53                                                 # number of stars
maxShutter = float(4095)                                    # maximum shutter time. when shutter time is set outside
                                                            # the range [0:4095] it is taken as the modulus of tShutter/4095
SHsat = float(65532)                                        # SH saturation value
cameraName = 'SH'
shutter = maxShutter

#Auxiliary arrays & variables                               
cent = numpy.zeros([finalniter,nsubaps])
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
    bgImage = c.SumData('rtcPxlBuf',niter*2,'f')[0]/float(niter*2)
    c.Set('bgImage',bgImage)

    #4- Subaps
    bbbc.star_on(star_id)
    try:
        subapLocation = FITS.Read('/home/dani/BeagleAcquisition/SH/subapLocation/SH_subapLocation_led_%d.fits'%(star_id))[1]
        c.Set('subapLocation',subapLocation)
        c.Set("refCentroids",None)
        centroids = c.GetStreamBlock(cameraName+'rtcCentBuf',finalniter)
        print 'Adquirio el StreamBlock'
        centroids = centroids[centroids.keys()[0]]
        print 'Extrajo la lista del diccionario'
        for j in range(0,finalniter):
            cent[j,:] = centroids[j][0]
        print 'Reconstruyo la matriz'
        cent = numpy.square(cent)
        print 'Todo al cuadrado'
        cent2 = numpy.sqrt(cent[:,::2]+cent[:,1::2])
        print 'Sumo y saco raiz'
        cent2 = numpy.var(cent2,0)
        print 'Varianza hecha'
        pylab.plot(cent2)
        print 'Primer comando de plot'
        pylab.show()
        print 'Segundo comando de plot'
        oli = raw_input('Press any key to conitnue to the next star:_ ')
        print 'Pidio un raw_input'

    except Exception:
        print 'No subaps for led_%d'%(star_id)
    bbbc.star_off(star_id)
        
