import halduino.halduino as halduino


def loop():
    if halduino.getLineFollowValue() == 0:
        halduino.setSpeedEngines(100, 100)
    elif halduino.getLineFollowValue() == 1:
        halduino.setSpeedEngines(0, 100)
    elif halduino.getLineFollowValue() == 2:
        halduino.setSpeedEngines(100, 0)
    elif halduino.getLineFollowValue() == 3:
        halduino.setSpeedEngines(-100, -100)


def setup():
    while halduino.isButtonPressed() is False:
        pass
