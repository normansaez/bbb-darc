#!/usr/bin/env python

import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
from time import sleep
import sys


def turn_on_gpio(pin):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin,GPIO.HIGH)
    print sys._getframe().f_code.co_name,
    print(' '+pin)
#    raw_input('press a key to continue')

def turn_off_gpio(pin):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin,GPIO.LOW)
    print sys._getframe().f_code.co_name,
    print(' '+pin)
#    raw_input('press a key to continue')

def turn_off():    
    #0- PWM to LOW
    turn_off_gpio("P8_13")
    turn_off_gpio("P8_19")
    turn_off_gpio("P9_14")
    turn_off_gpio("P9_16")
    
    #1- LE Enable
    turn_on_gpio("P8_3")
    turn_on_gpio("P8_4")
    turn_on_gpio("P8_5")
    turn_on_gpio("P8_11")
    turn_on_gpio("P8_15")
    turn_on_gpio("P8_17")
    turn_on_gpio("P8_42")
    turn_on_gpio("P8_44")
    turn_on_gpio("P8_45")
    turn_on_gpio("P8_46")
    turn_on_gpio("P9_12")
    turn_on_gpio("P9_15")
    turn_on_gpio("P9_41")
    turn_on_gpio("P9_42")

    #2- D-bus Disable
    turn_off_gpio("P8_6")
    turn_off_gpio("P8_12")
    turn_off_gpio("P8_14")
    turn_off_gpio("P8_16")
    turn_off_gpio("P8_18")
    turn_off_gpio("P8_20")
    turn_off_gpio("P8_22")
    turn_off_gpio("P8_24")

    #3- LE Disable
    turn_off_gpio("P8_3")
    turn_off_gpio("P8_4")
    turn_off_gpio("P8_5")
    turn_off_gpio("P8_11")
    turn_off_gpio("P8_15")
    turn_off_gpio("P8_17")
    turn_off_gpio("P8_42")
    turn_off_gpio("P8_44")
    turn_off_gpio("P8_45")
    turn_off_gpio("P8_46")
    turn_off_gpio("P9_12")
    turn_off_gpio("P9_15")
    turn_off_gpio("P9_41")
    turn_off_gpio("P9_42")
    
 

    
   
