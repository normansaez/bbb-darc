#
# The client, on the command line
#

import CORBA, BBBServer
from random import randint

orb = CORBA.ORB_init()
#o = orb.string_to_object("corbaloc::192.168.7.2/BBBServer")
o = orb.string_to_object('IOR:010000001900000049444c3a4242425365727665722f5365727665723a312e3000000000010000000000000064000000010102000d0000003139322e3136382e302e31300000f8810e000000fe43e6bd52000005d8000000000000000200000000000000080000000100000000545441010000001c00000001000000010001000100000001000105090101000100000009010100')
#s = raw_input()
s = randint(0,2)
if s == 0:
    print o.get_status('status --> %d'% s) 
if s == 1:
    print o.set_low('status --> %d'% s) 

if s == 2:
    print o.set_high('status --> %d'% s) 

