import halduino.halduino as halduino


def set_engine(direction: int):
    if direction == 0:
        halduino.setSpeedEngine1(0)
        halduino.setSpeedEngine2(0)
        halduino.setSpeedEngine3(0)
        halduino.setSpeedEngine4(0)
        print('STOP!')
    elif direction == 1:
        halduino.setSpeedEngine1(255)
        halduino.setSpeedEngine2(255)
        halduino.setSpeedEngine3(255)
        halduino.setSpeedEngine4(255)
        print('Forward')


def loop():
    if halduino.getUS() < 10:
        set_engine(0)
    else:
        set_engine(1)
