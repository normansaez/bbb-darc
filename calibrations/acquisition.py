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

class Acquisition:
    def __init__(self):
        #Darc Controller instance
        self.camera_name = "SH"
        self.darc_instance = darc.Control(self.camera_name)
        #Beagle Controller instance
        self.bbbc = Controller()
        #self.logger = logging.getLogger(__name__)

        #
        self.niter = 100
        self.image_path = '/home/dani/BeagleAcquisition/SH/'
        self.dir_name = 'slopes'

    def take_img_from_darc(self, iteration, prefix):
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
        slope_name = self.camera_name + '_' + prefix + '_' +str(iteration).zfill(3) + '_T' +str(time.strftime("%Y_%m_%dT%H_%M_%S.fits", time.gmtime()))
        if os.path.exists(self.image_path+self.dir_name) is False:
            os.mkdir(self.image_path+self.dir_name)
        slp_path = os.path.normpath(self.image_path+self.dir_name+'/'+slope_name)
        logging.info('Image taken : %s' % slp_path)
        logging.debug(slope_stream)
        FITS.Write(slope_stream, slp_path, writeMode='a')
        logging.info('Image saved : %s' % slp_path)
    
    def take_data(self, star_list, cmd_list):
            '''
            This method does:
            After that,  start all over again,  given a number of times in num
            variable
            '''
            #motor move
            motor = Layer('ground_layer')
            motor.cmd_pos = cmd_list[0]
            self.bbbc.layer_move('ground_layer')

            #motor move
            motor = Layer('horizontal_altitude_layer')
            motor.cmd_pos = cmd_list[1]
            self.bbbc.layer_move('horizontal_altitude_layer')

            #motor move
            motor = Layer('vertical_altitude_layer')
            motor.cmd_pos = cmd_list[2]
            self.bbbc.layer_move('vertical_altitude_layer')

            # led on
            for star in star_list:
                self.bbbc.star_on(star) 
                #take img with darc
                self.take_img_from_darc(star, 'slopes')
                #led off
                self.bbbc.star_off(star) 
    

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
#    a.take_img_from_darc(1,'slope')
    star_list = [1,2,3,4]
    cmd_list = [ 1000, 1000, 1000]
    a.take_data(star_list, cmd_list)
