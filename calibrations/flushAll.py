from BeagleDarc.Controller import Controller
import ConfigParser


bbbc = Controller()
for s in range(1,54+1):
    try:
        print "s->%d on" % s
        bbbc.star_on(s)
        print "s->%d off" % s
        bbbc.star_off(s)
    except ConfigParser.NoSectionError:
        pass
