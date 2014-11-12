#!/usr/bin/env python
from BeagleDarc.Controller import Controller

import sys
sys.path.append('/rtc/lib/python')
import os
import re
import time
import glob
import logging
import random
import ConfigParser
import numpy as np
import darc
import FITS
import matplotlib.pyplot as plt
import postprocess as pp

from optparse import OptionParser
from subprocess import Popen, PIPE

from BeagleDarc.Controller import Controller
from BeagleDarc.Model import Layer
from BeagleDarc.Model import Star
from BeagleDarc.Model import Camera
from General_Calibration import Calibration

class Acquisition:
    def __init__(self,dir_name='slopes',camera='pike'):
        #Camera instance
        self.Cam = Camera(camera)
        #Darc Controller instance
        self.c = darc.Control(self.Cam.name)
        #Beagle Controller instance
        self.bbbc = Controller()
        #self.logger = logging.getLogger(__name__)
        #Camera instance
        self.Cam = Camera(camera)

        #
        self.niter = 5
        self.image_path = self.Cam.image_path
        self.dir_name = dir_name
        self.cases = {'slopes':0,'images':1,'both':2}

    def grab(self,stream,niter):
        taken = pp.unpack(self.c.GetStreamBlock(self.Cam.name+stream,niter)).sum(0)/float(niter)
        return taken

    def grab_data_from_darc(self,acquire):
        '''
        Using darc, take a FITS image and save it into the disk. By default use
        a <camera name>_<image prefix>_YEAR-MONTH-DAYTHOUR-MIN-SEC.fits as
        image name.  The path to be store the file as well as image_prefix can
        be modified in configuration file
    
        This should also take slopes (which will be used as training data)
        '''
        logging.info('About to take data with darc ...')
        slope_stream = None

        #Get slope_streams:
        if(self.cases[acquire]==0):
            slope_stream = self.grab('rtcCentBuf',self.niter)
            logging.debug(slope_stream)
            return slope_stream
        elif(self.cases[acquire]==1):
            slope_stream = self.grab('rtcCalPxlBuf',self.niter)
            logging.debug(slope_stream)
            return slope_stream
        else:
            print 'Can\'t acquire!'
            return
        
    
    def take_data(self, star_list, cmd_list,acquire):
            '''
            This method does:
            After that,  start all over again,  given a number of times in num
            variable

            star_list is a Star object list

            from BeagleDarc.Model import Star
            star_list = []
            for i in range(1,n+1):
                star_list.append(Star(i))
            
            '''
            print 'Acquisition position: ',
            print cmd_list

            #Turning on a star to prevent noise
            self.bbbc.star_on(1)

            #horizontal motor move
            self.bbbc.set_position('horizontal_altitude_layer',cmd_list[0], 200)

            #vertical motor move
            self.bbbc.set_position('vertical_altitude_layer',cmd_list[1], 200)
            
            slopes_frame = None
            images_frame = None

            if(self.cases[acquire]==0):
                slopes_frame = np.array([])
            elif(self.cases[acquire]==1):
                images_frame = np.array([])
            elif(self.cases[acquire]==2):
                slopes_frame = np.array([])
                images_frame = np.array([])

            # led on
            self.bbbc.star_off(1)
            for star in star_list:
                star.setup(self.Cam)
                self.bbbc.star_on(int(star.image_prefix))
                #take img with darc
                if(self.cases[acquire]==0):
                    slopes_frame = np.append(slopes_frame,self.grab_data_from_darc(acquire))
                elif(self.cases[acquire]==1):
                    images_frame = np.append(images_frame,self.grab_data_from_darc(acquire))
                elif(self.cases[acquire]==2):
                    slopes_frame = np.append(slopes_frame,self.grab_data_from_darc('slopes'))
                    images_frame = np.append(images_frame,self.grab_data_from_darc('images'))
                
                #led off
                self.bbbc.star_off(int(star.image_prefix))
            
            if(self.cases[acquire]==0):
                return slopes_frame
            elif(self.cases[acquire]==1):
                return images_frame
            elif(self.cases[acquire]==2):
                return (slopes_frame,images_frame)
            return slopes_frame
 

    def take_all_data(self,iterations,star_list,prefix,acquire='slopes',altitude=-1,fpf=10):
        '''
        fpf = frames per FITS.
        smpling = steps per position
        '''
        Start_time = str(time.strftime("%Y_%m_%dT%H_%M_%S.fits", time.gmtime()))
        #cali = Calibration(self.Cam.name)
        #cali.routine_calibration(star_list)

        # Comment this flush when calibrating
        self.bbbc.flush_all_leds()
        all_slopes = None
        all_images = None
        cmd_list = None
        if(self.cases[acquire]==0):
            all_slopes = np.zeros((fpf,len(star_list)*2*self.Cam.nsubaps))
        elif(self.cases[acquire]==1):
            all_images = np.zeros((fpf,len(star_list)*self.Cam.pxlx*self.Cam.pxly))
        elif(self.cases[acquire]==2):
            all_slopes = np.zeros((fpf,len(star_list)*2*self.Cam.nsubaps))
            all_images = np.zeros((fpf,len(star_list)*self.Cam.pxlx*self.Cam.pxly))
        else:
            print 'Can\'t acquire!'
            return
        Star_list = []
        cmd_list = self.cmdlist_gen(iterations,altitude)
        for s in star_list:
            Star_list.append(Star(s))
        
        for i in range(0,int(iterations)):
            Start_time = str(time.strftime("%Y_%m_%dT%H_%M_%S.fits", time.gmtime()))
            print '\nTaking iteration #: %d' % (i+1)
            if(self.cases[acquire]==0):
                oli = self.take_data(Star_list, cmd_list[i],'slopes')
                all_slopes[i%fpf,:] = oli
            elif(self.cases[acquire]==1):
                oli = self.take_data(Star_list, cmd_list[i],'images')
                all_images[i%fpf,:] = oli
            elif(self.cases[acquire]==2):
                oli = self.take_data(Star_list, cmd_list[i],'both')
                all_slopes[i%fpf,:] = oli[0]
                all_images[i%fpf,:] = oli[1]
            
            if((i+1)%fpf==0 or i==(iterations-1)):
                if os.path.exists(self.image_path+self.dir_name) is False:
                    os.mkdir(self.image_path+self.dir_name)
                slope_name = self.Cam.name + '_slopes_' + prefix + '_' +str(fpf).zfill(3) + '_T' +Start_time
                image_name = self.Cam.name + '_images_' + prefix + '_' +str(fpf).zfill(3) + '_T' +Start_time 
                slp_path = os.path.normpath(self.image_path+self.dir_name+'/'+slope_name)
                img_path = os.path.normpath(self.image_path+self.dir_name+'/'+image_name)
                if(self.cases[acquire]==0):
                    FITS.Write(all_slopes.astype(np.float32), slp_path, writeMode='w')
                elif(self.cases[acquire]==1):
                    FITS.Write(all_images.astype(np.float32), img_path, writeMode='w')
                elif(self.cases[acquire]==2):
                    FITS.Write(all_slopes.astype(np.float32), slp_path, writeMode='w')
                    FITS.Write(all_images.astype(np.float32), img_path, writeMode='w')
                logging.info('Data saved : %s' % slp_path)
                Start_time = str(time.strftime("%Y_%m_%dT%H_%M_%S.fits", time.gmtime()))
                if(self.cases[acquire]==0):
                    all_slopes = all_slopes*0.
                elif(self.cases[acquire]==1):
                    all_images = all_images*0.
                elif(self.cases[acquire]==2):
                    all_slopes = all_slopes*0.
                    all_images = all_images*0.
                self.bbbc.flush_all_leds()
               
        
    def cmdlist_gen(self,iterations,altitude=-1):
        # Motor 0: horizontal
        motorh = Layer('horizontal_altitude_layer')
        # Motor 1: vertical
        motorv = Layer('vertical_altitude_layer')
        cmd_temp = []
        cmd_list = []
        cur_pos = [0,0]
        mindis = motorh.vr_end + motorv.vr_end
        minarg = 0
        cmdx = []
        cmdy = []
        
        for cmd in range(0,int(iterations)):
            if(altitude>=0.0 and altitude<=1.0):
                cmd_temp = cmd_temp + [[int(motorh.vr_end*cmd/iterations),int(altitude*motorv.vr_end)]]
            else:
                cmd_temp = cmd_temp + [[random.randint(0,motorh.vr_end),random.randint(0,motorv.vr_end)]]

        for it0 in range(0,int(iterations)):
            for it1 in range(0,len(cmd_temp)):
                if(mindis > (abs(cmd_temp[it1][0]-cur_pos[0])*0.5 + (cmd_temp[it1][1]-cur_pos[1]))):
                    mindis = abs(cmd_temp[it1][0]-cur_pos[0])*0.5 + (cmd_temp[it1][1]-cur_pos[1])
                    minarg = it1
            
            cur_pos = cmd_temp.pop(minarg)
            cmd_list = cmd_list + [cur_pos]
            cmdx = cmdx + [cur_pos[0]]
            cmdy = cmdy + [cur_pos[1]]
            minarg = 0
            mindis = motorh.vr_end + motorv.vr_end
            
        #plt.plot(cmdx,cmdy,'k')
        #plt.show()
        return cmd_list

    def first_calibration(self,star_list):
        cali = Calibration(self.Cam.camera)
        cali.first_calibration(star_list)

