#!/usr/bin/env python

import sys, os
import BBBServer, BBBServer__POA
from omniORB import CORBA, PortableServer
import CosNaming
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
import getpass
import c_driver
from time import sleep
from server_dic import LED_STATUS
from server_dic import LE_DICT
from server_dic import PWM_LIST
from server_dic import DBUS_LIST
from BeagleDarc.Model import Layer
from BeagleDarc.Model import Star

MOTORS = ['ground_layer','vertical_altitude_layer','horizontal_altitude_layer']

class Server_i (BBBServer__POA.Server):

    def __init__(self):
        self.turn_off_all_leds()
        self.turn_off_all_motors()
        self.flush_all_leds()

    def flush_all_leds(self):
        for i in range(1,53+1):
            try:
                star = Star(i)
                self.led_on(star.pin_led, star.pin_pwm, star.pin_enable, star.name, star.simulated, star.exp_time, star.brightness)
                self.led_off(star.pin_led, star.pin_pwm, star.pin_enable, star.name, star.simulated, star.exp_time, star.brightness)
            except Exception, e:
                print e
        return 0
    def turn_off_all_leds(self):    
        #0- PWM to LOW
        self.disable_all_pwm()

        #1- LE Enable
        self.enable_all_LE()
    
        #2- D-bus Disable
        self.disable_all_dbus()
    
        #3- LE Disable
        self.disable_all_LE()

    def turn_off_all_motors(self):
        for motor_id in MOTORS:
            motor = Layer(motor_id)
            self.turn_off_gpio(motor.pin_dir)
            self.turn_off_gpio(motor.pin_step)
            self.turn_off_gpio(motor.pin_sleep)
            self.turn_off_gpio(motor.pin_opto1)
            self.turn_off_gpio(motor.pin_opto2)
    
    def disable_all_pwm(self):
        #0- PWM to LOW
        for pwm in PWM_LIST:
            self.turn_off_gpio(pwm)

    def enable_all_LE(self):
        #1- LE Enable
        for key, value in LE_DICT.items():
            self.turn_on_gpio(key)

    def disable_all_dbus(self):
        #2- D-bus Disable
        for dbus in DBUS_LIST:
            self.turn_off_gpio(dbus)
    
    def disable_all_LE(self):
        #3- LE Disable
        for key, value in LE_DICT.items():
            self.turn_off_gpio(key)

    def turn_on_gpio(self, pin):
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin,GPIO.HIGH)
#        c_driver.handle_gpio(1, pin)
#        print sys._getframe().f_code.co_name,
#        print(' '+pin)

    def turn_off_gpio(self, pin):
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin,GPIO.LOW)
#        c_driver.handle_gpio(0, pin)
#        print sys._getframe().f_code.co_name,
#        print(' '+pin)

    def refresh_led_status(self, pin_pwm, pin_enable):
        '''
        '''
        self.turn_off_gpio(pin_pwm)
        #Disable all LE
        self.disable_all_LE()
        
        self.turn_on_gpio(pin_enable)
        le_list = LE_DICT[pin_enable]
        for led in le_list:
            #print led
            led_sts = LED_STATUS[led]
            if led_sts[1] == "OFF":
                self.turn_off_gpio(led_sts[0])
            else:
                self.turn_on_gpio(led_sts[0])
        self.turn_off_gpio(pin_enable)
        #Disable all LE
        self.disable_all_LE()
        
        for key, value in LED_STATUS.iteritems():
            if value[1] == "ON":
                msg = "\033[31m%s->%s\033[0m" % (str(key), str(value))
                print msg
            else:
