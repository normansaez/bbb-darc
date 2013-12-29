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
    
    ### LE ###
    print ('start to turn on ...')
    turn_on_gpio('P8_45')
    print('LE: P8_45')
    raw_input('press a key to continue')
    turn_on_gpio('P8_5')
    print('LE: P8_5')
    raw_input('press a key to continue')
    turn_on_gpio('P8_42')
    print('LE: P8_42')
    raw_input('press a key to continue')
    turn_on_gpio('P8_46')
    print('LE: P8_46')
    raw_input('press a key to continue')
    turn_on_gpio('P8_4')
    print('LE: P8_4')
    raw_input('press a key to continue')
    turn_on_gpio('P8_3')
    print('LE: P8_3')
    raw_input('press a key to continue')
    turn_on_gpio('P8_17')
    print('LE: P8_17')
    raw_input('press a key to continue')


