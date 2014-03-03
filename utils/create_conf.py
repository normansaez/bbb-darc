import csv
import os
from sets import Set

filename_cfg = "configurations.cfg"
filename_dic = "server_dic.py"

filehandler_cfg = open(filename_cfg, 'w')
filehandler_dic = open(filename_dic, 'w')

filehandler_cfg.write("[beagledarc_server]\n")
filehandler_cfg.write("host = 192.168.7.2\n")
filehandler_cfg.write("user = root\n")
filehandler_cfg.write("password = \n")
filehandler_cfg.write("port = \n")
filehandler_cfg.write("ior = IOR:010000001900000049444c3a4242425365727665722f5365727665723a312e3000000000010000000000000064000000010102000b00000031302e34322e302e3937000052e700000e000000fed0a5cc5200000b99000000000000000200000000000000080000000100000000545441010000001c00000001000000010001000100000001000105090101000100000009010100 \n")
filehandler_cfg.write("\n")
filehandler_cfg.write("[darc]\n")
filehandler_cfg.write("camera = ShackHartmann\n")
filehandler_cfg.write("pxlx = 1920\n")
filehandler_cfg.write("pxly = 1080\n")
filehandler_cfg.write("image_path = /home/dani/nsaez/images/\n")
filehandler_cfg.write("\n")

