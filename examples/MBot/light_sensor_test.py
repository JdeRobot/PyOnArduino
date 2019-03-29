from time import sleep

import halduino.halduino as halduino


def set_engine(direction: int):
    if direction == 0:
        halduino.setSpeedEngines(0, 0)
        sleep(500)
        halduino.playBuzzer(330, 1000)
        halduino.setSpeedEngines(-100, -100)
        sleep(500)
        halduino.setSpeedEngines(100, 0)
        sleep(1200)
    elif direction == 1:
        halduino.setSpeedEngines(100, 100)


def loop():
    if halduino.getLightSensor() < 100:
        set_engine(0)
    else:
        set_engine(1)
