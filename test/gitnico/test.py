#!/usr/bin/env/ python
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
from time import sleep
import sys
import turn_off_all

def turn_on_gpio(pin):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin,GPIO.HIGH)
#   print sys._getframe().f_code.co_name,
#   print(' '+pin)
            #raw_input('press a key to continue')

def turn_off_gpio(pin):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin,GPIO.LOW)
#   print sys._getframe().f_code.co_name,
#print(' '+pin)
                    #raw_input('press a key to continue')

if __name__ == '__main__':
    timeout = 1200 #secs
    turn_on_gpio('P8__27')
    sleep(timeout)
    raw_input('termine')
                    
