from time import sleep

import HALduino.halduino as halduino


def set_engine(direction: int):
    if direction == 0:
        halduino.setSpeedEnginesControl(0, 0)
        sleep(500)
        halduino.setSpeedEnginesControl(-100, -100)
        sleep(500)
        halduino.setSpeedEnginesControl(100, 0)
        sleep(100)
        print('Rotate!')
    elif direction == 1:
        halduino.setSpeedEnginesControl(100, 100)
        print('Forward')


def loop():
    if halduino.getUS() < 30:
        set_engine(0)
    else:
        set_engine(1)
