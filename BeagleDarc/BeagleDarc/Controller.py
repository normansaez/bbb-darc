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
#        obj         = orb.resolve_initial_references("NameService")
        obj         = orb.string_to_object("corbaloc:iiop:10.42.0.97/NameService")
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
        self.client = obj._narrow(BBBServer.Server)
        
        if (self.client is None):
            print "Object reference is not an BBBServer::Server"
            sys.exit(1)

    #star methods
    def flush_all_leds(self):
        return self.client.flush_all_leds()

    def star_on(self, star_id):
        star = Star(star_id)
        self.client.led_on(star.pin_led,
                star.pin_pwm,
                star.pin_enable,
                star.name,
                star.simulated,
                star.exp_time,
                star.brightness)

    def star_off(self, star_id):
        star = Star(star_id)
        self.client.led_off(star.pin_led, 
                star.pin_pwm, 
                star.pin_enable, 
                star.name, 
                star.simulated, 
                star.exp_time, 
                star.brightness)


    #layer methods
    def layer_move(self, layer_id):
        layer = Layer(layer_id)
        steps = self.client.motor_move(layer.name, 
                layer.direction, 
                layer.velocity, 
                layer.steps, 
                layer.cur_pos,
                layer.cmd_pos)
        layer.cur_pos = layer.cur_pos + steps
        return steps

    def layer_move_skip_sensor(self, layer_id):
        layer = Layer(layer_id)
        steps = self.client.motor_move_skip_sensor(layer.name, 
                layer.direction, 
                layer.velocity, 
                layer.steps, 
                layer.cur_pos,
                layer.cmd_pos)
        layer.cur_pos = layer.cur_pos + steps
        return steps

    def get_stars_status(self):
        led_status = {}
        key_list = self.client.get_stars_status_keys()
        for i in key_list:
            status = self.client.get_stars_status_value(i)
            star_id = status[2]
            sts = status[1]
            led_status[int(star_id)] = sts
        return led_status

    def set_position(self, layer_id, cmd_pos, vel):
        '''
        '''
        layer = Layer(layer_id)
        layer.cmd_pos = cmd_pos
        layer.velocity = vel
        layer.cur_pos = self.client.get_motor_cur_pos(layer.name)
        steps = cmd_pos - layer.cur_pos
        if steps > 0:
            layer.direction = 'END_POSITION'
        else:
            layer.direction = 'INIT_POSITION'
            steps = abs(steps)
        layer.steps = steps
        layer.cur_pos = self.layer_move_skip_sensor(layer_id)
        
    def get_motor_cur_pos(self, layer_id):
        '''
        '''
        layer = Layer(layer_id)
        return self.client.get_motor_cur_pos(layer.name)

    def get_motor_cmd_pos(self, layer_id):
        '''
        '''
        layer = Layer(layer_id)
        return self.client.get_motor_cmd_pos(layer.name)

if __name__ == '__main__':
    c = Controller()
    c.star_on(1)
    c.star_off(1)
    #print c.layer_move('ground_layer')
    #print c.layer_move_skip_sensor('ground_layer')
    import darc
    c = darc.Control('SH')
