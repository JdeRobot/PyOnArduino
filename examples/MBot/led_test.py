from time import sleep

import halduino.halduino as halduino


def loop():
    halduino.setLeds(0, 150, 0, 0)
    sleep(500)
    halduino.setLeds(1, 0, 150, 0)
    sleep(500)
    halduino.setLeds(2, 0, 0, 150)
    sleep(500)
    halduino.setLeds(0, 150, 150, 150)
    sleep(500)
