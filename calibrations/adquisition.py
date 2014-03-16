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

class Adquisition:
    def __init__(self):
        #Darc Controller instance
        self.camera_name = "SH"
        self.darc_instance = darc.Control(self.camera_name)
        #Beagle Controller instance
        self.bbbc = Controller()
#        self.logger = logging.getLogger(__name__)

def take_img_from_darc(self, iteration, prefix):
    '''
    Using darc, take a FITS image and save it into the disk. By default use
    a image_prefix-YEAR-MONTH-DAY-T-HOUR-MIN-SEC.fits as image name.  The
    path to be store the file as well as image_prefix can be modified in
    configuration file
    '''
    try:
        logging.debug('About to take image with darc ...')
        stream = self.darc_instance.GetStream(self.camera_name+'rtcPxlBuf')
        img_ite = 's%s_'% str(iteration).zfill(3)
        img_wfs = 'w%s_'% str(prefix).zfill(3)
        image_name = img_ite + img_wfs +'T' +str(time.strftime("%Y_%m_%dT%H_%M_%S.fits", time.gmtime()))
        if os.path.exists(self.image_path+self.dir_name) is False:
            os.mkdir(self.image_path+self.dir_name)
        path = os.path.normpath(self.image_path+self.dir_name+'/'+image_name)
        logging.info('Image taken : %s' % path)
        logging.debug(stream)
        #print "stream info:"
        #print type(stream)
        #print stream
        #print type(stream[0])
        #print "####################"
        #print type(stream[1])
        data = stream[0].reshape(self.pxly, self.pxlx)
        #print data.shape
        #print "data info:"
        #print type(data)
        #print data
        #print data.shape
        data = data/4
        #print "--------------"
        #print data
        #print type(data)
        data = data.view('h')
        logging.debug('About to save image to disk , name: %s' % path)
        FITS.Write(data, path, writeMode='a')
        logging.info('Image saved : %s' % path)
    except Exception, ex:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logging.error(ex)
        logging.error("Check line number: %d" % exc_tb.tb_lineno)
        logging.error("Is darc running??") 

def take_data(self):
        '''
        This method does:
        0. take image (dark)
        1. turn on led 1
        2. take image
        3. turn on led 2
        4. take image
        5. turn on led 3
        6. take image
        7. move a motor
        
        After that,  start all over again,  given a number of times in num
        variable
        '''
        cur_pos_1 = 0
        cur_pos_2 = 0
        step = 5000
        self.take_img_from_darc('dark', 'dark')
        #mover motores:
        self.setup('motor_ground_layer')
        self.motor_to_init('motor_ground_layer')
        self.set_direccion(CHANGEDIR[self.direccion])
        cur_pos_1, cmd_pos = self.move_in_valid_range(cur_pos_1, step)

        for iteration in range(0, num):
            self.setup('led_lgs1')
            # led 1 on
            self.set_led_on()
            time.sleep(self.exposicion*MILI2SEC)

            #take img with darc
            self.take_img_from_darc(iteration, self.image_prefix)

            #led off
            self.set_led_off()

            # led 2 on
            self.setup('led_lgs2')
            self.set_led_on()
            time.sleep(self.exposicion*MILI2SEC)

            #take img with darc
            self.take_img_from_darc(iteration, self.image_prefix)

            #led off
            self.set_led_off()

            # led 3 on
            self.setup('led_lgs3')
            self.set_led_on()
            time.sleep(self.exposicion*MILI2SEC)

            #take img with darc
            self.take_img_from_darc(iteration, self.image_prefix)

            #led off
            self.set_led_off()

            # sci led on
            self.setup('led_sci')
            self.set_led_on()
            time.sleep(self.exposicion*MILI2SEC)

            #take img with darc
            self.take_img_from_darc(iteration, self.image_prefix)

            #led off
            self.set_led_off()

            #mover motores:
            cur_pos_1, cmd_pos = self.move_in_valid_range(cur_pos_1, step)
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



