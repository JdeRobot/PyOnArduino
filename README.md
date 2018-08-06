# PyOnArduino
The purpose of PyOnArduino is to create a tool that can translate Python-like code to Arduino code. We 
pursue this target in order to program an educational robot that uses an Arduino microprocessor using 
Python.

## Requirements and installation
+ Python 3.6 [Download](https://www.python.org/downloads/)
+ Arduino IDE [Download](https://www.arduino.cc/en/Main/Software)
+ Arduino Makefile [Download and installation](https://github.com/sudar/Arduino-Makefile)

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
### Sensors and actuators supported [WIP]

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
Infrared sensors | getIR[1,2,3,4,5] ()

### Python features supported [WIP]
Functionality we are currently working on giving support to

Feature | Limitations/Comments
----------------|---------------------
Variable declaration      | SUPPORTED
Function definition | With/without return statement 
Operators | + - / * ^ %
Comparators | < <= >= == != 
Logic operators | and or is not
Pass | SUPPORTED 
Loops | for, while
sleep() | SUPPORTED
If | If/elif/else
For | Working on it
While | If/elif/else
Arrays | Working on it
Boolean operations | and or
Tuples | Future work
Range | Future work


### Architecture file
A robot's architecture file can be added when executing PyOnArduino. On this file, added sensors' port can be added, 
so PyOnArduino can understand where to link them. Example: 
```
    ultrasonicSensor = TK2
    rgbled = 7
```
To declare a sensor's port, just add the name + '=' + port name. 
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

### Problem with Complubot

There is a problem with Arduino Robot(Complubot). Sometimes when you upload a project it can make 
the usb port stop working. If you ever get to this point, the solution is quite simple. Write an 
empty sketch and upload it. While it's being uploaded press the reset button on the board two times.
This should fix the problem! [Source](http://forum.arduino.cc/index.php?topic=269822.0)