#!/usr/bin/env python

import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
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
    ### LE ###
    turn_on_gpio('P8_44')
    ### PWM ###
    #turn_off_pwm('P9_14')
    ### ###
    turn_on_gpio('P8_20')
    turn_on_gpio('P8_16')
    turn_on_gpio('P8_14')
    turn_on_gpio('P8_12')
    turn_on_gpio('P8_6')

