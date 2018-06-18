from time import sleep

import HALduino.halduino as halduino

def loop():
    sleep(100)
    print(halduino.getIR1())
