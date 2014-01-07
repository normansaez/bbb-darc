#!/usr/bin/env python

import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
from time import sleep
import sys
import turn_off_all

def turn_on_gpio(pin):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin,GPIO.HIGH)
    print sys._getframe().f_code.co_name,
    print(' '+pin)
    #raw_input('press a key to continue')

def turn_off_gpio(pin):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin,GPIO.LOW)
    print sys._getframe().f_code.co_name,
    print(' '+pin)
    #raw_input('press a key to continue')

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
    
    turn_off_all.turn_off()
    # Se prende NGS-A1
    print ('\nstart to turn on PWM ...')
    turn_off_gpio('P9_14')
    turn_off_gpio('P8_13')
    turn_off_gpio('P9_16')
    turn_off_gpio('P8_19')
    
    # LE
    turn_on_gpio('P8_45')
    # Bus D 
    turn_on_gpio('P8_20')
    turn_off_gpio('P8_22')
    turn_off_gpio('P8_24')
    turn_off_gpio('P8_18')
    turn_off_gpio('P8_16')
    turn_off_gpio('P8_14')
    turn_off_gpio('P8_12')
    turn_off_gpio('P8_6')
    raw_input('press a key to disable')

    # Disable LE
    turn_off_gpio('P8_45')

    raw_input('\n\nIF you press ANY KEY,THEN you WILL QUIT!!!')
