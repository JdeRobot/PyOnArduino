import HALduino.halduino as halduino

def loop():
    if halduino.getIR2() < halduino.getIR4() and halduino.getIR5() < 990:
        halduino.setSpeedEngines(0,110)
    else:
        halduino.setSpeedEngines(110, 0)