#
# The server
#

#!/usr/bin/env python

import sys, os
import CORBA, BBBServer, BBBServer__POA
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
import getpass



LE_DICT = {"P8_3":1,
"P8_4":2,
"P8_5":3,
"P8_11":4,
"P8_15":5,
"P8_17":6,
"P8_42":7,
"P8_44":8,
"P8_45":9,
"P8_46":10,
"P9_12":11,
"P9_15":12,
"P9_41":13,
"P9_42":14}

LE_1  = ["LGS_B_12", "LGS_B_13", "LGS_B_20", "LGS_B_21","LGS_B_22","LGS_B_23","LGS_B_24", "LGS_B_25"]
LE_2  = ["LGS_B_4", "LGS_B_5", "LGS_B_6", "LGS_B_7","LGS_B_8","LGS_B_9","LGS_B_10", "LGS_B_11"]
LE_3  = ["LGS_A_4", "LGS_A_5", "LGS_A_6", "LGS_A_7","LGS_A_8","LGS_A_9","LGS_A_10", "LGS_A_11"]
LE_4  = ["NGS_A_4", "NGS_A_5", "NGS_A_6", "NGS_A_7","NGS_A_8","NGS_A_9","NGS_A_10", "NGS_A_11"]
LE_5  = ["NGS_A_12", "NGS_A_13", "NGS_A_20", "NGS_A_21","NGS_A_22","NGS_A_23","NGS_A_24", "NGS_A_25"]
LE_6  = ["LGS_C_10", "LGS_C_11", "LGS_C_12", "LGS_C_13","LGS_C_25"]
LE_7  = ["LGS_A_12", "LGS_A_13", "LGS_A_20", "LGS_A_21","LGS_A_22","LGS_A_23","LGS_A_24", "LGS_A_25"]
LE_8  = ["NGS_C_10", "NGS_C_11", "NGS_C_12", "NGS_C_13","NGS_C_25"]
LE_9  = ["LGS_A_1", "LGS_A_2", "LGS_A_3", "LGS_A_14","LGS_A_15","LGS_A_16","LGS_A_17", "LGS_A_18"]
LE_10  = ["LGS_B_1", "LGS_B_2", "LGS_B_3", "LGS_B_14","LGS_B_15","LGS_B_16","LGS_B_17", "LGS_B_18"]
LE_11  = ["NGS_B_4", "NGS_B_5", "NGS_B_6", "NGS_B_7","NGS_B_8","NGS_B_9","NGS_B_10", "NGS_B_11"]
LE_12  = ["NGS_B_12", "NGS_B_13", "NGS_B_20", "NGS_B_21","NGS_B_22","NGS_B_23","NGS_B_24", "NGS_B_25"]
LE_13  = ["NGS_B_1", "NGS_B_2", "NGS_B_3", "NGS_B_14","NGS_B_15","NGS_B_16","NGS_B_17", "NGS_B_18"]
LE_14  = ["NGS_A_1", "NGS_A_2", "NGS_A_3", "NGS_A_14","NGS_A_15","NGS_A_16","NGS_A_17", "NGS_A_18"]




class Server_i (BBBServer__POA.Server):

    def turn_off(self):    
        #0- PWM to LOW
        turn_off_gpio("P8_13")
        turn_off_gpio("P8_19")
        turn_off_gpio("P9_14")
        turn_off_gpio("P9_16")
        
        #1- LE Enable
        turn_on_gpio("P8_3")
        turn_on_gpio("P8_4")
        turn_on_gpio("P8_5")
        turn_on_gpio("P8_11")
        turn_on_gpio("P8_15")
        turn_on_gpio("P8_17")
        turn_on_gpio("P8_42")
        turn_on_gpio("P8_44")
        turn_on_gpio("P8_45")
        turn_on_gpio("P8_46")
        turn_on_gpio("P9_12")
        turn_on_gpio("P9_15")
        turn_on_gpio("P9_41")
        turn_on_gpio("P9_42")
    
        #2- D-bus Disable
        turn_off_gpio("P8_6")
        turn_off_gpio("P8_12")
        turn_off_gpio("P8_14")
        turn_off_gpio("P8_16")
        turn_off_gpio("P8_18")
        turn_off_gpio("P8_20")
        turn_off_gpio("P8_22")
        turn_off_gpio("P8_24")
    
        #3- LE Disable
        turn_off_gpio("P8_3")
        turn_off_gpio("P8_4")
        turn_off_gpio("P8_5")
        turn_off_gpio("P8_11")
        turn_off_gpio("P8_15")
        turn_off_gpio("P8_17")
        turn_off_gpio("P8_42")
        turn_off_gpio("P8_44")
        turn_off_gpio("P8_45")
        turn_off_gpio("P8_46")
        turn_off_gpio("P9_12")
        turn_off_gpio("P9_15")
        turn_off_gpio("P9_41")
        turn_off_gpio("P9_42")

    def turn_on_gpio(self, pin):
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin,GPIO.HIGH)
        print sys._getframe().f_code.co_name,
        print(' '+pin)
    
    def turn_off_gpio(self, pin):
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin,GPIO.LOW)
        print sys._getframe().f_code.co_name,
        print(' '+pin)

    def refresh_status(pin_pwm, pin_enable, pin_led):
        '''
        '''
        turn_on_gpio(pin_pwm)
        turn_on_gpio(pin_enable)
        le_list = "LE_%d" % LE_DICT[pin_enable]
        for star in eval(le_list):
            sts = STATUS[star]
            if sts = "OFF":
                turn_off_gpio(pin_led)
            else:
        turn_off_gpio(pin_enable)

    def on(self, pin_led, pin_pwm, pin_enable, name, simulated, exp_time, brightness):
        STATUS[name] = "ON"
        self.refresh_status(pin_pwm, pin_enable, pin_led)
        return "ok"

    def led_off(self, pin_led, pin_pwm, pin_enable, name, simulated, exp_time, brightness):
        print "%s(%s,%s,%s)" % (name, pin_led, pin_pwm, pin_enable)
        print "led off"
        return "ok"

    def motor_move(self, name, pin_dir, pin_step, pin_sleep, pin_opto1, pin_opto2, simulated, direction, velocity, steps, vr_init, vr_end, cur_pos):
        print "motor move"
        return "ok"

    def motor_move_skip_sensor(self, name, pin_dir, pin_step, pin_sleep, pin_opto1, pin_opto2, simulated, direction, velocity, steps, vr_init, vr_end, cur_pos):
        print "motor move"
        return "ok"
if __name__ == '__main__':
    if getpass.getuser() == 'root':
        orb = CORBA.ORB_init(sys.argv)
        poa = orb.resolve_initial_references("RootPOA")
        
        servant = Server_i()
        poa.activate_object(servant)
        
        #XXX DIRTY workaround to carry out with deadline
        f = open('/tmp/IOR.txt','w')
        f.write(orb.object_to_string(servant._this()))
        print orb.object_to_string(servant._this())
        f.close()
        
        poa._get_the_POAManager().activate()
        orb.run()
    else:
        print "The server should run as root!!:\nsudo su -\npython\
        /home/ubuntu/bbb-darc/BBBServer/server.py"
