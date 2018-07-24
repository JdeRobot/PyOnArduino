import HALduino.halduino as halduino


def loop():
    if halduino.getIR2() < halduino.getIR4() and halduino.getIR5() < 990:
        halduino.setSpeedEnginesMotor(0, 110)
    else:
        halduino.setSpeedEnginesMotor(110, 0)