with open('mapping.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        if row[1].__contains__('m') and not row[1].__contains__('name'):
            if row[1] == 'm1':
                filehandler_cfg.write("[ground_layer]\n")
                filehandler_cfg.write("name = ground_layer\n")
            if row[1] == 'm2':
                filehandler_cfg.write("[vertical_altitude_layer]\n")
                filehandler_cfg.write("name = vertical_altitude_layer\n")
            if row[1] == 'm3':
                filehandler_cfg.write("[horizontal_altitude_layer]\n")
                filehandler_cfg.write("name = horizontal_altitude_layer\n")
            filehandler_cfg.write("pin_dir = %s\n" % row[2])
            filehandler_cfg.write("pin_step = %s\n" % row[3])
            filehandler_cfg.write("pin_sleep = %s\n" % row[4])
            filehandler_cfg.write("pin_opto1 = %s\n" % row[5])
            filehandler_cfg.write("pin_opto2 = %s\n" % row[6])
            filehandler_cfg.write("simulated = False\n")
            filehandler_cfg.write("direction = INIT_POSITION\n")
            filehandler_cfg.write("velocity = 57\n")
            filehandler_cfg.write("steps = 50000\n")
            filehandler_cfg.write("vr_init = 0\n")
            filehandler_cfg.write("vr_end = 21000\n")
            filehandler_cfg.write("cur_pos = 0\n")
            filehandler_cfg.write("image_prefix = %s\n" % row[1])
            filehandler_cfg.write("\n")
        else:
            if row[0] == '100' or row[0] == '0' or row[0] == 'id' or row[0] == "":
                pass
            else:
                filehandler_cfg.write("[led_%s]\n" % row[0])
                filehandler_cfg.write("pin_led = %s\n" % row[2])
                filehandler_cfg.write("pin_pwm = %s\n" % row[3])
                filehandler_cfg.write("pin_enable = %s\n" % row[4])
                filehandler_cfg.write("name = %s\n" % row[1])
                filehandler_cfg.write("simulated = False\n")
                filehandler_cfg.write("exp_time = 15000.0\n")
                filehandler_cfg.write("brightness = 94\n")
                filehandler_cfg.write("image_prefix = %s\n" % row[0])
                filehandler_cfg.write("\n")
                
filehandler_cfg.close()

filehandler_dic.write("STAR_STATUS = {")
lines = ""
with open('mapping.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        if row[1] == "name" or row[1].__contains__('m') or row[1] == "" or row[2] == "NA"  or row[2] == "GND":
            pass
        else:
            lines += '"%s":["%s","%s"],\n' % (row[1],row[2],"OFF")
lines += "}\n"
lines = lines.replace(",\n}","}")
filehandler_dic.write(lines)
filehandler_dic.write("\n\n")

#Generate LE_DICT
filehandler_dic.write("LE_DICT = {")

le_set = Set([])
le_set_dbus0  = Set([])
le_set_dbus1  = Set([])
le_set_dbus2  = Set([])
le_set_dbus3  = Set([])
le_set_dbus4  = Set([])
le_set_dbus5  = Set([])
le_set_dbus6  = Set([])
le_set_dbus7  = Set([])
le_set_dbus8  = Set([])
le_set_dbus9  = Set([])
le_set_dbus10 = Set([])
le_set_dbus11 = Set([])
le_set_dbus12 = Set([])
le_set_dbus13 = Set([])

with open('mapping.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        if row[1] == "name" or row[1].__contains__('m') or row[1] == "" or row[2] == "NA"  or row[2] == "GND":
            pass
        else:
            le_set.add(row[4])

le_list = list(sorted(le_set))

with open('mapping.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        if row[1] == "name" or row[1].__contains__('m') or row[1] == "" or row[2] == "NA"  or row[2] == "GND":
            pass
        else:
            if le_list[0] == row[4]:
                le_set_dbus0.add(row[1])                
            if le_list[1] == row[4]:
                le_set_dbus1.add(row[1])                
            if le_list[2] == row[4]:
                le_set_dbus2.add(row[1])                
            if le_list[3] == row[4]:
                le_set_dbus3.add(row[1])                
            if le_list[4] == row[4]:
                le_set_dbus4.add(row[1])                
            if le_list[5] == row[4]:
                le_set_dbus5.add(row[1])                
            if le_list[6] == row[4]:
                le_set_dbus6.add(row[1])                
            if le_list[7] == row[4]:
                le_set_dbus7.add(row[1])                
            if le_list[8] == row[4]:
                le_set_dbus8.add(row[1])                
            if le_list[9] == row[4]:
                le_set_dbus9.add(row[1])                
            if le_list[10] == row[4]:
                le_set_dbus10.add(row[1])                
            if le_list[11] == row[4]:
                le_set_dbus11.add(row[1])                
            if le_list[12] == row[4]:
                le_set_dbus12.add(row[1])                
            if le_list[13] == row[4]:
                le_set_dbus13.add(row[1])                

l0 = "'%s':%s,\n" % (le_list[0], sorted(le_set_dbus0))
l0 = l0.replace('Set(','').replace(')','')
filehandler_dic.write(l0)

l1 = "'%s':%s,\n" % (le_list[1], sorted(le_set_dbus1))
l1 = l1.replace('Set(','').replace(')','')
filehandler_dic.write(l1)

l2 = "'%s':%s,\n" % (le_list[2], sorted(le_set_dbus2))
l2 = l2.replace('Set(','').replace(')','')
filehandler_dic.write(l2)

l3 = "'%s':%s,\n" % (le_list[3], sorted(le_set_dbus3))
l3 = l3.replace('Set(','').replace(')','')
filehandler_dic.write(l3)

l4 = "'%s':%s,\n" % (le_list[4], sorted(le_set_dbus4))
l4 = l4.replace('Set(','').replace(')','')
filehandler_dic.write(l4)

l5 = "'%s':%s,\n" % (le_list[5], sorted(le_set_dbus5))
l5 = l5.replace('Set(','').replace(')','')
filehandler_dic.write(l5)

l6 = "'%s':%s,\n" % (le_list[6], sorted(le_set_dbus6))
l6 = l6.replace('Set(','').replace(')','')
filehandler_dic.write(l6)

l7 = "'%s':%s,\n" % (le_list[7], sorted(le_set_dbus7))
l7 = l7.replace('Set(','').replace(')','')
filehandler_dic.write(l7)

l8 = "'%s':%s,\n" % (le_list[8], sorted(le_set_dbus8))
l8 = l8.replace('Set(','').replace(')','')
filehandler_dic.write(l8)

l9 = "'%s':%s,\n" % (le_list[9], sorted(le_set_dbus9))
l9 = l9.replace('Set(','').replace(')','')
filehandler_dic.write(l9)

l10 = "'%s':%s,\n" % (le_list[10], sorted(le_set_dbus10))
l10 = l10.replace('Set(','').replace(')','')
filehandler_dic.write(l10)

l11 = "'%s':%s,\n" % (le_list[11], sorted(le_set_dbus11))
l11 = l11.replace('Set(','').replace(')','')
filehandler_dic.write(l11)

l12 = "'%s':%s,\n" % (le_list[12], sorted(le_set_dbus12))
l12 = l12.replace('Set(','').replace(')','')
filehandler_dic.write(l12)

l13 = "'%s':%s}\n" % (le_list[13], sorted(le_set_dbus13))
l13 = l13.replace('Set(','').replace(')','')
filehandler_dic.write(l13)


filehandler_dic.close()

os.rename(filename_cfg,"../BeagleDarc/BeagleDarc/%s"%filename_cfg)
os.rename(filename_dic,"../BBBServer/%s"%filename_dic)
