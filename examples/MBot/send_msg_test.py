import halduino.halduino as halduino


def loop():
    if halduino.isButtonPressed():
        halduino.sendMessage('hello')
        halduino.playBuzzer(330, 500)