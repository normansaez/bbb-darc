import sys

base = int(sys.argv[1])
offset = int(sys.argv[2])

gpio = base*32+offset

print "gpio%d_[%d] = %d" % (base, offset, gpio)
