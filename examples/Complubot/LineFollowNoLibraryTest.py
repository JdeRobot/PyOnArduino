import HALduino.halduino as halduino


def loop():
    if halduino.getIR3() < 300:
        halduino.setSpeedEnginesMotor(110, 110)
    if halduino.getIR2() < 300:
        halduino.setSpeedEnginesMotor(110, 0)
    if halduino.getIR4() < 300:
        halduino.setSpeedEnginesMotor(0, 110)
