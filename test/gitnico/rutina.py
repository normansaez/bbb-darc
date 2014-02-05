#!/usr/bin/env python

import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
from time import sleep
import sys
import turn_off_all

def turn_on_gpio(pin):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin,GPIO.HIGH)

def turn_off_gpio(pin):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin,GPIO.LOW)


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

#Altitud horizontal
    turn_off_all.turn_off()
    turn_on_gpio('P9_41')
    turn_on_gpio('P8_24')
    turn_off_gpio('P9_41')
    
    turn_on_gpio('P9_27')
    count1 = 0
    flag = True
    limite = 10000
    while(flag):
        if count1 == limite:
            flag = False
        else:
            turn_off_gpio("P9_25")
            turn_on_gpio("P9_25")
        count1 += 1 
    # Cambio de direccion
    flag = True
    count1 = 0
    turn_on_gpio('P9_23')
    while(flag):
        if count1 == limite:
            flag = False
        else:
            turn_off_gpio("P9_25")
            turn_on_gpio("P9_25")
        count1 += 1
    turn_off_gpio('P9_27')
    print count1
    raw_input('\n\nIF you press ANY KEY,THEN you WILL QUIT!!!')
