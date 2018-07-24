from time import sleep

import HALduino.halduino as halduino


def loop():
    halduino.setScreenText("Hello World!!", 5, 5)
    sleep(2000)
    halduino.clearScreen()
    halduino.setScreenText("Complubot!!", 5, 5)
    sleep(2000)
    halduino.clearScreen()
