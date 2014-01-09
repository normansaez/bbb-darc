#!/usr/bin/env python

import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
from time import sleep
import sys
import turn_off_all
import os

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

def move_step_pin(motor, steps):
    os.system("./motor %d %d" % motor, steps)
if __name__ == '__main__':
    timeout = 0.0000001 #secs
    
    turn_off_all.turn_off()
    turn_off_gpio("P8_28")
    turn_off_gpio("P8_25")
    turn_off_gpio("P8_41")
    turn_off_gpio("P8_43")

    turn_off_gpio("P8_26")
    turn_off_gpio("P8_21")
    turn_off_gpio("P8_40")
    turn_off_gpio("P8_39")

    turn_off_gpio("P9_23")
    turn_off_gpio("P9_27")
    turn_off_gpio("P8_30")
    turn_off_gpio("P8_29")

    # Motor primero
    turn_on_gpio('P8_25')
    move_step_pin(1,5000)

    turn_on_gpio("P8_28")
    move_step_pin(1,5000)
    
    raw_input('siguiente motor')
    turn_off_gpio('P8_25')

    #Motor segundo
    turn_on_gpio('P8_21')
    move_step_pin(2,5000)
    turn_on_gpio("P8_26")
    move_step_pin(2,5000)
    raw_input('siguiente motor')    
    turn_off_gpio('P8_21')

    #Motor tercero
    turn_on_gpio('P9_27')
    move_step_pin(3,5000)
    turn_on_gpio("P9_23")
    move_step_pin(3,5000)
    turn_off_gpio('P9_27')
    raw_input('\n\nIF you press ANY KEY,THEN you WILL QUIT!!!')
