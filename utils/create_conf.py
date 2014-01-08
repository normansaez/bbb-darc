import csv

print "[beagledarc_server]"
print "host = 192.168.7.2"
print "user = root"
print "password = "
print "port = "
print "ior = IOR:010000001900000049444c3a4242425365727665722f5365727665723a312e3000000000010000000000000064000000010102000b00000031302e34322e302e3937000052e700000e000000fed0a5cc5200000b99000000000000000200000000000000080000000100000000545441010000001c00000001000000010001000100000001000105090101000100000009010100 "
print " "
print "[darc]"
print "camera = ShackHartmann"
print "pxlx = 1920"
print "pxly = 1080"
print "image_path = /home/dani/nsaez/images/"
print 

with open('mapping.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        if row[1].__contains__('m') and not row[1].__contains__('name'):
            if row[1] == 'm1':
                print "[ground_layer]"
                print "name = ground_layer"
            if row[1] == 'm2':
                print "[vertical_altitude_layer]"
                print "name = vertical_altitude_layer"
            if row[1] == 'm3':
                print "[horizontal_altitude_layer]"
                print "name = horizontal_altitude_layer"
            print "pin_dir = %s" % row[2]
            print "pin_step = %s" % row[3]
            print "pin_sleep = %s" % row[4]
            print "pin_opto1 = %s" % row[5]
            print "pin_opto2 = %s" % row[6]
            print "simulated = False"
            print "direction = INIT_POSITION"
            print "velocity = 57"
            print "steps = 50000"
            print "vr_init = 2"
            print "vr_end = 3"
            print "cur_pos = 0"
            print "image_prefix = %s" % row[1]
            print
        else:
            if row[0] == '100' or row[0] == '0' or row[0] == 'id' or row[0] == "":
                pass
            else:
                print "[led_%s]" % row[0]
                print "pin_led = %s" % row[2]
                print "pin_pwm = %s" % row[3]
                print "pin_enable = %s" % row[4]
                print "name = %s" % row[1]
                print "simulated = False"
                print "exp_time = 15000.0"
                print "brightness = 94"
                print "image_prefix = %s" % row[0]
                print

#import csv
#print "STAR_STATUS = {"
#with open('mapping.csv', 'rb') as csvfile:
#    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
#    for row in spamreader:
#        if row[1] == "name" or row[1].__contains__('m') or row[1] == "" or row[2] == "NA"  or row[2] == "GND":
#            pass
#        else:
#            print '"%s":["%s","%s"],' % (row[1],row[2],"OFF")
#print "}"
#
