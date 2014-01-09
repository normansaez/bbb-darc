#!/usr/bin/env python

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

    num = range(1,2000)
    
#    # Motor primero
#    # Prende el motor
#    turn_on_gpio('P8_25')
#    count1 = 0
#    flag = True
#    while(flag):
#        try:
#            turn_off_gpio("P8_27")
#            turn_on_gpio("P8_27")
#        except KeyboardInterrupt:
#            flag = False
#    
#    # Cambio de direccion
#    flag = True
#    turn_on_gpio('P8_28')
#    while(flag):
#        try:
#            turn_off_gpio("P8_27")
#            turn_on_gpio("P8_27")
#            count1 += 1
#        except KeyboardInterrupt:
#            flag = False
#    turn_off_gpio('P8_25')
#    print count1
#    
##   Motor segundo
#    turn_on_gpio('P8_21')
#    count1 = 0
#    flag = True
#    while(flag):
#        try:
#            turn_off_gpio("P8_23")
#            turn_on_gpio("P8_23")
#        except KeyboardInterrupt:
#            flag = False
#    
#    # Cambio de direccion
#    flag = True
#    turn_on_gpio('P8_26')
#    while(flag):
#        try:
#            turn_off_gpio("P8_23")
#            turn_on_gpio("P8_23")
#            count1 += 1
#        except KeyboardInterrupt:
#            flag = False
#    turn_off_gpio('P8_21')
#    print count1
#
#    #Motor tercero
#    turn_on_gpio('P9_27')
#    for i in num:
#        turn_off_gpio("P9_25")
#        sleep(timeout)
#        turn_on_gpio("P9_25")
#        sleep(timeout)
#    
#    turn_on_gpio("P9_23")
#    for i in num:
#        turn_off_gpio("P9_25")
#        sleep(timeout)
#        turn_on_gpio("P9_25")
#        sleep(timeout)
#    
#    turn_off_gpio('P9_27')
    turn_on_gpio('P9_27')
    count1 = 0
    flag = True
    while(flag):
        try:
            turn_off_gpio("P9_25")
            turn_on_gpio("P9_25")
        except KeyboardInterrupt:
            flag = False
    
    # Cambio de direccion
    flag = True
    turn_on_gpio('P9_23')
    while(flag):
        try:
            turn_off_gpio("P9_25")
            turn_on_gpio("P9_25")
            count1 += 1
        except KeyboardInterrupt:
            flag = False
    turn_off_gpio('P9_27')
    print count1
    raw_input('\n\nIF you press ANY KEY,THEN you WILL QUIT!!!')
