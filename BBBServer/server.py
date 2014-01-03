#
# The server
#

#!/usr/bin/env python

import sys, os
import CORBA, BBBServer, BBBServer__POA
#import Adafruit_BBIO.GPIO as GPIO
#import Adafruit_BBIO.PWM as PWM

class Server_i (BBBServer__POA.Server):
    def led_on(self, name, pin_led, pin_pwm, pin_enable):
        print "%s(%s,%s,%s)" % (name, pin_led, pin_pwm, pin_enable)
        print "preparing ..."
        GPIO.setup(pin_led, GPIO.OUT)
        GPIO.setup(pin_enable, GPIO.OUT)
        GPIO.output(pin_enable, GPIO.HIGH)
        GPIO.output(pin_led, GPIO.HIGH)
        PWM.start(pin_pwm, 50)
        PWM.set_duty_cycle(pin_pwm, 25.5)
        PWM.set_frequency(pin_pwm, 10)
        print "..."
        print "led on"
        return "ok"
    def led_off(self, name, pin_led, pin_pwm, pin_enable):
        print "%s(%s,%s,%s)" % (name, pin_led, pin_pwm, pin_enable)
        print "led off"
        return "ok"

    def motor_move(self, name, steps, vel, pin_dir, pin_step, pin_sleep, stat_der, stat_izq):
        print "%s(%s,%s,%s,%s,%s) => (%s, %s)" % (name, steps, vel, pin_dir, pin_step, pin_sleep, stat_der, stat_izq)
        print "motor move"
        return "ok"

orb = CORBA.ORB_init(sys.argv)
poa = orb.resolve_initial_references("RootPOA")

servant = Server_i()
poa.activate_object(servant)

#XXX Dirty hack to accomplish deadline
f = open('/tmp/IOR.txt','w')
f.write(orb.object_to_string(servant._this()))
print orb.object_to_string(servant._this())
f.close()

poa._get_the_POAManager().activate()
orb.run()

