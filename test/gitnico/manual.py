#!/usr/bin/env python

import Adafruit_BBIO.GPIO as GPIO
import sys
import turn_off_all
from BeagleDarc.Model import Star
from BeagleDarc.Model import Layer

def turn_on_gpio(pin):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin,GPIO.HIGH)

def turn_off_gpio(pin):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin,GPIO.LOW)

def one_led(id_number):
    star = Star(id_number)
#   Turning everything off
    turn_off_all.turn_off()
#   LE on
    turn_on_gpio(star.pin_enable)
#   D on
    turn_on_gpio(star.pin_led)
#   LE off
    turn_off_gpio(star.pin_enable)

def move_motor(motor_number):
    m = {1:"ground_layer",2:"vertical_altitude_layer",3:"horizontal_altitude_layer"}.get(motor_number)
    motor = Layer(m)
    turn_on_gpio(motor.pin_sleep)
    count1 = 0
    flag = True
    while(flag):
        try:
            turn_off_gpio(motor.pin_step)
            turn_on_gpio(motor.pin_step)
        except KeyboardInterrupt:
            flag = False
   
    # Cambio de direccion
    flag = True
    turn_on_gpio(motor.pin_dir)
    while(motor.vr_end > count1):
        try:
            turn_off_gpio(motor.pin_step)
            turn_on_gpio(motor.pin_step)
            count1 += 1
        except KeyboardInterrupt:
            flag = False
    turn_off_gpio(motor.pin_dir)

 

if __name__ == '__main__':

#   Otras variables   
    turn_off_all.turn_off()
    turn_off_all.turn_off_motor()
   
#   Motores a cero
#   A dormir   
    turn_off_gpio("P8_25")
    turn_off_gpio("P8_21")
    turn_off_gpio("P9_27")

#   Direcciones iniciales a 'fin'
    turn_off_gpio("P8_28")
    turn_off_gpio("P8_26")
    turn_off_gpio("P9_23")

    for i in range(1,3+1):
        move_motor(i)
    
    opcion = raw_input('Tell me, what can I do for you?\n1- Turn on a LED\n2- Move ground layer')
