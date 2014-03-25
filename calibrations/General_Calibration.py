"""
Recalibration of useBrightes, backgrounds, shutter times, subaps locations
and reference centroids.

Author: Nicolas S. Dubost
        nsdubost@uc.cl
Last update: March 20, 2014
"""

#!/usr/bin/env python
import FITS
import darc
import numpy
import pylab
import random
from BeagleDarc.Controller import Controller
from BeagleDarc.Model import Camera
from BeagleDarc.Model import Star

class General_Calibration:
    def __init__(self,cameraName):
        '''
        INPUT
        cameraName       [string]
        '''
        #Darc Controller instance
        c = darc.Control(cameraName)
        #Beagle Controller instance
        bbbc = Controller()
        #Darc camera instance
        SHCamera = Camera('camera')

        #Parameters
        niter = int(5)
        finalniter = int(10)
        slopeniter = int(10)
        nsubaps = SHCamera.nsubaps*2                                # number of active subaps(208*2)
        nstars = SHCamera.nstars                                    # number of stars
        maxShutter = float(SHCamera.max_shutter)                    # maximum shutter time. when shutter time is set outside
                                                                    # the range [0:4095] it is taken as the modulus of tShutter/4095
        SHsat = float(SHCamera.saturation)                          # SH saturation value
        cameraName = SHCamera.camera
        shutter = maxShutter

        #Auxiliary arrays & variables                               
        cent = numpy.zeros([niter,nsubaps])
        centx = 0.0
        centy = 0.0
        #bgImage = c.SumData("rtcPxlBuf",1,"f")[0]
        #auxImage = bgImage
        #auxImageMax = numpy.amax(auxImage)

    def Set_useBrightest(self):
        '''
        #1- Setting useBrightest, loaded from the config. file.
        '''
        
        c.Set('useBrightest',SHCamera.usebrightest)
        
    def find_useBrightest(self):
        bgImage_fwShutter_calibration(1)
        subap_calibration(1)
        hardniter = 200
        nBrightest = 100                                    # range of values
                                                            # to test
        noise = numpy.zeros(nBrightest)
        cameraName = 'SH'
        frames = numpy.zeros([hardniter,nsubaps])
        bbbc.star_on(1)
        for i in range(0,nBrightest):
            print '\nRecording with useBrightest:%3.0f ' %i
            c.Set('useBrightest',-i)
            cent = c.GetStreamBlock(cameraName+'rtcCentBuf',hardniter)   # hardniter frames - as a dict
            cent = cent[cent.keys()[0]]
            for j in range(0,hardniter):
                frames[j,:] = cent[j][0]
            centx2 = numpy.square(frames[:,::2])
            centy2 = numpy.square(frames[:,1::2])
            noise[i] = ((centx2+centy2).sum(0)/float(hardniter)).sum(0)/float(nsubaps)       #

        print noise.argmin(0)
        c.Set('useBrightest',-float(noise.argmin(0)))
        SHCamera.usebrightest = -float(noise.argmin(0))
        pylab.plot(noise)
        pylab.show()
        
        bbbc.star_off(1)
        FITS.Write(noise.astype(numpy.float32),'noise_vs_useBrightest.fits')

    def find_slope_niter():
        stream = 'rtcCentBuf'
        threshold = 1.0
        for star_id in range(1,1+nstars):
            star = Star(star_id)
            ok = star.setup(SHCamera)
            if(ok):
                slope_niter = find_niter(stream,threshold)
                if(slope_niter[0] != -1):
                    star.slope_iter = slope_niter[0]
                    FITS.Write(slope_niter[1],SHCamera.rawdata_path + 'SH_slopes_noscreen_led_%d.fits'%(star_id),writeMode='a')
                else:
                    print 'Relax threshold'
                             
    def find_bg_niter():
        stream = 'rtcPxlBuf'
        threshold = 10
        c.Set('fwShutter',SHCamera.maxshutter)
        bg_niter = find_niter(stream,threshold)
        if(bg_iter[0] != -1):
            SHCamera.bg_niter = bg_niter[0]
            FITS.Write(bg_niter[1],SHCamera.rawdata_path + 'SH_bgImage_shutter_%d.fits'%(int(SHCamera.maxshutter)),writeMode='a')
        else:
            print 'Relax threshold'
        

    def find_niter(self,stream, threshold):
        '''
        Finds and store (with Norman's help) a reasonable number of
        iterations to use when grabbing slopes or backgrounds. 
        The result is as small as possible given a wanted variance 
        under 1 pxl for slopes.

        INPUT
        stream[str]            Name of the darc stream for which you
                               want to find the correct number of iterations
        
        threshold[float]       Threshold under which you want the noise
                               of your system to be (variance).
        '''
        harniter = 10000
        subniter = 200
        threshold = float(threshold)
        slopes = numpy.zeros([hardniter,nsubaps])
        runningnoise = numpy.zeros(subniter)
        found = False
        index_found = 0
        
        print 'Stream Block Acquisition'
        cent = c.GetStreamBlock(cameraName+'rtcCentBuf',hardniter)   # hardniter frames - as a dict
        print 'Extracting data'
        cent = cent[cent.keys()[0]]
        for j in range(0,hardniter):
            slopes[j,:] = cent[j][0]
        
        print 'Reducing data'
        for n in numpy.arange(1,subniter+1):
            runningnoise[n-1] = running_var(slopes,0,n)
            if(runningnoise<=threshold and not(found)):
                found = True
                index_found = n
            
        if(found):
            return [index_found, slopes]
        else:
            return -1
            print 'Number of iterations not found'

    def running_var(self,data,axis,n):
        '''
        Shuffles data and calculates the mean along the specified axis.
        The mean is calculated for sets of n samples. The variance is 
        calculated upon the resulting set of mean numbers. If data is
        2-dimensional the output is the maximum resulting value.
       
        INPUT
        data[numpy array]            Array of up to 2 dimensions
        axis[int]
        n[int]        

        OUTPUT
        var[numpy float]
        '''
        # First we shuffle in the axis direction
        if(axis==1):
            data = numpy.transpose(data)
       
        shape = numpy.shape(data)
        if(numpy.shape(shape)[0]==1):
            data = data.reshape((numpy.shape(data)[0],1))
            
        elif(numpy.shape(shape)[0]>2):
            raise DimError('data has more than 2 dimensions')

        large = int(numpy.shape(data)[0]/n)
        data = data[0:large,:]
        shape = numpy.shape(data)
        means = numpy.zeros((large,shape[1]))
            
        for i in numpy.arange(0,shape[1]):
            numpy.random.shuffle(data[:,i])
            for j in numpy.arange(0,large):
                means[j,i] = numpy.mean(data[j*n:(j+1)*n,i])
        return numpy.amax(numpy.var(means,0))
            

    def bgImage_fwShutter_calibration(self,star_id):
        '''
        Determines, sets and save the bgImage for star_id. fwShutter is
        saved on the files name.
        INPUT
        star_id[int]
        '''
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
        FITS.Write(bgImage,'/home/dani/BeagleAcquisition/SH/BG/SH_bg_led_%d_shutter_%d.fits'%(star_id,int(shutter)),writeMode='a') #  From config file
    
    def subap_calibration(self,star_id):
        '''
        Calibrates the subaps location for star_id
        using an existing subap location. Finds reference
        centroids.
        INPUT
        star_id[int]
        '''
        #4- Subaps
        bbbc.star_on(star_id)
        try:
            subapLocation = FITS.Read('/home/dani/BeagleAcquisition/SH/subapLocation/SH_subapLocation_led_%d.fits'%(star_id))[1] # From config file?
            c.Set('subapLocation',subapLocation)
            c.Set("refCentroids",None)
            cent = c.SumData("rtcCentBuf",slopeniter,"f")[0]/float(slopeniter)
            subapLocation[:,0:1] -= round(cent[::2].mean())
            subapLocation[:,4:5] -= round(cent[1::2].mean())
            FITS.Write(subapLocation,'/home/dani/BeagleAcquisition/SH/SH_subapLocation_led_%d.fits'%(star_id),writeMode='a') # From config file?

            #5- Ref Cent
            c.Set('subapLocation',subapLocation)
            cent = c.SumData("rtcCentBuf",slope,"f")[0]/float(slopeniter)
            FITS.Write(cent.astype(numpy.float32),'/home/dani/BeagleAcquisition/SH/RefCent/SH_RefCent_led_%d.fits'%(star_id))  # From config file?
        except Exception:
            print 'No subaps for led_%d'%(star_id)
        bbbc.star_off(star_id)

    def routine_calibration(self):
        '''
        Calibrates useBrightest, backgrounds, shutter times,
        subap locations and reference centroids for all stars
        '''
        #Main loop. Calibrates for each star
        Set_useBrightest()
        for star_id in range(1,nstars+1):
            print '\nCalibrating star:%3.0f ' %star_id
            bgImage_fwShutter_calibration(star_id)
            subap_calibration(star_id)
            
            
    
