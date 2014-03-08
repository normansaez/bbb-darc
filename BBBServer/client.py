#!/usr/bin/env python
import sys
from omniORB import CORBA
from random import randint
import CosNaming, BBBServer

# Initialise the ORB
orb = CORBA.ORB_init(sys.argv, CORBA.ORB_ID)

# Obtain a reference to the root naming context
obj         = orb.resolve_initial_references("NameService")
rootContext = obj._narrow(CosNaming.NamingContext)

if rootContext is None:
    print "Failed to narrow the root naming context"
    sys.exit(1)

# Resolve the name "BeagleBone.Server/BBBServer.Object"
name = [CosNaming.NameComponent("BeagleBone", "Server"),
        CosNaming.NameComponent("BBBServer", "Object")]
try:
    obj = rootContext.resolve(name)

except CosNaming.NamingContext.NotFound, ex:
    print "Name not found"
    sys.exit(1)

# Narrow the object to an BBBServer::Server
eo = obj._narrow(BBBServer.Server)

if (eo is None):
    print "Object reference is not an BBBServer::Server"
    sys.exit(1)

result  = eo.led_on('P8_20', 'P8_19', 'P8_45', 'LGS_A_1', False, 1.0, 1)

print eo.get_stars_status_keys()
print eo.get_stars_status_value('LGS_B_4')
name = 'ground_layer'
direction = 'INIT_POSITION'
velocity = 0
steps = 1000
cur_pos = 1
cmd_pos = 3
print eo.motor_move(name, direction, velocity, steps, cur_pos, cmd_pos)
print eo.motor_move_skip_sensor(name, direction, velocity, steps, cur_pos, cmd_pos)

