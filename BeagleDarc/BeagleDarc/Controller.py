#!/usr/bin/python 
'''
Controller
'''

import sys
import BBBServer
import CosNaming
from BeagleDarc.Model import BeagleDarcServerM 
from BeagleDarc.Model import Star
from BeagleDarc.Model import Layer
from subprocess import Popen, PIPE
from omniORB import CORBA

class Controller:
    '''
    Controller:
    '''
    def __init__(self):
        '''
        Init server in BBB called BBBServer
        '''
        self.bds = BeagleDarcServerM('beagledarc_server')
        # Initialise the ORB
        orb = CORBA.ORB_init(sys.argv, CORBA.ORB_ID)
        
        # Obtain a reference to the root naming context
        obj         = orb.resolve_initial_references("NameService")
        rootContext = obj._narrow(CosNaming.NamingContext)
        
        if rootContext is None:
            print "Failed to narrow the root naming context"
            sys.exit(1)
        
        # Resolve the name "BeagleBone.Server/BBBServer.Object"
        name = [CosNaming.NameComponent("BeagleBone", "Server"),
                CosNaming.NameComponent("BBBServer", "Object")]
        try:
            obj = rootContext.resolve(name)
        
        except CosNaming.NamingContext.NotFound, ex:
            print "Name not found"
            sys.exit(1)
        
        # Narrow the object to an BBBServer::Server
        self.cli_obj = obj._narrow(BBBServer.Server)
        
        if (self.cli_obj is None):
            print "Object reference is not an BBBServer::Server"
            sys.exit(1)

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
