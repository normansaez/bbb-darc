#
# The client, on the command line
#

import CORBA, BBBServer
from random import randint

orb = CORBA.ORB_init()
#o = orb.string_to_object("corbaloc::192.168.7.2/BBBServer")

#using dirty fix
#f = open('/tmp/IOR.txt','r')
#ior_ = f.readlines()
#ior = ior_[0].split('\n')[0]
#f.close()
#print ior
o = orb.string_to_object('IOR:010000001900000049444c3a4242425365727665722f5365727665723a312e3000000000010000000000000064000000010102000e0000003134362e3135352e31342e313200538c0e000000fe4297cc5200000b40000000000000000200000000000000080000000100000000545441010000001c00000001000000010001000100000001000105090101000100000009010100')
o.led_on('P8_20', 'P8_19', 'P8_45', 'LGS_A_1', False, 1.0, 1)
raw_input()
 



