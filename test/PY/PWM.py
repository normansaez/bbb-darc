#!/usr/bin/env python

import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
from time import sleep

def turn_on_gpio(pin):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin,GPIO.HIGH)

def turn_off_gpio(pin):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin,GPIO.LOW)

def turn_on_pwm(pin):
    PWM.start(pin, 50)
    PWM.set_duty_cycle(pin, 25.5)
    PWM.set_frequency(pin, 10)

def turn_off_pwm(pin):
    PWM.stop(pin)
    PWM.cleanup()

if __name__ == '__main__':
    timeout = 3 #secs
    
    print "PWM"
    turn_on_gpio('P9_14')
    print('P9_14')
    raw_input('press a key to continue')
    turn_on_gpio('P9_16')
    print('P9_16')
    raw_input('press a key to continue')
    turn_on_gpio('P8_13')
    print('P8_13')
    raw_input('press a key to continue')
    turn_on_gpio('P8_19')
    print('P8_19')
    raw_input('press a key to continue')
##################################################
