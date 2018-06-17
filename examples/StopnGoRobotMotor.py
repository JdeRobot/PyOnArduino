import HALduino.halduino as halduino

def set_engine(direction: int):
    if direction == 0:
        halduino.setVEngine1(-255, -255)
        print('STOP!')
    elif direction == 1:
        halduino.setVEngine1(255, 255)
        print('Forward')

def loop():
    set_engine(1)