#                print key, value
                pass
                
    def led_on(self, pin_led, pin_pwm, pin_enable, name, simulated, exp_time, brightness):
        print sys._getframe().f_code.co_name,
        print ": %s(%s,%s,%s)" % (name, pin_led, pin_pwm, pin_enable)
        LED_STATUS[name][1] = "ON"
        self.refresh_led_status(pin_pwm, pin_enable)
        return "ok"

    def led_off(self, pin_led, pin_pwm, pin_enable, name, simulated, exp_time, brightness):
        print sys._getframe().f_code.co_name,
        print ": %s(%s,%s,%s)" % (name, pin_led, pin_pwm, pin_enable)
        LED_STATUS[name][1] = "OFF"
        self.refresh_led_status(pin_pwm, pin_enable)
        return "ok"

    def motor_move(self, name, direction, velocity, steps, cur_pos, cmd_pos):
        return self.motor_move_skip_sensor(name, direction, velocity, steps, cur_pos, cmd_pos) 

    def set_to_zero(self, name, direction, velocity, steps, cur_pos, cmd_pos):
        motor = Layer(name)
        motor.steps = 0
        motor.direction = direction
        motor.velocity = velocity
        dir_pin = 0
        motor.cur_pos = 0
        motor.cmd_pos = 0
        print "SET ALL TO ZERO"
        print "name      %s" % motor.name
        print "direction %s" % motor.direction
        print "velocity  %d" % motor.velocity
        print "steps     %d" % motor.steps
        print "cur_pos   %d" % motor.cur_pos
        print "cmd_pos   %d" % motor.cmd_pos
        return 0
    
    def motor_move_skip_sensor(self, name, direction, velocity, steps, cur_pos, cmd_pos):
        print "name      %s" % name
        print "direction %s" % direction
        print "velocity  %d" % velocity
        print "steps     %d" % steps
        print "cur_pos   %d" % cur_pos
        print "cmd_pos   %d" % cmd_pos
        motor = Layer(name)
        motor.steps = steps
        motor.direction = direction
        motor.velocity = velocity
        dir_pin = 0

        if('INIT_POSITION' in direction):
            dir_pin = 1 - motor.pos_dir
        else:
            dir_pin = motor.pos_dir

        if(dir_pin):
            print 'pin on'
        else:
            print 'pin off'

        if(dir_pin):
            self.turn_on_gpio(motor.pin_dir)
        else:
            self.turn_off_gpio(motor.pin_dir)

        self.turn_on_gpio(motor.pin_sleep)
        s = c_driver.move_motor(steps, motor.pin_step)
        self.turn_off_gpio(motor.pin_sleep)
        print sys._getframe().f_code.co_name,
        print ": %s -> %1.2f " % (name, s)

        motor.cur_pos = cmd_pos
        motor.cmd_pos = cmd_pos
        print "\n\n"
        return motor.cur_pos
    
    def get_stars_status_keys(self):
        key_list = []
        for key, value in LED_STATUS.items():
            key_list.append(key)
        return key_list

    def get_stars_status_value(self, key):
        return LED_STATUS[key]

    def get_motor_cur_pos(self, name):
        motor = Layer(name)
        return motor.cur_pos

    def get_motor_cmd_pos(self, name): 
        motor = Layer(name)
        return motor.cmd_pos

if __name__ == '__main__':
    if getpass.getuser() == 'root':
        # Initialise the ORB and find the root POA
        orb = CORBA.ORB_init(sys.argv, CORBA.ORB_ID)
        poa = orb.resolve_initial_references("RootPOA")
        
        servanti = Server_i()
        servant = servanti._this()
        # Obtain a reference to the root naming context
        obj         = orb.resolve_initial_references("NameService")
        rootContext = obj._narrow(CosNaming.NamingContext)
        if rootContext is None:
            print "Failed to narrow the root naming context"
            sys.exit(1)
        
        # Bind a context named "BeagleBone.Server" to the root context
        name = [CosNaming.NameComponent("BeagleBone", "Server")]
        try:
            BeagleBoneContext = rootContext.bind_new_context(name)
            print "New BeagleBone context bound"
            
        except CosNaming.NamingContext.AlreadyBound, ex:
            print "BeagleBone context already exists"
            obj = rootContext.resolve(name)
            BeagleBoneContext = obj._narrow(CosNaming.NamingContext)
            if BeagleBoneContext is None:
                print "BeagleBone.Server exists but is not a NamingContext"
                sys.exit(1)
        
        # Bind the BBBServer object to the BeagleBone context
        name = [CosNaming.NameComponent("BBBServer", "Object")]
        try:
            BeagleBoneContext.bind(name, servant)
            print "New BBBServer object bound"
        
        except CosNaming.NamingContext.AlreadyBound:
            BeagleBoneContext.rebind(name, servant)
            print "BBBServer binding already existed -- rebound"
        
        # Activate the POA
        poaManager = poa._get_the_POAManager()
        poaManager.activate()
        
        # Block for ever (or until the ORB is shut down)
        orb.run()
    else:
        print "The server should run as root!!:\nsudo su -\npython\
        /home/ubuntu/bbb-darc/BBBServer/server.py"
