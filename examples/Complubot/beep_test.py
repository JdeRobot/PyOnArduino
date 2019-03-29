from time import sleep
import halduino.halduino as halduino


def loop():
    halduino.playBeep(0)
    sleep(100)
    halduino.playBeep(1)
    sleep(100)
    halduino.playBeep(2)
    sleep(100)
