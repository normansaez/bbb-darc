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

class SingletonServer:
    class __impl:
        def __init__(self):
            self.bds = BeagleDarcServerM('beagledarc_server')
            self.status = None

        def singleton_id(self):
            return id(self)

        def start_BBBServer(self):
            cmd = "ssh %s@%s \"python /home/ubuntu/bbb-darc/BBBServer/server.py &> /var/log/BBBServer.log &\"" % (self.bds.user, self.bds.host)
            process = Popen(cmd , stdout=sys.stdout , stderr=sys.stderr , shell=True)
            cmd = "ssh %s@%s \"cat /tmp/IOR.txt &\"" % (self.bds.user, self.bds.host)
            process = Popen(cmd , stdout=PIPE , stderr=PIPE , shell=True)
            sts = process.wait()
            out = process.stdout.read().strip()
            err = process.stderr.read().strip()
            self.bds.ior = out
            self.status = "ON"
            print "status: ON"

        def stop_BBBServer(self):
            cmd = "ssh %s@%s \"ps aux |grep server.py|awk \'{print \\$2}\'|xargs kill -9 && rm -fr /tmp/IOR.txt \"" % (self.bds.user, self.bds.host)
            process = Popen(cmd , stdout=PIPE , stderr=PIPE , shell=True)
            sts = process.wait()
            out = process.stdout.read().strip()
            err = process.stderr.read().strip()
            self.status = "OFF"
            print "status: OFF"

    __instance = None
    def __init__(self):
        '''
        Creates the Singleton (the only instance)
        '''
        if SingletonServer.__instance is None:
            SingletonServer.__instance = SingletonServer.__impl()
        self.__dict__['_Singleton__instance'] = SingletonServer.__instance   

    def __getattr__(self, attr):
        '''
        Overwritten __getattr__ method
        '''
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        '''
        Overwritten __setattr__ method
        '''
        return setattr(self.__instance, attr, value)

class Controller:
    '''
    Controller:
    '''
    def __init__(self):
        '''
        Init server in BBB called BBBServer
        '''
        self.sserver = SingletonServer()
        self.sserver.start_BBBServer()
        #init corba client:
        orb = CORBA.ORB_init()
        self.cli_obj = orb.string_to_object(self.sserver.bds.ior)

    def __del__(self):
        '''
        Stop server in BBB
        '''
        self.sserver.stop_BBBServer()

    def start_BBBServer(self):
        if self.sserver.status is "OFF":
            self.sserver.start_BBBServer()

    def stop_BBBServer(self):
        if self.sserver.status is "ON":
            self.sserver.stop_BBBServer()


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
