from time import sleep

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
    sleep(100)
    if halduino.getUS() < 10:
        set_engine(0)
    else:
        set_engine(1)

    print(5 + 33 - 4 * 4)
    print(5 - 3 / 5)
    print(5 * 3)
    print(5 / 3)
    print(5 % 3)

    y = [1,2,3,4]

    for x in y:
        print(x)

    if True:
        print('HELLO')
    elif halduino.getUS() <= 10:
        set_engine(0)
    else:
        set_engine(1)

def print_name_surname(name: str, surname: str, second: str, another: str):
    print(name + surname + second + another)