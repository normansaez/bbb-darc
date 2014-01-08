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
import omniORB

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
        self.cli_obj = None
        self.cli_obj  = orb.string_to_object('IOR:010000001900000049444c3a4242425365727665722f5365727665723a312e3000000000010000000000000064000000010102000b00000031302e34322e302e3937000052e700000e000000fed0a5cc5200000b99000000000000000200000000000000080000000100000000545441010000001c00000001000000010001000100000001000105090101000100000009010100')
#        try:
#            self.cli_obj = orb.string_to_object(self.bds.ior)
#        except omniORB.CORBA.MARSHAL, e:
#            print "START SERVER ON BEAGLEBONE OR SET IOR CORRECTLY"
#            sys.exit(-1)
    #star methods
    def star_on(self, star_id):
        star = Star(star_id)
        self.cli_obj.led_on(star.pin_led, star.pin_pwm, star.pin_enable, star.name, star.simulated, star.exp_time, star.brightness)

    def star_off(self, star_id):
        star = Star(star_id)
        self.cli_obj.led_off(star.pin_led, star.pin_pwm, star.pin_enable, star.name, star.simulated, star.exp_time, star.brightness)


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
    c.layer_move('ground_layer')
    c.layer_move_skip_sensor('ground_layer')
