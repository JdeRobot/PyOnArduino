from time import sleep
import HALduino.halduino as halduino


def loop():
    halduino.setBeep(0)
    sleep(100)
    halduino.setBeep(1)
    sleep(100)
    halduino.setBeep(2)
    sleep(100)
