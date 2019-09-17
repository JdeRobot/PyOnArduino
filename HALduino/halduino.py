def getUS() -> int:
    """
        Gets the ultrasonic sensor measurement.
        @return: sensor's measurement.
    """
    pass


def setSpeedEngine1(speed: int):
    """
        Set engine 1 speed.
        @param speed: engine's speed.
    """
    pass


def setSpeedEngine2(speed: int):
    """
        Set engine 2 speed.
        @param speed: engine's speed.
    """
    pass


def setSpeedEngine3(speed: int):
    """
        Set engine 3 speed.
        @param speed: engine's speed.
    """
    pass


def setSpeedEngine4(speed: int):
    """
        Set engine 4 speed.
        @param speed: engine's speed.
    """
    pass


def setSpeedEngines(leftSpeed: int, rightSpeed: int):
    """
        Set engines speed for both left side and right side of the robot.
        @param leftSpeed: left engine speed.
        @param rightSpeed: right engine's speed.
    """
    pass


def setSpeed(speed: int):
    """
        Set robot's speed.
        @param speed: speed for the robot.
    """
    pass


def getIR1() -> int:
    """
        Get infrared sensor 1 measurement.
        @return: sensor's measurement.
    """
    pass


def getIR2() -> int:
    """
        Get infrared sensor 2 measurement.
        @return: sensor's measurement.
    """
    pass


def getIR3() -> int:
    """
        Get infrared sensor 3 measurement.
        @return: sensor's measurement.
    """
    pass


def getIR4() -> int:
    """
        Get infrared sensor 4 measurement.
        @return: sensor's measurement.
    """
    pass


def getIR5() -> int:
    """
        Get infrared sensor 5 measurement.
        @return: sensor's measurement.
    """
    pass


def lineFollow(KP: int, KD: int, robotSpeed: int, integrationTime: int):
    """
        Line follow method.
        @param KP:
        @param KD:
        @param robotSpeed:
        @param integrationTime:
    """
    pass


def playBeep(type: int):
    """
        Robot plays a beep given the type.
        @param type: type of beep. Available types: 0, 1, 2.
    """
    pass


def playMelody(melody: str):
    """
        Robot plays a melody.
        @param melody: string containing the melody to be played.
    """
    pass


def setScreenText(text: str, x: int, y: int):
    """
        Text given is writen in the screen.
        @param text: text to write on the screen.
        @param x: starting x point to write the text.
        @param y: starting y point to write the text.
    """
    pass


def clearScreen():
    """
        Clear the screen if something is writen.
    """
    pass


def setLeds(number: int, red: int, green: int, blue: int):
    """
        Set the leds in the robot color.
        @param number: ked number.
        @param red: amount of red color.
        @param green: amount of green color.
        @param blue: amount of blue color.
    """
    pass


def playBuzzer(frequency: int, length: int):
    """
        Robot plays buzzer.
        @param frequency: frequency to be played.
        @param length: time length to play.
    """
    pass


def isButtonPressed() -> bool:
    """
        Checks if button is pressed.
        @return: boolean with state of the button.
    """
    pass


def isButtonReleased() -> bool:
    """
        Checks is button is released.
        @return: boolean with state of the button.
    """
    pass


def getLightSensor() -> int:
    """
        Gets light sensor measurement.
        @return: value of distance the light reaches.
    """
    pass


def sendMessage(message: str):
    """
        Robot sends message using infrared sensor.
        @param message: string with the message to send.
    """
    pass


def getMessage() -> str:
    """
        Get message sent to the robot using infrared sensor.
        @return: message retrieved by robot.
    """
    pass


def showClock(hour: int, min: int):
    """
        Show clock on screen.
        @param hour: hour to write on screen.
        @param min: min to write on screen.
    """
    pass


def drawString(text: str):
    """
        Draw string on screen.
        @param text: string to write on screen.
    """
    pass


def getLineFollowValue() -> int:
    """
        Get line follow current state value.
        @return: line follow state value.
    """
    pass


# Methods in Spanish
def avanzar(vel: int):
    """
        El robot avanza en línea recta según el valor de velocidad.
        @param vel: velocidad de avance del robot.
    """
    pass


def retroceder(vel: int):
    """
        El robot retrocede en línea recta según el valor de velocidad.
        @param vel: velocidad de retroceso del robot.
    """
    pass


def parar():
    """
        El robot detiene su movimiento.
    """
    pass


def leerIRsiguelineas() -> int:
    """
        Lee el valor actual del estado del sensor de infrarrojos utilizado para el siguelineas.
        @return: valor del estado del infrarrojo.
    """
    pass


def leerUltrasonido() -> int:
    """
        Leer el valor del sensor de ultrasonido.
        @return: valor devuelto por el sensor.
    """
    pass