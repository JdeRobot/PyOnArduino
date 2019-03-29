from time import sleep

import halduino.halduino as halduino


def loop():
    sleep(100)
    print(halduino.getIR1())
