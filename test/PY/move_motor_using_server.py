
import CORBA, BBBServer
from random import randint
from BeagleDarc.Model import Layer
from BeagleDarc.Model import BeagleDarcServerM 

#COLOR CONST
BLUE     = '\033[34m'
RED      = '\033[31m'
GREEN    = '\033[32m'
YELLOW   = '\033[33m'
BLACK    = '\033[30m'
CRIM     = '\033[36m'
NO_COLOR = '\033[0m'

MAX_NUM = 2147483600

def motor_to_init(motor, server):
    '''
    Moves motor to init
    '''
    m = Layer(motor)
    print(RED+'Moving until find a sensor OR PRESS CONTROL+C'+NO_COLOR)
    m.steps = MAX_NUM
    server.motor_move(m.name, m.pin_dir, m.pin_step, m.pin_sleep, m.pin_opto1, m.pin_opto2, m.simulated, m.direction, m.velocity, m.steps, m.vr_init, m.vr_end, m.cur_pos)

def move_in_valid_range(motor, steps, server):
    '''
    Movements in valid ranges
    '''
    m = Layer(motor)
    print("cur_pos : %d" % m.cur_pos)
    cmd_pos = m.cur_pos + steps
    print("cmd_pos : %d" % cmd_pos)
    if cmd_pos < m.vr_init:
        print("cmd from %d --> %d" % (cmd_pos, m.vr_init))
        cmd_pos = m.vr_init
    if cmd_pos > m.vr_end:
        print("cmd from %d --> %d" % (cmd_pos, m.vr_init))
        cmd_pos = m.vr_init

    steps = cmd_pos - m.cur_pos
    if steps > 0:
        print("STEPS to cmd_pos: %d --> to %s" % (steps,m.direction))
        m.steps = steps
        m.direction = "END_POSITION"
        server.motor_move(m.name, m.pin_dir, m.pin_step, m.pin_sleep, m.pin_opto1, m.pin_opto2, m.simulated, m.direction, m.velocity, m.steps, m.vr_init, m.vr_end, m.cur_pos)
    else:
        m.direction = "INIT_POSITION"
        print("STEPS to cmd_pos: %d --> to %s" % (steps,m.direction))
        steps = abs(steps)
        m.steps = steps
        server.motor_move(m.name, m.pin_dir, m.pin_step, m.pin_sleep, m.pin_opto1, m.pin_opto2, m.simulated, m.direction, m.velocity, m.steps, m.vr_init, m.vr_end, m.cur_pos)
    m.cur_pos = cmd_pos
    return m.cur_pos, cmd_pos

if __name__ == '__main__':
    bds = BeagleDarcServerM('beagledarc_server')
    orb = CORBA.ORB_init()
    o = orb.string_to_object(bds.ior)
    o = orb.string_to_object()
    motor_to_init('ground_layer', o)
    #Here we have to move motors until INIT_POSITION . Otherwise, this is the end.
    #start to moving randomly:
    steps = randint(100,1000)
    move_in_valid_range('ground_layer', steps, o)
