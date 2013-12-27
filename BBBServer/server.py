#
# The server
#

#!/usr/bin/env python

import sys, os
import CORBA, BBBServer, BBBServer__POA
from time import sleep
from random import randint

class Server_i (BBBServer__POA.Server):
    def set_high(self, cmd):
        print cmd
        s = randint(1,40)
        print sys._getframe().f_code.co_name, 
        print " sleeping %d" % s
        sleep(s)
        return cmd

    def set_low(self, cmd):
        print cmd
        s = randint(1,40)
        print sys._getframe().f_code.co_name, 
        print "sleeping %d" % s
        sleep(s)
        return cmd

    def get_status(self, cmd):
        print cmd
        s = randint(1,40)
        print sys._getframe().f_code.co_name, 
        print "sleeping %d" % s
        sleep(s)
        return cmd

orb = CORBA.ORB_init(sys.argv)
poa = orb.resolve_initial_references("RootPOA")

servant = Server_i()
poa.activate_object(servant)

print orb.object_to_string(servant._this())

poa._get_the_POAManager().activate()
orb.run()

