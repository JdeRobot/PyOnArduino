import halduino.halduino as halduino


def loop():
    if halduino.isButtonPressed():
        halduino.playBuzzer(330, 1000)
    elif halduino.isButtonReleased() is True:
        halduino.playBuzzer(249, 1000)
