#!/usr/bin/python 
'''
Controller
'''

import CORBA
import BBBServer
import sys
from BeagleDarc.Model import BeagleDarcServerM 
from BeagleDarc.Model import Star
from BeagleDarc.Model import Layer
from subprocess import Popen, PIPE

class Controller:
    '''
    Controller:
    '''
    def __init__(self):
        '''
        Init server in BBB called BBBServer
        '''
        self.bds = BeagleDarcServerM('beagledarc_server')
        #init corba client:
        orb = CORBA.ORB_init()
        self.cli_obj = orb.string_to_object(self.bds.ior)
    #star methods
    def star_on(self, star_id):
        star = Star(star_id)
        self.cli_obj.led_on(str(star.pin_led), str(star.pin_pwm), str(star.pin_enable), str(star.name), str(star.simulated), str(star.exp_time), str(star.brightness))

    def star_off(self, star_id):
        star = Star(star_id)
        self.cli_obj.led_off(str(star.pin_led), str(star.pin_pwm), str(star.pin_enable), str(star.name), str(star.simulated), str(star.exp_time), str(star.brightness))


    #layer methods
    def layer_move(self, layer_id):
        layer = Layer(layer_id)
        self.cli_obj.motor_move(layer.name, layer.pin_dir, layer.pin_step, layer.pin_sleep, layer.pin_opto1, layer.pin_opto2, layer.simulated, layer.direction, layer.velocity, layer.steps, layer.vr_init, layer.vr_end, layer.cur_pos)

    def layer_move_skip_sensor(self, layer_id):
        layer = Layer(layer_id)
        self.cli_obj.motor_move_skip_sensor(layer.name, layer.pin_dir, layer.pin_step, layer.pin_sleep, layer.pin_opto1, layer.pin_opto2, layer.simulated, layer.direction, layer.velocity, layer.steps, layer.vr_init, layer.vr_end, layer.cur_pos)

if __name__ == '__main__':
    c = Controller()
    c.star_on(1)
    c.star_off(1)
#    c.layer_move('ground_layer')
#    c.layer_move_skip_sensor('ground_layer')
