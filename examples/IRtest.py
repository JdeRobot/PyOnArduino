from time import sleep

import HALduino.halduino as halduino

def setup():
    halduino.setupIR1()

def loop():
    sleep(100)
    print(halduino.getIR1())
