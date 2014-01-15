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
    raw_input('press a key to continue')

def turn_off_gpio(pin):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin,GPIO.LOW)
    print sys._getframe().f_code.co_name,
    print(' '+pin)
    raw_input('press a key to continue')

def turn_on_pwm(pin):
    PWM.start(pin, 50)
    PWM.set_duty_cycle(pin, 25.5)
    PWM.set_frequency(pin, 10)
    print sys._getframe().f_code.co_name,
    print(' '+pin)
    raw_input('press a key to continue')

def turn_off_pwm(pin):
    PWM.stop(pin)
    PWM.cleanup()
    print sys._getframe().f_code.co_name,
    print(' '+pin)
    raw_input('press a key to continue')

if __name__ == '__main__':
    timeout = 3 #secs
    
    ### LE ###
    print ('start to turn on ...')
    turn_on_gpio('P8_45')
    turn_on_gpio('P8_5')
    turn_on_gpio('P8_42')
    turn_on_gpio('P8_46')
    turn_on_gpio('P8_4')
    turn_on_gpio('P8_3')
    turn_on_gpio('P8_17')
    raw_input('\n\nIF you press ANY KEY,THEN you WILL QUIT!!!')