if __name__ == '__main__':
    usage = '''
            Type -h, --help for help.
                '''
    parser = OptionParser(usage)
    parser.add_option("-d", "--debug", dest="debug", metavar="debug", default=False, action="store_true", help = "debug mode, prints all messages")
    (options , args) = parser.parse_args()
    if options.debug is False:
        logging.getLogger().setLevel(logging.INFO)
        logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s')
    else:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.basicConfig(format='%(asctime)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s')


    dir_name = 'alt_050_v1_s_16_8_3_1_5_12_20_34'
    '''
    acquire = 'slopes'
    prefix = 'useB_0'
    star_list = [4,18,24,36]
    altitude = -1
    '''
    
    acquire = 'images'
    prefix = 'useB_0'
    #star_list = [1,6,7,8,9,10,11,12,13,14,18,24,26,28,32,34,36,49,51]
    #star_list = [5,26]
    #star_list = [1,18,26]
    star_list = [16,8,3,1,5,12,20,34]
    altitude = 0.5
    

    a = Acquisition(dir_name=dir_name,camera='pike')
    iterations = 14500./18. # 18 is the number of steps per position
    numberoffits = 1
    fpf = 10
    #a.first_calibration(star_list)
    for nof in range(1,numberoffits+1):
        a.take_all_data(iterations,star_list,prefix,acquire=acquire,altitude=altitude,fpf=fpf)
        #fix = prefix + '_altitude_%.0f'%(100*(nof-1)/(numberoffits-1))
        #a.take_all_data(iterations,star_list,fix,acquire=acquire,altitude=(nof-1.0)/(numberoffits-1))

