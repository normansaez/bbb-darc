#!/usr/bin/env python

import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
from time import sleep
import sys
import turn_off_all

def turn_on_gpio(pin):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin,GPIO.HIGH)
    print sys._getframe().f_code.co_name,
    print(' '+pin)
    #raw_input('press a key to continue')

def turn_off_gpio(pin):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin,GPIO.LOW)
    print sys._getframe().f_code.co_name,
    print(' '+pin)
    #raw_input('press a key to continue')

def turn_on_pwm(pin):
    PWM.start(pin, 50)
    PWM.set_duty_cycle(pin, 25.5)
    PWM.set_frequency(pin, 10)
    print sys._getframe().f_code.co_name,
    print(' '+pin)
    raw_input('press a key to continue')

def turn_off_pwm(pin):
    PWM.stop(pin)
    PWM.cleanup()
    print sys._getframe().f_code.co_name,
    print(' '+pin)
    raw_input('press a key to continue')

if __name__ == '__main__':
    timeout = 3 #secs
    
    turn_off_all.turn_off()
    # Se prende NGS-A1
    print ('\nstart to turn on PWM ...')
    turn_off_gpio('P9_14')
    turn_off_gpio('P8_13')
    turn_off_gpio('P9_16')
    turn_off_gpio('P8_19')
    print ('\nstart to turn on LE ...')
    turn_on_gpio('P9_42')
    # Lo siguiente se comenta asumiendo que el estado  de 
    # cualquier pata LE es por defecto LOW
    #turn_off_gpio('P8_5')
    #turn_off_gpio('P8_42')
    #turn_off_gpio('P8_46')
    #turn_off_gpio('P8_4')
    #turn_off_gpio('P8_3')
    #turn_off_gpio('P8_17')
    print ('\nstart to turn on PIN ...')
    turn_on_gpio('P8_20')
    turn_off_gpio('P8_22')
    turn_off_gpio('P8_24')
    turn_off_gpio('P8_18')
    turn_off_gpio('P8_16')
    turn_off_gpio('P8_14')
    turn_off_gpio('P8_12')
    turn_off_gpio('P8_6')
    raw_input('press a key to continue')

    #NGS-A2
    turn_off_gpio("P8_20")
    turn_on_gpio("P8_22")
    raw_input('press a key to continue')

    #NGS-A3
    turn_off_gpio("P8_22")
    turn_on_gpio("P8_24")
    raw_input('press a key to continue')

    #NGS-A4
    turn_off_gpio("P8_24")
    turn_off_gpio("P9_42")
    turn_on_gpio("P8_11")
    turn_on_gpio("P8_6")
    raw_input('press a key to continue')

    #NGS-A5
    turn_off_gpio("P8_6")
    turn_on_gpio("P8_12")
    raw_input('press a key to continue')

    #NGS-A6
    turn_off_gpio("P8_12")
    turn_on_gpio("P8_14")
    raw_input('press a key to continue')

    #NGS-A7
    turn_off_gpio("P8_14")
    turn_on_gpio("P8_16")
    raw_input('press a key to continue')

    #NGS-A8
    turn_off_gpio("P8_16")
    turn_on_gpio("P8_18")
    raw_input('press a key to continue')

    #NGS-A9
    turn_off_gpio("P8_18")
    turn_on_gpio("P8_20")
    raw_input('press a key to continue')

    #NGS-A10
    turn_off_gpio("P8_20")
    turn_on_gpio("P8_22")
    raw_input('press a key to continue')

    #NGS-A11
    turn_off_gpio("P8_22")
    turn_on_gpio("P8_24")
    raw_input('press a key to continue')

    #NGS-A12
    turn_off_gpio("P8_24")
    turn_off_gpio("P8_11")
    turn_on_gpio("P8_15")
    turn_on_gpio("P8_6")
    raw_input('press a key to continue')

    #NGS-A13
    turn_off_gpio("P8_6")
    turn_on_gpio("P8_12")
    raw_input('press a key to continue')

    #NGS-A14
    turn_off_gpio("P8_12")
    turn_off_gpio("P8_15")
    turn_on_gpio("P9_42")
    turn_on_gpio("P8_18")
    raw_input('press a key to continue')

    #NGS-A15
    turn_off_gpio("P8_18")
    turn_on_gpio("P8_16")
    raw_input('press a key to continue')

    #NGS-A16
    turn_off_gpio("P8_16")
    turn_on_gpio("P8_14")
    raw_input('press a key to continue')

    #NGS-A17
    turn_off_gpio("P8_14")
    turn_on_gpio("P8_12")
    raw_input('press a key to continue')

    #NGS-A18
    turn_off_gpio("P8_12")
    turn_on_gpio("P8_6")
    raw_input('press a key to continue')

    #NGS-A20
    turn_off_gpio("P8_6")
    turn_off_gpio("P9_42")
    turn_on_gpio("P8_15")
    turn_on_gpio("P8_24")
    raw_input('press a key to continue')

    #NGS-A21
    turn_off_gpio("P8_24")
    turn_on_gpio("P8_22")
    raw_input('press a key to continue')

    #NGS-A22
    turn_off_gpio("P8_22")
    turn_on_gpio("P8_20")
    raw_input('press a key to continue')

    #NGS-A23
    turn_off_gpio("P8_20")
    turn_on_gpio("P8_18")
    raw_input('press a key to continue')

    #NGS-A24
    turn_off_gpio("P8_18")
    turn_on_gpio("P8_16")
    raw_input('press a key to continue')

    #NGS-A25
    turn_off_gpio("P8_16")
    turn_on_gpio("P8_14")
    raw_input('press a key to continue')

    #NGS-B1
    turn_off_all.turn_off()
    turn_on_gpio("P9_41")
    turn_on_gpio("P8_14")
    raw_input("press a key to continue")

    #NGS-B2
    turn_off_gpio("P8_14")
    turn_on_gpio("P8_12")
    raw_input('press a key to continue')

    #NGS-B3
    turn_off_gpio("P8_12")
    turn_on_gpio("P8_6")
    raw_input('press a key to continue')

    #NGS-B4
    turn_off_all.turn_off()
    turn_on_gpio("P9_12")
    turn_on_gpio("P8_24")
    raw_input('press a key to continue')

    #NGS-B5
    turn_off_gpio("P8_24")
    turn_on_gpio("P8_22")
    raw_input('press a key to continue')

    #NGS-B6
    turn_off_gpio("P8_22")
    turn_on_gpio("P8_20")
    raw_input('press a key to continue')

    #NGS-B7
    turn_off_gpio("P8_20")
    turn_on_gpio("P8_18")
    raw_input('press a key to continue')

    #NGS-B8
    turn_off_gpio("P8_18")
    turn_on_gpio("P8_16")
    raw_input('press a key to continue')

    #NGS-B9
    turn_off_gpio("P8_16")
    turn_on_gpio("P8_14")
    raw_input('press a key to continue')

    #NGS-B10
    turn_off_gpio("P8_14")
    turn_on_gpio("P8_12")
    raw_input('press a key to continue')

    #NGS-B11
    turn_off_gpio("P8_12")
    turn_on_gpio("P8_6")
    raw_input('press a key to continue')

    #NGS-B12
    turn_off_all.turn_off()
    turn_on_gpio("P9_15")
    turn_on_gpio("P8_24")
    raw_input('press a key to continue')

    #NGS-B13
    turn_off_gpio("P8_24")
    turn_on_gpio("P8_22")
    raw_input('press a key to continue')

    #NGS-B14
    turn_off_all.turn_off()
    turn_on_gpio("P9_41")
    turn_on_gpio("P8_16")
    raw_input('press a key to continue')

    #NGS-B15
    turn_off_gpio("P8_16")
    turn_on_gpio("P8_18")
    raw_input('press a key to continue')

    #NGS-B16
    turn_off_gpio("P8_18")
    turn_on_gpio("P8_20")
    raw_input('press a key to continue')

    #NGS-B17
    turn_off_gpio("P8_20")
    turn_on_gpio("P8_22")
    raw_input('press a key to continue')

    #NGS-B18
    turn_off_gpio("P8_22")
    turn_on_gpio("P8_24")
    raw_input('press a key to continue')

    #NGS-B20
    turn_off_all.turn_off()
    turn_on_gpio("P9_15")
    turn_on_gpio("P8_6")
    raw_input('press a key to continue')

    #NGS-B21
    turn_off_gpio("P8_6")
    turn_on_gpio("P8_12")
    raw_input('press a key to continue')

    #NGS-B22
    turn_off_gpio("P8_12")
    turn_on_gpio("P8_14")
    raw_input('press a key to continue')

    #NGS-B23
    turn_off_gpio("P8_14")
    turn_on_gpio("P8_16")
    raw_input('press a key to continue')

    #NGS-B24
    turn_off_gpio("P8_16")
    turn_on_gpio("P8_18")
    raw_input('press a key to continue')

    #NGS-B25
    turn_off_gpio("P8_18")
    turn_on_gpio("P8_20")
    raw_input('press a key to continue')

    #NGS-C10
    turn_off_all.turn_off()
    turn_on_gpio("P8_44")
    turn_on_gpio("P8_18")
    raw_input("press a key to continue")

    #NGS-C11
    turn_off_gpio("P8_18")
    turn_on_gpio("P8_16")
    raw_input('press a key to continue')

    #NGS-C12
    turn_off_gpio("P8_16")
    turn_on_gpio("P8_14")
    raw_input('press a key to continue')

    #NGS-C13
    turn_off_gpio("P8_14")
    turn_on_gpio("P8_12")
    raw_input('press a key to continue')

    #NGS-C25
    turn_off_gpio("P8_12")
    turn_on_gpio("P8_6")
    raw_input('Press enter to go for LGS-A1')

