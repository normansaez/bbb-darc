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
from server_dic import STAR_STATUS
from server_dic import LE_DICT

class Server_i (BBBServer__POA.Server):

    def __init__(self):
        self.turn_off()
        self.initial_status_motors()
        pass

    def turn_off(self):    
        #0- PWM to LOW
        self.disable_all_pwm()

        #1- LE Enable
        self.enable_all_LE()
    
        #2- D-bus Disable
        self.disable_all_dbus()
    
        #3- LE Disable
        self.disable_all_LE()

    def initial_status_motors(self):
        self.turn_off_gpio("P8_28")
        self.turn_off_gpio("P8_25")
        self.turn_off_gpio("P8_41")
        self.turn_off_gpio("P8_43")

        self.turn_off_gpio("P8_26")
        self.turn_off_gpio("P8_21")
        self.turn_off_gpio("P8_40")
        self.turn_off_gpio("P8_39")

        self.turn_off_gpio("P9_23")
        self.turn_off_gpio("P9_27")
        self.turn_off_gpio("P8_30")
        self.turn_off_gpio("P8_29")
    
    def disable_all_pwm(self):
        #0- PWM to LOW
        self.turn_off_gpio("P8_13")
        self.turn_off_gpio("P8_19")
        self.turn_off_gpio("P9_14")
        self.turn_off_gpio("P9_16")

    def enable_all_LE(self):
        #1- LE Enable
        self.turn_on_gpio("P8_3")
        self.turn_on_gpio("P8_4")
        self.turn_on_gpio("P8_5")
        self.turn_on_gpio("P8_11")
        self.turn_on_gpio("P8_15")
        self.turn_on_gpio("P8_17")
        self.turn_on_gpio("P8_42")
        self.turn_on_gpio("P8_44")
        self.turn_on_gpio("P8_45")
        self.turn_on_gpio("P8_46")
        self.turn_on_gpio("P9_12")
        self.turn_on_gpio("P9_15")
        self.turn_on_gpio("P9_41")
        self.turn_on_gpio("P9_42")

    def disable_all_dbus(self):
        #2- D-bus Disable
        self.turn_off_gpio("P8_6")
        self.turn_off_gpio("P8_12")
        self.turn_off_gpio("P8_14")
        self.turn_off_gpio("P8_16")
        self.turn_off_gpio("P8_18")
        self.turn_off_gpio("P8_20")
        self.turn_off_gpio("P8_22")
        self.turn_off_gpio("P8_24")
    
    def disable_all_LE(self):
        #3- LE Disable
        self.turn_off_gpio("P8_3")
        self.turn_off_gpio("P8_4")
        self.turn_off_gpio("P8_5")
        self.turn_off_gpio("P8_11")
        self.turn_off_gpio("P8_15")
        self.turn_off_gpio("P8_17")
        self.turn_off_gpio("P8_42")
        self.turn_off_gpio("P8_44")
        self.turn_off_gpio("P8_45")
        self.turn_off_gpio("P8_46")
        self.turn_off_gpio("P9_12")
        self.turn_off_gpio("P9_15")
        self.turn_off_gpio("P9_41")
        self.turn_off_gpio("P9_42")

    def turn_on_gpio(self, pin):
#       GPIO.setup(pin, GPIO.OUT)
#        GPIO.output(pin,GPIO.HIGH)
        print sys._getframe().f_code.co_name,
        print(' '+pin)
    
    def turn_off_gpio(self, pin):
#        GPIO.setup(pin, GPIO.OUT)
#        GPIO.output(pin,GPIO.LOW)
        print sys._getframe().f_code.co_name,
        print(' '+pin)

    def refresh_status(self, pin_pwm, pin_enable):
        '''
        '''
        self.turn_off_gpio(pin_pwm)
        #Disable all LE
        self.disable_all_LE()
        #
        self.turn_on_gpio(pin_enable)
        le_list = LE_DICT[pin_enable]
        for star in le_list:
            #print star
            star_sts = STAR_STATUS[star]
            if star_sts[1] == "OFF":
                self.turn_off_gpio(star_sts[0])
            else:
                self.turn_on_gpio(star_sts[0])
        self.turn_off_gpio(pin_enable)
        #Disable all LE
        self.disable_all_LE()
        #
        for key, value in STAR_STATUS.iteritems():
            if value[1] == "ON":
                msg = "\033[31m%s->%s\033[0m" % (str(key), str(value))
                print msg
            else:
                print key, value
                
    def led_on(self, pin_led, pin_pwm, pin_enable, name, simulated, exp_time, brightness):
        print "---------------------------------------------------"
        print "%s(%s,%s,%s)" % (name, pin_led, pin_pwm, pin_enable)
        print "-----------"
        STAR_STATUS[name][1] = "ON"
        self.refresh_status(pin_pwm, pin_enable)
        print "---------------------------------------------------"
        return "ok"

    def led_off(self, pin_led, pin_pwm, pin_enable, name, simulated, exp_time, brightness):
        print "---------------------------------------------------"
        print "%s(%s,%s,%s)" % (name, pin_led, pin_pwm, pin_enable)
        print "-----------"
        STAR_STATUS[name][1] = "OFF"
        self.refresh_status(pin_pwm, pin_enable)
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
