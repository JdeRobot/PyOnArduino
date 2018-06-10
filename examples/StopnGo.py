import HALduino.halduino as halduino

def set_engine(direction: int):
    if direction == 0:
        halduino.setVEngine1(0, 0)
        halduino.setVEngine2(0, 0)
        halduino.setVEngine3(0, 0)
        halduino.setVEngine4(0, 0)
        print('STOP!')
    elif direction == 1:
        halduino.setVEngine1(0, 1)
        halduino.setVEngine2(0, 1)
        halduino.setVEngine3(0, 1)
        halduino.setVEngine4(0, 1)
        print('Forward')

def loop():
    if halduino.getUS() < 10:
        set_engine(0)
    else:
        set_engine(1)