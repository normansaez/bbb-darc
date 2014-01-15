from threading import Thread
from Queue import Queue
from random import randint
from time import sleep


def move_motor(motor, timeout, queue):
    h_ = queue.get()
    t = randint(5,10)
    print "%s -> sleeping %d" % (motor, t)
    sleep(t)
    print "finish %s" % motor 
    queue.task_done()


if __name__ == '__main__':
    queue = Queue()
    timeout = 10
    for motor in ["m1","m2","m3"]:
        queue.put(motor)
    for motor in ["m1","m2","m3"]:
        rh =  Thread(name=str(motor+"-thread"), target=move_motor, args=(motor, timeout, queue))
        rh.setDaemon(True)
        rh.start()
    queue.join()
