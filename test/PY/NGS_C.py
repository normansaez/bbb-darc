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
    
    print "NGS"
    print "Connector C"
    ### LE ###
    turn_off_gpio('P8_44')
    ### PWM ###
    turn_off_pwm('P9_14')
    ### ###
    turn_off_gpio('P8_20')
    turn_off_gpio('P8_16')
    turn_off_gpio('P8_14')
    turn_off_gpio('P8_12')
    turn_off_gpio('P8_6')
    print ('finish to turn off ...')
    raw_input('press a key to continue')
##################################################
    ### LE ###
    print ('start to turn on ...')
    turn_on_gpio('P8_44')
    print('LE: P8_44')
    raw_input('press a key to continue')
    ### PWM ###
    #turn_off_pwm('P9_14')
    ### ###
    turn_on_gpio('P8_20')
    print('P8_20')
    raw_input('press a key to continue')
    turn_on_gpio('P8_16')
    print('P8_16')
    raw_input('press a key to continue')
    turn_on_gpio('P8_14')
    print('P8_14')
    raw_input('press a key to continue')
    turn_on_gpio('P8_12')
    print('P8_12')
    raw_input('press a key to continue')
    turn_on_gpio('P8_6')
    print('P8_6')
    raw_input('press a key to continue')

