# PyOnArduino
The purpose of PyOnArduino is to create a tool that can translate Python-like code to Arduino code. We 
pursue this target in order to program an educational robot that uses an Arduino microprocessor using 
Python.

## Example

Example of PyOnArduino in action. On this example, the same Python + PyOnArduino code is compiled and 
uploaded to the robots and the behaviour is the same

<p align="center">
    <a href="https://www.youtube.com/watch?v=gK-LwSBi6co">
    <img src="https://img.youtube.com/vi/gK-LwSBi6co/0.jpg" alt="Sublime's custom image"/>
    </a>
</p>

## Requirements and installation
+ Python 3.6 [Download](https://www.python.org/downloads/)
+ Arduino IDE [Download](https://www.arduino.cc/en/Main/Software)
+ Arduino Makefile [Download and installation](https://github.com/sudar/Arduino-Makefile)
    + Check makefiles folders and change the variables if the usb port or directories are different.
+ pySerial [Documentation](https://pythonhosted.org/pyserial/pyserial.html#installation)
+ To execute on mBot you need to add Makeblock libraries to the Arduino IDE following [this repo](https://github.com/Makeblock-official/Makeblock-Libraries)
+ If you use MacOS and you want to execute on mBot, you'll probably new ch340 driver [Download](https://github.com/adrianmihalko/ch340g-ch34g-ch34x-mac-os-x-driver)

To execute the project 
```
    python3 translator/Translator.py [input-file] [robot]
    python3 translator/Translator.py [input-file] [robot] [architecture-file]
```
## Robots supported
* [Complubot](https://www.arduino.cc/en/Guide/Robot) (Arduino Robot)
* [MBot](https://www.makeblock.com/steam-kits/mbot)
* SergioRobot: This is an educational project not a real world development
## Features
### Sensors and actuators supported 

#### Complubot
Sensor/Actuator | Supported functions
----------------|---------------------
DC Engines      | setSpeedEnginesControl(left, right), setSpeedEnginesMotor(left, right)
Ultrasonic sensors | getUS()
Infrared sensors | getIR[1,2,3,4,5]
Beep emitter | playBeep(type)
Sound emitter | playMelody(melody)
Screen write | setScreenText(text), clearScreen()

#### mBot
Sensor/Actuator | Supported functions
----------------|---------------------
DC Engines      | setSpeedEngines(speed), getLineFollowValue()
Ultrasonic sensors | getUS()
LEDs | setLeds(ledNumber, red, green, blue)
Infrared sensors | getMessage(), sendMessage(message)
Light sensor | getLightSensor()
Button | isButtonPressed(), isButtonReleased()
Buzzer | playBuzzer(tone, length)
External screen | drawString(name), showClock(hour, min)

#### SergioRobot
Sensor/Actuator | Supported functions
----------------|---------------------
DC Engines      | setSpeedEngine[1,2,3,4] (speed)
Ultrasonic sensors | getUS()
Infrared sensors | getIR[1,2] ()

### Python features supported
Supported functionality

Feature | Limitations/Comments
----------------|---------------------
Variable declaration      | SUPPORTED
Function definition | With/without return statement 
Operators | + - / * ^ %
Comparators | < <= >= == != 
Logic operators | and or is not
Pass | SUPPORTED 
Loops | while, for (future proposal)
sleep() | SUPPORTED
If | If/elif/else
Boolean operations | and or
Arrays | Future proposal
Tuples | Future proposal
Range | Future proposal


### Architecture file
A robot's architecture file can be added when executing PyOnArduino. On this file, added sensors' port can be added, 
so PyOnArduino can understand where to link them. Example: 
```
    ultrasonicSensor = TK2
    rgbled = 7
```
To declare a sensor's port, just add the name + '=' + port name. 
Example files:
* [mBot](https://github.com/JdeRobot/PyOnArduino/blob/master/HALduino/mBotGeneralArchitecture)
* [Complubot](https://github.com/JdeRobot/PyOnArduino/blob/master/HALduino/ComplubotControlGeneralArchitecture)
#### Complubot port names
* ultrasonicSensor

#### mBot port names
* leftMotor
* rightMotor
* ultrasonicSensor
* rgbled
* lightSensor
* ledMtx
* lineFollower

### Example

Examples available in [examples](https://github.com/JdeRobot/PyOnArduino/tree/master/examples) folder, check them out!

## Problem with Complubot

There is a problem with Arduino Robot(Complubot). Sometimes when you upload a project it can make 
the usb port stop working. If you ever get to this point, the solution is quite simple. Write an 
empty sketch and upload it. While it's being uploaded press the reset button on the board two times.
This should fix the problem! [Source](http://forum.arduino.cc/index.php?topic=269822.0)


## Running Tests

To run the tests, run the following
```
python3 tests/<test-file>
```
To run specific tests for a bot, call the function in main and run the above command.