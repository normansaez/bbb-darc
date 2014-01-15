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

def move_motor(motor_number,steps):
    m = {1:"ground_layer",2:"vertical_altitude_layer",3:"horizontal_altitude_layer"}.get(motor_number)
    motor = Layer(m)
    turn_on_gpio(motor.pin_sleep)
    cmd_pos = 40000
    sumando = 0
    while(motor.cur_pos+cmd_pos>motor.vr_end or motor.cur_pos+cmd_pos<0)
        cmd_pos=raw_input('How many steps\n(sign does count)')
    if(cmd_pos>0):
        sumando = 1
        turn_off_gpio(motor.pin_dir)
    else:
        turn_on_gpio(motor.pin_dir)
        sumando = -1
    destino = motor.cur_pos + cmd_pos
    flag = True
    while(flag and destino != motor.cur_pos):
        try:
            turn_off_gpio(motor.pin_step)
            turn_on_gpio(motor.pin_step)
            motor.cur_pos += sumando
        except KeyboardInterrupt:
            flag = False
   
    turn_off_gpio(motor.pin_sleep)

def calibrate_motor():
    for i in range(1,3+1)      
        m = {1:"ground_layer",2:"vertical_altitude_layer",3:"horizontal_altitude_layer"}.get(motor_number)
        motor = Layer(m)
        turn_on_gpio(motor.pin_sleep)
        cmd_pos = 40000
        flag = True
        turn_off_gpio(motor.pin_dir)
        while(flag):
            try:
                turn_off_gpio(motor.pin_step)
                turn_on_gpio(motor.pin_step)
            except KeyboardInterrupt:
                flag = False
        motor.cur_pos = motot.vr_end
        turn_on_gpio(motor.pin_dir)
        flag = True
        while(flag and motor.cur_pos>0)
                try:
                    turn_off_gpio(motor.pin_step)
                    turn_on_gpio(motor.pin_step)
                    motor.cur_pos -= 1
                except KeyboardInterrupt:
                    flag = False
        turn_off_gpio(motor.pin_sleep)

def move_ground_layer(g_layer_motor, v_altitude_motor,h_altitude_motor,steps):
    stoped_v =
    move_vertical_altitude(v_altitude_motor,h_altitude_motor,steps)
#   La condicion de este y los ifs equivalentes necesita revision
#   Hacer funcion get_gpio()
    if stoped_v and
            (steps+g_layer_motor.cur_pos>g_layer_motor.vr_end):
        return False
    elif stoped_v:
        if get_gpio(v_altitude_motor.pin_dir):
            turn_off_gpio(v_altitude_motor.pin_dir)
        else:
            turn_on_gpio(v_altitude_motor.pin_dir)
        move_motor(1,steps)
        return True
    else:
        return True

def move_vertical_altitude(v_altitude_motor,h_altitude_motor,steps):
    stoped_h = move_horizontal_altitude(h_altitude_motor,steps)
    
    if stoped_h and (steps+v_altitude_motor.cur_pos>v_altitude_motor.vr_end):
        return True
    elif stoped_h:
        if get_gpio(h_altitude_motor.pin_dir):
            turn_off_gpio(h_altitude_motor.pin_dir)
        else:
            turn_on_gpio(h_altitude_motor.pin_dir)
        move_motor(2,steps)
        return False
    else:
        return False

def move_horizontal_altitude(h_altitude_motor,steps):


if __name__ == '__main__':

#   Otras variables   
    turn_off_all.turn_off()
    turn_off_all.turn_off_motor()
   
#   Direcciones iniciales a 'fin'
    turn_off_gpio("P8_28")
    turn_off_gpio("P8_26")
    turn_off_gpio("P9_23")

    calibrate_motor()
    
    take_data = True
    motorgl = Layer('ground_layer')
    motorval = Layer('vertical_altitude_layer')
    motorhal = Layer('horizontal_altitude_layer')
    steps = 1000
        
    while(take_data):
        take_data = move_ground_layer(motorgl,motorval,motorhal)





