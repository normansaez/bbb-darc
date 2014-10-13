import csv
import os
from sets import Set

filename_cfg = "configurations.cfg"
filename_dic = "server_dic.py"

filehandler_cfg = open(filename_cfg, 'w')
filehandler_dic = open(filename_dic, 'w')

le_set = Set([])
pwm_set = Set([])
dbus_set = Set([])

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

#Creating configuration:
filehandler_cfg.write("[beagledarc_server]\n")
filehandler_cfg.write("host = 10.42.0.97\n")
filehandler_cfg.write("user = root\n")
filehandler_cfg.write("password = \n")
filehandler_cfg.write("port = \n")

filehandler_cfg.write("\n")
filehandler_cfg.write("[pike]\n")
filehandler_cfg.write("name = pike\n")
filehandler_cfg.write("pxlx = 1920\n")
filehandler_cfg.write("pxly = 1080\n")
filehandler_cfg.write("image_path = /home/dani/BeagleAcquisition/Pike/\n")
filehandler_cfg.write("bg_path = /home/dani/BeagleAcquisition/Pike/BG/\n")
filehandler_cfg.write("subaplocation_path = /home/dani/BeagleAcquisition/Pike/subapLocation/\n")
filehandler_cfg.write("rawdata_path = /home/dani/BeagleAcquisition/Pike/RawData/\n")
filehandler_cfg.write("refcent_path = /home/dani/BeagleAcquisition/Pike/RefCent/\n")
filehandler_cfg.write("subapflag = /home/dani/git/canaryLaserCommissioning/subapFlag.fits\n")
filehandler_cfg.write("exptime = fwShutter\n")
filehandler_cfg.write("shutter = fwShutter\n")
filehandler_cfg.write("usebrightest = -85\n")
filehandler_cfg.write("bg_iter = 100\n")
filehandler_cfg.write("maxexptime = 4095.0\n")
filehandler_cfg.write("initexptime = 1228.0\n")
filehandler_cfg.write("nstars = 53\n")
filehandler_cfg.write("nsubaps = 208\n")
filehandler_cfg.write("allsubaps = 256\n")
filehandler_cfg.write("saturation = 65532.0\n")
filehandler_cfg.write("xwidth = 42\n")
filehandler_cfg.write("ywidth = 42\n")
filehandler_cfg.write("xgap = 37\n")
filehandler_cfg.write("ygap = 37\n")
filehandler_cfg.write("fwhm = 6\n")

filehandler_cfg.write("\n")
filehandler_cfg.write("[sbig]\n")
filehandler_cfg.write("name = sbig\n")
filehandler_cfg.write("pxlx = 765\n")
filehandler_cfg.write("pxly = 510\n")
filehandler_cfg.write("image_path = /home/dani/BeagleAcquisition/SBIG/\n")
filehandler_cfg.write("bg_path = /home/dani/BeagleAcquisition/SBIG/BG/\n")
filehandler_cfg.write("subaplocation_path = /home/dani/BeagleAcquisition/SBIG/subapLocation/\n")
filehandler_cfg.write("rawdata_path = /home/dani/BeagleAcquisition/SBIG/RawData/\n")
filehandler_cfg.write("refcent_path = /home/dani/BeagleAcquisition/SBIG/RefCent/\n")
filehandler_cfg.write("subapflag = /home/dani/git/canaryLaserCommissioning/subapFlag.fits\n")
filehandler_cfg.write("exptime = sbigExpTime\n")
filehandler_cfg.write("shutter = sbigShutter\n")
filehandler_cfg.write("usebrightest = -85\n")
filehandler_cfg.write("bg_iter = 100\n")
filehandler_cfg.write("maxexptime = 360000\n")
filehandler_cfg.write("initexptime = 6.0\n")
filehandler_cfg.write("nstars = 53\n")
filehandler_cfg.write("nsubaps = 208\n")
filehandler_cfg.write("allsubaps = 256\n")
filehandler_cfg.write("saturation = 65532.0\n")
filehandler_cfg.write("xwidth = 34\n")
filehandler_cfg.write("ywidth = 34\n")
filehandler_cfg.write("xgap = 30\n")
filehandler_cfg.write("ygap = 30\n")
filehandler_cfg.write("fwhm = 5\n")

filehandler_cfg.write("\n")

with open('mapping.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
    for row in spamreader:
        if row[1].__contains__('m') and not row[1].__contains__('name'):
            if row[1] == 'm1':
                filehandler_cfg.write("[vertical_altitude_layer]\n")
                filehandler_cfg.write("name = vertical_altitude_layer\n")
            if row[1] == 'm2':
                filehandler_cfg.write("[ground_layer]\n")
                filehandler_cfg.write("name = ground_layer\n")
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
            filehandler_cfg.write("pos_dir = %s\n" % row[7])
            filehandler_cfg.write("velocity = 57\n")
            filehandler_cfg.write("steps = 50000\n")
            filehandler_cfg.write("vr_init = 0\n")
            filehandler_cfg.write("vr_end = %s\n" % row[8])
            filehandler_cfg.write("cmd_pos = 0\n")
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
                filehandler_cfg.write("slope_iter = 10\n")
                if row[5] == '1':
                    filehandler_cfg.write("valid = True\n")
                else:
                    filehandler_cfg.write("valid = False\n")
                filehandler_cfg.write("image_prefix = %s\n" % row[0])
                filehandler_cfg.write("\n")
                
filehandler_cfg.close()

#Creating dictionaries and lists:
filehandler_dic.write("LED_STATUS = {")
lines = ""
with open('mapping.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
    for row in spamreader:
        if row[1] == "name" or row[1].__contains__('m') or row[1] == "" or row[2] == "NA"  or row[2] == "GND":
            pass
        else:
            lines += '"%s":["%s","%s","%s"],\n' % (row[1],row[2],"OFF", row[0])
            le_set.add(row[4])
            pwm_set.add(row[3])
            dbus_set.add(row[2])
lines += "}\n"
lines = lines.replace(",\n}","}")
filehandler_dic.write(lines)
filehandler_dic.write("\n\n")

le_list = list(sorted(le_set))
pwm_list = list(sorted(pwm_set))
dbus_list = list(sorted(dbus_set))

#Generate LE_DICT
filehandler_dic.write("LE_DICT = {")
with open('mapping.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
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

#Generate PWM_LIST
filehandler_dic.write("\n\nPWM_LIST = ")
filehandler_dic.write("%s"% pwm_list)
filehandler_dic.write("\n")

#Generate DBUS_LIST
filehandler_dic.write("\n\nDBUS_LIST = ")
filehandler_dic.write("%s"% dbus_list)
filehandler_dic.write("\n")

filehandler_dic.close()

os.rename(filename_cfg,"../BeagleDarc/BeagleDarc/%s"%filename_cfg)
os.rename(filename_dic,"../BBBServer/%s"%filename_dic)
