#!/usr/bin/python 
'''
'''

import sys
import os
import time
import glob
import logging
import ConfigParser
from BeagleDarc.Model import Layer
from time import sleep
import Adafruit_BBIO.GPIO as GPIO

def turn_on_gpio(pin):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin,GPIO.HIGH)

def turn_off_gpio(pin):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin,GPIO.LOW)



class Motor:
    def __init__(self, num=None):
        NUM2NAME = {1:'ground_layer',2:'vertical_altitude_layer',3:'horizontal_altitude_layer'}
        if num is None:
            num = 1

        self.layer = Layer(NUM2NAME[num])
        self.timeout = 0.0000001 #secs

    def move(self):
        turn_on_gpio(self.layer.sleep)
        for i in range(0,self.layer.steps):
            turn_off_gpio(self.layer.steps)
            sleep(timeout)
            turn_on_gpio(self.layer.steps)
            sleep(timeout)
            
        turn_off_gpio(self.layer.sleep)



if __name__ == '__main__':
    motor = Motor(1)

    steps = 2000
    motor.step = step
    motor.move()
        
