from time import sleep

import HALduino.halduino as halduino


def loop():
    sleep(100)
    print(halduino.getIR1())
    print(' ')
    print(halduino.getIR2())
    print(' ')
    print(halduino.getIR3())
    print(' ')
    print(halduino.getIR4())
    print(' ')
    print(halduino.getIR5())
    print(' ')
