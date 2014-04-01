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
import numpy
import darc
import FITS

from optparse import OptionParser
from subprocess import Popen, PIPE

from BeagleDarc.Controller import Controller
from BeagleDarc.Model import Layer
from BeagleDarc.Model import Star
from BeagleDarc.Model import Camera
from General_Calibration import General_Calibration

class Acquisition:
    def __init__(self):
        #Darc Controller instance
        self.camera_name = "SH"
        self.darc_instance = darc.Control(self.camera_name)
        #Beagle Controller instance
        self.bbbc = Controller()
        #self.logger = logging.getLogger(__name__)
        #Camera instance
        self.SHCamera = Camera('camera')

        #
        self.niter = 10
        self.image_path = self.SHCamera.image_path
        self.dir_name = 'slopes'

    def take_slp_from_darc(self):
        '''
        Using darc, take a FITS image and save it into the disk. By default use
        a <camera name>_<image prefix>_YEAR-MONTH-DAYTHOUR-MIN-SEC.fits as
        image name.  The path to be store the file as well as image_prefix can
        be modified in configuration file
    
        This should also take slopes (which will be used as training data)
        '''
        #Get slope_streams:
        logging.info('About to take image with darc ...')
        slope_stream = self.darc_instance.SumData('rtcCentBuf', self.niter,'f')[0]/float(self.niter)
        
        logging.debug(slope_stream)
        return slope_stream
        
    
    def take_data(self, star_list, cmd_list):
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
            #motor move
            motor = Layer('ground_layer')
            self.bbbc.set_position('ground_layer',cmd_list[0], 200)
            self.bbbc.layer_move('ground_layer')

            #motor move
            motor = Layer('horizontal_altitude_layer')
            self.bbbc.set_position('horizontal_altitude_layer',cmd_list[1], 200)
            self.bbbc.layer_move('horizontal_altitude_layer')

            #motor move
            motor = Layer('vertical_altitude_layer')
            self.bbbc.set_position('vertical_altitude_layer',cmd_list[2], 200)
            self.bbbc.layer_move('vertical_altitude_layer')

            slopes_frame = numpy.array([])
            # led on
            for star in star_list:
                star.setup(self.SHCamera)
                self.bbbc.star_on(int(star.image_prefix))
                #take img with darc
                slopes_frame = numpy.append(slopes_frame,self.take_slp_from_darc())
                
                #led off
                self.bbbc.star_off(int(star.image_prefix))
            
            return slopes_frame
 

    def take_all_data(self,iterations,star_list,prefix):
        Start_time = str(time.strftime("%Y_%m_%dT%H_%M_%S.fits", time.gmtime()))
        cali = General_Calibration(self.SHCamera.camera)
        cali.routine_calibration()
        all_data = numpy.zeros((iterations,len(star_list)*2*self.SHCamera.nsubaps))
        Star_list = []
        cmd_list = [0,0,0]
        for s in star_list:
            Star_list.append(Star(s))
        
        for i in range(0,iterations):
            print '\nTaking iteration #: %d' % (i+1)
            motor = Layer('ground_layer')

            #cmd_list[0] = random.randint(0,motor.vr_end)
            cmd_list[0] = random.randint(0,10)

            motor = Layer('horizontal_altitude_layer')

            #cmd_list[1] = random.randint(0,motor.vr_end)
            cmd_list[1] = random.randint(0,10)

            motor = Layer('vertical_altitude_layer')

            #cmd_list[2] = random.randint(0,motor.vr_end)
            cmd_list[2] = random.randint(0,10)
            
            oli = self.take_data(Star_list, cmd_list)
            all_data[i,:] = oli

        slope_name = self.camera_name + '_' + prefix + '_' +str(iterations).zfill(3) + '_T' +Start_time
        if os.path.exists(self.image_path+self.dir_name) is False:
            os.mkdir(self.image_path+self.dir_name)
        slp_path = os.path.normpath(self.image_path+self.dir_name+'/'+slope_name)
        FITS.Write(all_data.astype(numpy.float32), slp_path, writeMode='a')
        logging.info('Data saved : %s' % slp_path)

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


    a = Acquisition()
    star_list = [1,2,3,4]
    prefix = 'slopes'
    iterations = 5
    a.take_all_data(iterations,star_list,prefix)
