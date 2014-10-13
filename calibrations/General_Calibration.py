"""
Recalibration of useBrightes, backgrounds, exptime times, subaps locations
and reference centroids.

Author: Nicolas S. Dubost
        nsdubost@uc.cl
Last update: October the 13th, 2014
"""

#!/usr/bin/env python
import FITS
import darc
import numpy
import os
from numpy import unravel_index
import pylab
import random
from BeagleDarc.Controller import Controller
from BeagleDarc.Model import Camera
from BeagleDarc.Model import Star
import ConfigParser
import scipy
from scipy import signal
import postprocess as pp

class Calibration:
    def __init__(self,cameraName):
        '''
        INPUT
        cameraName       [string]
        '''
        #Darc Controller instance
        self.c = darc.Control(cameraName)
        #Beagle Controller instance
        self.bbbc = Controller()
        #Darc camera instance
        self.Cam = Camera(cameraName)

        #Parameters
        self.niter = int(5)
        self.finalniter = int(10)
        self.slopeniter = int(10)
        self.nsubaps = int(self.Cam.nsubaps)                             # number of active subaps(208*2)
        self.nsubaps *= 2
        self.nstars = self.Cam.nstars                                    # number of stars
        self.maxexptime = float(self.Cam.maxexptime)                     # maximum exptime time. when exptime time is set outside
                                                                    # the range [0:4095] it is taken as the modulus of tExptime/4095
        self.sat = float(self.Cam.saturation)                          # self.Cam.name saturation value
        self.name = self.Cam.name
        self.exptime = self.maxexptime
        self.majorpattern = None
        self.minorpattern = None

        #Auxiliary arrays & variables
        self.cent = numpy.zeros((self.niter,self.nsubaps))
        self.centx = 0.0
        self.centy = 0.0
        #bgImage = c.SumData("rtcPxlBuf",1,"f")[0]
        #auxImage = bgImage
        #auxImageMax = numpy.amax(auxImage)

    def Set_useBrightest(self):
        '''
        #1- Setting useBrightest, loaded from the config. file.
        '''
        
        #self.c.Set('useBrightest',2*float(self.Cam.usebrightest))
        self.c.Set('useBrightest',0)
        
    def find_useBrightest(self):
        self.bgImage_exptime_calibration(1)
        self.subap_calibration(1)
        hardniter = 100
        nBrightest = 100                                    # range of values
                                                            # to test
        noise = numpy.zeros(nBrightest)
        name = self.Cam.name
        frames = numpy.zeros([hardniter,self.nsubaps])
        self.bbbc.star_on(1)
        for i in range(0,nBrightest):
            print '\nRecording with useBrightest:%3.0f ' %i
            self.c.Set('useBrightest',-i)
            cent = self.c.GetStreamBlock(name+'rtcCentBuf',hardniter)   # hardniter frames - as a dict
            cent = cent[cent.keys()[0]]
            for j in range(0,hardniter):
                frames[j,:] = cent[j][0]
            centx2 = numpy.square(frames[:,::2])
            centy2 = numpy.square(frames[:,1::2])
            noise[i] = ((centx2+centy2).sum(0)/float(hardniter)).sum(0)/float(self.nsubaps)       #

        print noise.argmin(0)
        self.c.Set('useBrightest',-float(noise.argmin(0)))
        self.Cam.usebrightest = -int(noise.argmin(0))
        pylab.plot(noise)
        pylab.show()
        
        self.bbbc.star_off(1)
        #FITS.Write(noise.astype(numpy.float32),'noise_vs_useBrightest.fits')

    def find_slope_niter():
        stream = 'rtcCentBuf'
        threshold = 1.0
        for star_id in range(1,1+nstars):
            star = Star(star_id)
            ok = star.setup(self.Cam)
            if(ok):
                slope_niter = find_niter(stream,threshold)
                if(slope_niter[0] != -1):
                    star.slope_iter = slope_niter[0]
                    FITS.Write(slope_niter[1],self.Cam.rawdata_path + self.Cam.name+'_slopes_noscreen_led_%d.fits'%(star_id),writeMode='a')
                else:
                    print 'Relax threshold'
                             
    def find_bg_niter():
        stream = 'rtcPxlBuf'
        threshold = 10
        c.Set('exptime',self.Cam.maxexptime)
        bg_niter = find_niter(stream,threshold)
        if(bg_iter[0] != -1):
            self.Cam.bg_niter = bg_niter[0]
            FITS.Write(bg_niter[1],self.Cam.rawdata_path + self.Cam.name+'_bgImage_exptime_%d.fits'%(int(self.Cam.maxexptime)),writeMode='a')
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
        cent = self.c.GetStreamBlock(name+stream,hardniter)   # hardniter frames - as a dict
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

    def bgImage_exptime_calibration(self,star_id):
        '''
        Determines, sets and save the bgImage for star_id. exptime is
        saved on the files name.
        INPUT
        star_id[int]
        '''
        #2-3 bgImage & exptime iteration
        star = Star(star_id)
        star.setup(self.Cam)
        exptime = numpy.round(self.initexptime)
        self.c.Set('bgImage',None)
        self.c.Set(self.Cam.exptime,int(exptime))
        bgImage = self.grab('rtcPxlBuf,'self.finalniter) #1313
        self.c.Set('bgImage',bgImage)
        self.bbbc.star_on(star_id)
        auxImage = self.grab('rtcCalPxlBuf',self.finalniter)
        self.bbbc.star_off(star_id)
        auxImageMax = numpy.amax(auxImage)
        print ''
        relativemax = 0.7
        threshold = 0.05

        while(numpy.absolute(auxImageMax/self.sat-relativemax)>threshold):
            # The while condition is set so that the maximum value found in the image
            # is around 60% of the saturation value
            print "exptime: ",
            print exptime
            print 'auxImageMax: ',
            print str(100*auxImageMax/self.sat)+'%'
            exptime = exptime*(self.sat*float(relativemax))/auxImageMax
            if(exptime>=self.maxexptime):
                # Protection
                exptime = self.maxexptime
                auxImageMax = self.sat*relativemax
                self.c.Set(self.Cam.exptime,int(exptime))
            else:
                self.c.Set('bgImage',None)
                self.c.Set(self.Cam.exptime,int(exptime))
                bgImage = self.grab('rtcPxlBuf',self.finalniter)
                self.c.Set('bgImage',bgImage)
                self.bbbc.star_on(star_id)
                auxImage = self.grab('rtcCalPxlBuf',self.finalniter)
                self.bbbc.star_off(star_id)
                auxImageMax = numpy.amax(auxImage)
        
        print "Final exptime: ",
        print exptime
        print 'Final auxImageMax: ',
        print str(100*auxImageMax/self.sat)+'%'
        self.c.Set('bgImage',None)
        bgImage = self.grab('rtcPxlBuf',self.Cam.bg_iter)
        self.c.Set('bgImage',bgImage)
        self.flushAll()
        self.bbbc.star_on(star_id)
        auxImage = self.grab('rtcCalPxlBuf',self.finalniter)
        self.bbbc.star_off(star_id)
        self.c.Set('bgImage',bgImage)
        
        #Saving values found and removing previous values
        files = os.listdir(self.Cam.bg_path)
        files = [s for s in files if 'led_%d_'%(star_id) in s]
        if(files!=[]):
            for file_name in files:
                os.remove(self.Cam.bg_path + file_name)
        FITS.Write(bgImage,self.Cam.bg_path + self.Cam.name+'_bg_led_%d_exptime_%d.fits'%(star_id,int(exptime)),writeMode='w')
        FITS.Write(auxImage.reshape((self.Cam.pxly,self.Cam.pxlx)),self.Cam.bg_path + self.Cam.name+'_aux_led_%d_exptime_%d.fits'%(star_id,int(exptime)),writeMode='w')

    def pupil_location(self,star_id):
        #Parameters
        self.c.Set('bgImage',None)
        allsubaps = self.Cam.allsubaps                    # Active+Inactive subaps
        side = int(numpy.sqrt(allsubaps))
        nstars = self.Cam.nstars
        subapLocation = numpy.zeros((allsubaps,6))             # Centred on (0,0)
        subapLocation[:,2] = subapLocation[:,2] + 1
        subapLocation[:,5] = subapLocation[:,5] + 1

        Xwidth = self.Cam.xwidth
        Ywidth = self.Cam.ywidth
        Xgap = self.Cam.xgap
        Ygap = self.Cam.ygap 

        # Checking for parity
        xRow = numpy.array([])
        if(side%2):
            xRow = numpy.arange(-numpy.ceil(float(side)/2),round(float(side)/2))*Xgap -round(Xwidth/2)
        else:
            xRow = numpy.arange(-float(side)/2,float(side)/2)*Xgap + round(Xgap/2) -round(Xwidth/2)

        yRow = numpy.array([])
        if(side%2):
            yRow = numpy.arange(-numpy.ceil(float(side)/2),round(float(side)/2))*Ygap -round(Ywidth/2)
        else:
            yRow = numpy.arange(-float(side)/2,float(side)/2)*Ygap + round(Ygap/2) -round(Ywidth/2)

        for row in range(1,int(side+1)):
            subapLocation[side*(row-1):side*(row),0] = yRow[row-1]
            subapLocation[side*(row-1):side*(row),1] = subapLocation[side*(row-1):side*(row),0] + Ywidth
            subapLocation[side*(row-1):side*(row),3] = xRow
            subapLocation[side*(row-1):side*(row),4] = subapLocation[side*(row-1):side*(row),3] + Xwidth

        if(self.majorpattern==None):
            self.majorpattern = numpy.zeros((-subapLocation[0,0]+subapLocation[-1,1]+1,-subapLocation[0,3]+subapLocation[-1,4]+1))
            self.minorpattern = numpy.zeros((Ywidth+1,Xwidth+1))
            centx = float(Xwidth+1)/2 - 0.5
            centy = float(Ywidth+1)/2 - 0.5
            fwhm = self.Cam.fwhm
            subapLocAux = subapLocation
            Aux = numpy.zeros((allsubaps,6))
            Aux[:,0:2] = subapLocAux[:,0:2] - subapLocation[0,0]
            Aux[:,3:5] = subapLocAux[:,3:5] - subapLocation[0,3]
            subapflag = FITS.Read(self.Cam.subapflag)[1]
            subapflag = subapflag.ravel()
            
            for y in range(0,Ywidth):
                for x in range(0,Xwidth):
                    self.minorpattern[y,x] = numpy.exp(-(pow(x-centx,2)+pow(y-centy,2))/(2*pow(fwhm/2.35482,2)))
                
            tracker = 0
            for subap in Aux:
                if(int(subapflag[tracker])):
                    self.majorpattern[subap[0]:subap[1]+1,subap[3]:subap[4]+1] += self.minorpattern
                tracker += 1

        patternshape = self.majorpattern.shape
        self.bbbc.star_on(star_id)
        s = Star(star_id)
        #image = self.grab('rtcCalPxlBuf',s.slope_iter)
        image = self.grab('rtcCalPxlBuf',1)
        image = image.reshape((self.Cam.pxly,self.Cam.pxlx))
        correlation = scipy.signal.fftconvolve(image,self.majorpattern,mode='same')
        argmx = numpy.unravel_index(correlation.argmax(),correlation.shape)
        print 'Pupil centre for star %d: '%(star_id),
        print [argmx[1],argmx[0]]
        print subapLocation[5,3]
        subapLocation[:,0:2] += argmx[0]
        subapLocation[:,3:5] += argmx[1]
        print subapLocation[5,3]


        #Saving values found and removing previous values
        files = os.listdir(self.Cam.subaplocation_path)
        files = [st for st in files if 'led_%d.fits'%(star_id) in st]
        if(files!=[]):
            for file_name in files:
                os.remove(self.Cam.subaplocation_path + file_name)
        FITS.Write(subapLocation,self.Cam.subaplocation_path + self.Cam.name+'_subapLocation_led_%d.fits'%(star_id),writeMode='w')

        FITS.Write(image,self.Cam.subaplocation_path + 'image_%d.fits'%(star_id),writeMode='w')
        FITS.Write(correlation,self.Cam.subaplocation_path + 'correlation_%d.fits'%(star_id),writeMode='w')
        FITS.Write(self.majorpattern,self.Cam.subaplocation_path + 'major.fits',writeMode='w')
        FITS.Write(self.minorpattern,self.Cam.subaplocation_path + 'minor.fits',writeMode='w')

        self.bbbc.star_off(star_id)

        subapflag = FITS.Read(self.Cam.subapflag)[1]
        subapflag = subapflag.ravel()
        v = subapflag.argmax()
        print '1st subap centre for star %d: '%(star_id),
        print [v,(subapLocation[v,3]+subapLocation[v,4])/2,(subapLocation[v,0]+subapLocation[v,1])/2]
        
        #return subapLocation
    
    def subap_calibration(self,star_id):
        '''
        Calibrates the subaps location for star_id
        using an existing subap location. Finds reference
        centroids.
        INPUT
        star_id[int]
        '''
        #4- Subaps
        self.bbbc.star_on(star_id)
        s = Star(star_id)
        if(s.valid):
            subapLocation = FITS.Read(self.Cam.subaplocation_path + self.Cam.name+'_subapLocation_led_%d.fits'%(star_id))[1]
            self.c.Set('subapLocation',subapLocation.astype(numpy.float32))
            self.c.Set("refCentroids",None)
            cent = self.grab('rtcCentBuf',s.slope_iter)
            subapLocation[:,3:5] += round(cent[::2].mean())
            subapLocation[:,0:2] += round(cent[1::2].mean())
            print '\nX subap correction: ',
            print round(cent[::2].mean())
            print 'Y subap correction: ',
            print round(cent[1::2].mean())

            #Saving values found and removing previous values
            files = os.listdir(self.Cam.subaplocation_path)
            files = [st for st in files if 'led_%d.fits'%(star_id) in st]
            if(files!=[]):
                for file_name in files:
                    os.remove(self.Cam.subaplocation_path + file_name)

            FITS.Write(subapLocation.astype(numpy.float32),self.Cam.subaplocation_path + self.Cam.name+'_subapLocation_led_%d.fits'%(star_id),writeMode='a')

            #5- Ref Cent
            self.c.Set('subapLocation',subapLocation.astype(numpy.float32))
            cent = self.grab('rtcCentBuf',s.slope_iter)

            #Saving values found and removing previous values
            files = os.listdir(self.Cam.refcent_path)
            files = [st for st in files if 'led_%d.fits'%(star_id) in st]
            if(files!=[]):
                for file_name in files:
                    os.remove(self.Cam.refcent_path + file_name)

            FITS.Write(cent.astype(numpy.float32),self.Cam.refcent_path+self.Cam.name+'_RefCent_led_%d.fits'%(star_id),writeMode='a')
            self.c.Set('refCentroids',cent.astype(numpy.float32))
        else:
            print 'No subaps for led_%d'%(star_id)
        self.bbbc.star_off(star_id)

    def routine_calibration(self,star_list):
        '''
        Calibrates useBrightest, backgrounds and exptime times
        for given stars
        '''
        #Main loop. Calibrates for each star
        self.bbbc.set_position('horizontal_altitude_layer',-10000,200)
        #First we flush
        print 'Flushing!'
        self.flushAll()
        print 'Done flushing.\nBg acquisition...'
        self.Set_useBrightest()
        for star_id in star_list:
            estrella = Star(star_id)
            if(estrella.valid):
                print '\nCalibrating star:%3.0f ' %star_id
                self.bgImage_exptime_calibration(star_id)

    def first_calibration(self,star_list):
        '''
        Calibrates useBrightest, backgrounds, exptime times,
        subap locations and reference centroids for given stars
        '''
        #Main loop. Calibrates for each star
        #First we flush
        self.flushAll()
        self.Set_useBrightest()
        for star_id in star_list:
            estrella = Star(star_id)
            if(estrella.valid):
                print '\nCalibrating star:%3.0f ' %star_id
                self.pupil_location(star_id)
                self.subap_calibration(star_id)
                self.bgImage_exptime_calibration(star_id)
        raw_input('First calibration concluded.\nSet phase screen and press enter to continue')

    def flushAll(self):
        self.bbbc.flush_all_leds()

    def grab(stream,niter):
        taken = pp.unpack(self.c.GetStreamBlock(self.Cam.name+'rtcPxlBuf',niter)).sum(0)/float(niter)
        return taken

            
if __name__ == '__main__':
    from General_Calibration import Calibration
    cali = Calibration('sbig')
    array = cali.routine_calibration([1])
