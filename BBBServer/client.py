#
# The client, on the command line
#

import CORBA, BBBServer
from random import randint

orb = CORBA.ORB_init()
#o = orb.string_to_object("corbaloc::192.168.7.2/BBBServer")

#using dirty fix
f = open('/tmp/IOR.txt','r')
ior_ = f.readlines()
ior = ior_[0].split('\n')[0]
f.close()
#print ior
o = orb.string_to_object(ior)
name = 'lala'
pin_led = 'lele'
pin_pwm = 'lili'
pin_enable = 'lolo'
o.led_on(name, pin_led, pin_pwm, pin_enable)
 



