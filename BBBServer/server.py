#
# The server
#

#!/usr/bin/env python

import sys, os
import CORBA, BBBServer, BBBServer__POA

class Server_i (BBBServer__POA.Server):
    def set_high(self, cmd):
        print cmd
        return cmd

    def set_low(self, cmd):
        print cmd
        return cmd

    def get_status(self, cmd):
        print cmd
        return cmd

orb = CORBA.ORB_init(sys.argv)
poa = orb.resolve_initial_references("RootPOA")

servant = Server_i()
poa.activate_object(servant)

print orb.object_to_string(servant._this())

poa._get_the_POAManager().activate()
orb.run()

