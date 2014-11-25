from __future__ import print_function
import sys

import Pyro4


if sys.version_info < (3, 0):
    input = raw_input

with Pyro4.core.Proxy("PYRONAME:bbb.server") as proxy:
    proxy.flush_all_leds()
