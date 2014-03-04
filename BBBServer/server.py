#
# The server
#

#!/usr/bin/env python

import sys, os
import BBBServer, BBBServer__POA
from omniORB import CORBA, PortableServer
import CosNaming
#import Adafruit_BBIO.GPIO as GPIO
#import Adafruit_BBIO.PWM as PWM
import getpass
from time import sleep
from server_dic import LED_STATUS
from server_dic import LE_DICT
from server_dic import PWM_LIST
from server_dic import DBUS_LIST
from BeagleDarc.Model import Layer

class Server_i (BBBServer__POA.Server):

    def __init__(self):
        self.turn_off_all_leds()
        self.turn_off_all_motors()

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
        motor_names =['ground_layer','vertical_altitude_layer','horizontal_altitude_layer']
        for motor_id in motor_names:
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
#       GPIO.setup(pin, GPIO.OUT)
#        GPIO.output(pin,GPIO.HIGH)
#        print sys._getframe().f_code.co_name,
#        print(' '+pin)
        pass

    def turn_off_gpio(self, pin):
#        GPIO.setup(pin, GPIO.OUT)
#        GPIO.output(pin,GPIO.LOW)
#        print sys._getframe().f_code.co_name,
#        print(' '+pin)
        pass

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
        print "---------------------------------------------------"
        print "%s(%s,%s,%s)" % (name, pin_led, pin_pwm, pin_enable)
        print "-----------"
        LED_STATUS[name][1] = "ON"
        self.refresh_led_status(pin_pwm, pin_enable)
        print "---------------------------------------------------"
        return "ok"

    def led_off(self, pin_led, pin_pwm, pin_enable, name, simulated, exp_time, brightness):
        print "---------------------------------------------------"
        print "%s(%s,%s,%s)" % (name, pin_led, pin_pwm, pin_enable)
        print "-----------"
        LED_STATUS[name][1] = "OFF"
        self.refresh_led_status(pin_pwm, pin_enable)
        print "---------------------------------------------------"
        return "ok"

    def motor_move(self, name, pin_dir, pin_step, pin_sleep, pin_opto1, pin_opto2, simulated, direction, velocity, steps, vr_init, vr_end, cur_pos):
        self.turn_on_gpio(pin_dir)
        self.turn_on_gpio(pin_sleep)
        for s in range(0, steps):
            self.turn_off_gpio(pin_step)
            self.turn_on_gpio(pin_step)
        self.turn_off_gpio(pin_sleep)
        return "ok"

    def motor_move_skip_sensor(self, name, pin_dir, pin_step, pin_sleep, pin_opto1, pin_opto2, simulated, direction, velocity, steps, vr_init, vr_end, cur_pos):
        self.turn_on_gpio(pin_dir)
        self.turn_on_gpio(pin_sleep)
        for s in range(0, steps):
            self.turn_off_gpio(pin_step)
            self.turn_on_gpio(pin_step)
        self.turn_off_gpio(pin_sleep)
        return "ok"
    
    def get_stars_status_keys(self):
        key_list = []
        for key, value in LED_STATUS.items():
            key_list.append(key)
        return key_list

    def get_stars_status_value(self, key):
        return LED_STATUS[key]

if __name__ == '__main__':
    #XXX: replace != by == 
    if getpass.getuser() != 'root':
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
