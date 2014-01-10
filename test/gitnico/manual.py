#!/usr/bin/env python

import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
from time import sleep
import sys
import turn_off_all
from BeagleDarc.Model import Star

def turn_on_gpio(pin):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin,GPIO.HIGH)
#    print sys._getframe().f_code.co_name,
#    print(' '+pin)
    #raw_input('press a key to continue')

def turn_off_gpio(pin):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin,GPIO.LOW)
#    print sys._getframe().f_code.co_name,
#   print(' '+pin)
    #raw_input('press a key to continue')

def one_led(id_number):
#   Turning everything off
    turn_off_all.turn_off()
#   LE on
    turn_on_gpio(estrellas[id_number].pin_enable)
#   D on
    turn_on_gpio(estrellas[id_number].pin_led)
#   LE off
    turn_off_gpio(estrellas[id_number].pin_enable)

def move_motor(motor_number):
   turn_on_gpio(SLEEP_DIC[motor_number])
   aux_string = STEP_DIC[motor_number]
   aux_int = XY_DIC[motor_number]
   count1 = 0
   flag = True
   while(flag):
       try:
           turn_off_gpio(aux_string)
           turn_on_gpio(aux_string)
       except KeyboardInterrupt:
           flag = False
   
   # Cambio de direccion
   flag = True
   turn_on_gpio(DIR_DIC[i])
   while(aux_int>count1):
       try:
           turn_off_gpio(aux_string)
           turn_on_gpio(aux_string)
           count1 += 1
       except KeyboardInterrupt:
           flag = False
   turn_off_gpio(SLEEP_DIC[i])

 

#   Definicion de diccionarios
DIR_DIC={1:'P8_28',2:'P8_26',3:'P9_23'}
SLEEP_DIC={1:'P8_25',2:'P8_21',3:'P9_27'}
STEP_DIC={1:'P8_27',2:'P8_23',3:'P9_25'}
XY_DIC={1:9000,2:21000,3:21000}

#   Lista de Estrellas
estrellas = []
star = Star(1)
for i in range(1,53+1):
    star = Star(i)
    estrellas.append(star)

#   Otras variables   
count1 = 0
flag = True
aux_string = ''
aux_int = 0
opcion = 0
Pos1 = 0
Pos2 = 0
Pos3 = 0


if __name__ == '__main__':
#   Definicion de diccionarios
    DIR_DIC={1:'P8_28',2:'P8_26',3:'P9_23'}
    SLEEP_DIC={1:'P8_25',2:'P8_21',3:'P9_27'}
    STEP_DIC={1:'P8_27',2:'P8_23',3:'P9_25'}
    XY_DIC={1:9000,2:21000,3:21000}

#   Lista de Estrellas
    estrellas = []
    star = Star(1)
    for i in range(1,53+1):
        star = Star(i)
        estrellas.append(star)

#   Otras variables   
    count1 = 0
    flag = True
    aux_string = ''
    aux_int = 0
    opcion = 0

#   Apaga a la gente  
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

#   Setea posicion de motores
    for i in range(1,3+1):
        turn_on_gpio(SLEEP_DIC[i])
        aux_string = STEP_DIC[i]
        aux_int = XY_DIC[i]
        count1 = 0
        flag = True
        while(flag):
            try:
                turn_off_gpio(aux_string)
                turn_on_gpio(aux_string)
            except KeyboardInterrupt:
                flag = False
        
        # Cambio de direccion
        flag = True
        turn_on_gpio(DIR_DIC[i])
        while(aux_int>count1):
            try:
                turn_off_gpio(aux_string)
                turn_on_gpio(aux_string)
                count1 += 1
            except KeyboardInterrupt:
                flag = False
        turn_off_gpio(SLEEP_DIC[i])

    
    while(True):
        opcion = raw_input('Tell me, what can I do for you?
            \n1- Turn on a LED
            \n2- Move ground layer')








