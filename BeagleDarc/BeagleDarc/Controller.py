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
        self.start_BBBServer()
        #init corba client:
        orb = CORBA.ORB_init()
        self.cli_obj = orb.string_to_object(self.bds.ior)

    def __del__(self):
        '''
        Stop server in BBB
        '''
        self.stop_BBBServer()

    def start_BBBServer(self):
        cmd = "ssh %s@%s \"python /home/ubuntu/bbb-darc/BBBServer/server.py &\"" % (self.bds.user, self.bds.host)
        process = Popen(cmd , stdout=sys.stdout , stderr=sys.stderr , shell=True)
        cmd = "ssh %s@%s \"cat /tmp/IOR.txt &\"" % (self.bds.user, self.bds.host)
        process = Popen(cmd , stdout=PIPE , stderr=PIPE , shell=True)
#        sts = process.wait()
#        out = process.stdout.read().strip()
#        err = process.stderr.read().strip()
#        self.bds.ior = out

    def stop_BBBServer(self):
        cmd = "ssh %s@%s \"ps aux |grep server.py|awk \'{print \\$2}\'|xargs kill -9 && rm -fr /tmp/IOR.txt \"" % (self.bds.user, self.bds.host)
        process = Popen(cmd , stdout=PIPE , stderr=PIPE , shell=True)
#        sts = process.wait()
#        out = process.stdout.read().strip()
#        err = process.stderr.read().strip()

    #star methods
    def star_on(self, star_id):
        star = Star(star_id)
        self.cli_obj.led_on(star.name, star.pin_led, star.pin_pwm, star.pin_enable)


    def star_off(self, star_id):
        star = Star(star_id)
#        self.cli_obj.led_off(name, pin_led, pin_pwm, pin_enable)

    #layer methods
    def layer_move(self, layer_id):
        layer = Layer(layer_id)
#        self.cli_obj.motor_move(name, steps, vel, pin_dir, pin_step, pin_sleep, stat_der, stat_izq)

    def layer_move_skip_sensor(self, layer_id):
        layer = Layer(layer_id)

if __name__ == '__main__':
    c = Controller()
    c.star_on(1)
    c.star_off(1)
    c.layer_move('ground_layer')
    c.layer_move_skip_sensor('ground_layer')
