#
# The server
#

#!/usr/bin/env python

import sys, os
import CORBA, BBBServer, BBBServer__POA
from time import sleep
from random import randint

class Server_i (BBBServer__POA.Server):
    def led_on(pin_led, pin_pwm, pin_enable):
        print "led on"

    def led_off(pin_led, pin_pwm, pin_enable):
        print "led off"

    def motor_move(pin_dir, pin_step, pin_sleep, stat_der, stat_izq):
        print "motor move"

orb = CORBA.ORB_init(sys.argv)
poa = orb.resolve_initial_references("RootPOA")

servant = Server_i()
poa.activate_object(servant)

print orb.object_to_string(servant._this())

poa._get_the_POAManager().activate()
orb.run()