#######################

    #LGS-A1
    turn_off_all.turn_off()
    turn_on_gpio("P8_45")
    turn_on_gpio("P8_20")
    raw_input('press a key to continue')

    #LGS-A2
    turn_off_gpio("P8_20")
    turn_on_gpio("P8_22")
    raw_input('press a key to continue')

    #LGS-A3
    turn_off_gpio("P8_22")
    turn_on_gpio("P8_24")
    raw_input('press a key to continue')

    #LGS-A4
    turn_off_all.turn_off()
    turn_on_gpio("P8_5")
    turn_on_gpio("P8_6")
    raw_input('press a key to continue')

    #LGS-A5
    turn_off_gpio("P8_6")
    turn_on_gpio("P8_12")
    raw_input('press a key to continue')

    #LGS-A6
    turn_off_gpio("P8_12")
    turn_on_gpio("P8_14")
    raw_input('press a key to continue')

    #LGS-A7
    turn_off_gpio("P8_14")
    turn_on_gpio("P8_16")
    raw_input('press a key to continue')

    #LGS-A8
    turn_off_gpio("P8_16")
    turn_on_gpio("P8_18")
    raw_input('press a key to continue')

    #LGS-A9
    turn_off_gpio("P8_18")
    turn_on_gpio("P8_20")
    raw_input('press a key to continue')

    #LGS-A10
    turn_off_gpio("P8_20")
    turn_on_gpio("P8_22")
    raw_input('press a key to continue')

    #LGS-A11
    turn_off_gpio("P8_22")
    turn_on_gpio("P8_24")
    raw_input('press a key to continue')

    #LGS-A12
    turn_off_all.turn_off()
    turn_on_gpio("P8_42")
    turn_on_gpio("P8_6")
    raw_input('press a key to continue')

    #LGS-A13
    turn_off_gpio("P8_6")
    turn_on_gpio("P8_12")
    raw_input('press a key to continue')

    #LGS-A14
    turn_off_all.turn_off()
    turn_on_gpio("P8_45")
    turn_on_gpio("P8_18")
    raw_input('press a key to continue')

    #LGS-A15
    turn_off_gpio("P8_18")
    turn_on_gpio("P8_16")
    raw_input('press a key to continue')

    #LGS-A16
    turn_off_gpio("P8_16")
    turn_on_gpio("P8_14")
    raw_input('press a key to continue')

    #LGS-A17
    turn_off_gpio("P8_14")
    turn_on_gpio("P8_12")
    raw_input('press a key to continue')

    #LGS-A18
    turn_off_gpio("P8_12")
    turn_on_gpio("P8_6")
    raw_input('press a key to continue')

    #LGS-A20
    turn_off_all.turn_off()
    turn_on_gpio("P8_42")
    turn_on_gpio("P8_24")
    raw_input('press a key to continue')

    #LGS-A21
    turn_off_gpio("P8_24")
    turn_on_gpio("P8_22")
    raw_input('press a key to continue')

    #LGS-A22
    turn_off_gpio("P8_22")
    turn_on_gpio("P8_20")
    raw_input('press a key to continue')

    #LGS-A23
    turn_off_gpio("P8_20")
    turn_on_gpio("P8_18")
    raw_input('press a key to continue')

    #LGS-A24
    turn_off_gpio("P8_18")
    turn_on_gpio("P8_16")
    raw_input('press a key to continue')

    #LGS-A25
    turn_off_gpio("P8_16")
    turn_on_gpio("P8_14")
    raw_input('press a key to continue')

    #LGS-B1
    turn_off_all.turn_off()
    turn_on_gpio("P8_46")
    turn_on_gpio("P8_14")
    raw_input('press a key to continue')

    #LGS-B2
    turn_off_gpio("P8_14")
    turn_on_gpio("P8_12")
    raw_input('press a key to continue')

    #LGS-B3
    turn_off_gpio("P8_12")
    turn_on_gpio("P8_6")
    raw_input('press a key to continue')

    #LGS-B4
    turn_off_all.turn_off()
    turn_on_gpio("P8_4")
    turn_on_gpio("P8_24")
    raw_input('press a key to continue')

    #LGS-B5
    turn_off_gpio("P8_24")
    turn_on_gpio("P8_22")
    raw_input('press a key to continue')

    #LGS-B6
    turn_off_gpio("P8_22")
    turn_on_gpio("P8_20")
    raw_input('press a key to continue')

    #LGS-B7
    turn_off_gpio("P8_20")
    turn_on_gpio("P8_18")
    raw_input('press a key to continue')

    #LGS-B8
    turn_off_gpio("P8_18")
    turn_on_gpio("P8_16")
    raw_input('press a key to continue')

    #LGS-B9
    turn_off_gpio("P8_16")
    turn_on_gpio("P8_14")
    raw_input('press a key to continue')

    #LGS-B10
    turn_off_gpio("P8_14")
    turn_on_gpio("P8_12")
    raw_input('press a key to continue')

    #LGS-B11
    turn_off_gpio("P8_12")
    turn_on_gpio("P8_6")
    raw_input('press a key to continue')

    #LGS-B12
    turn_off_all.turn_off()
    turn_on_gpio("P8_3")
    turn_on_gpio("P8_24")
    raw_input('press a key to continue')

    #LGS-B13
    turn_off_gpio("P8_24")
    turn_on_gpio("P8_22")
    raw_input('press a key to continue')

    #LGS-B14
    turn_off_all.turn_off()
    turn_on_gpio("P8_46")
    turn_on_gpio("P8_16")
    raw_input('press a key to continue')

    #LGS-B15
    turn_off_gpio("P8_16")
    turn_on_gpio("P8_18")
    raw_input('press a key to continue')

    #LGS-B16
    turn_off_gpio("P8_18")
    turn_on_gpio("P8_20")
    raw_input('press a key to continue')

    #LGS-B17
    turn_off_gpio("P8_20")
    turn_on_gpio("P8_22")
    raw_input('press a key to continue')

    #LGS-B18
    turn_off_gpio("P8_22")
    turn_on_gpio("P8_24")
    raw_input('press a key to continue')

    #LGS-B20
    turn_off_all.turn_off()
    turn_on_gpio("P8_3")
    turn_on_gpio("P8_6")
    raw_input('press a key to continue')

    #LGS-B21
    turn_off_gpio("P8_6")
    turn_on_gpio("P8_12")
    raw_input('press a key to continue')

    #LGS-B22
    turn_off_gpio("P8_12")
    turn_on_gpio("P8_14")
    raw_input('press a key to continue')

    #LGS-B23
    turn_off_gpio("P8_14")
    turn_on_gpio("P8_16")
    raw_input('press a key to continue')

    #LGS-B24
    turn_off_gpio("P8_16")
    turn_on_gpio("P8_18")
    raw_input('press a key to continue')

    #LGS-B25
    turn_off_gpio("P8_18")
    turn_on_gpio("P8_20")
    raw_input('press a key to continue')

    #LGS-C10
    turn_off_all.turn_off()
    turn_on_gpio("P8_17")
    turn_on_gpio("P8_18")
    raw_input('press a key to continue')

    #LGS-C11
    turn_off_gpio("P8_18")
    turn_on_gpio("P8_16")
    raw_input('press a key to continue')

    #LGS-C12
    turn_off_gpio("P8_16")
    turn_on_gpio("P8_14")
    raw_input('press a key to continue')

    #LGS-C13
    turn_off_gpio("P8_14")
    turn_on_gpio("P8_12")
    raw_input('press a key to continue')

    #LGS-C25
    turn_off_gpio("P8_12")
    turn_on_gpio("P8_6")
    raw_input('Press enter to go for LGS-A1')

    raw_input('\n\nIF you press ANY KEY,THEN you WILL QUIT!!!')
