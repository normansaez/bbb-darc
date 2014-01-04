import csv
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
            print "pin_enable = %s" % row[4]
            print "pin_direction = %s" % row[2]
            print "pin_steps = %s" % row[3]
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

