import HALduino.halduino as halduino

def set_engine(direction: int):
    if direction == 0:
        halduino.setSpeedEngines(0, 0)
        print('STOP!')
    elif direction == 1:
        halduino.setSpeedEngines(100, 100)
        print('Forward')

def loop():
    if halduino.getUS() < 30:
        set_engine(0)
    else:
        set_engine(1)