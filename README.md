# PyOnArduino
The purpose of PyOnArduino is to create a tool that can translate Python-like code to Arduino code. We 
pursue this target in order to program an educational robot that uses an Arduino microprocessor using 
Python.

## Requirements and installation
+ Python 3.6 [Download](https://www.python.org/downloads/)

To execute the project 
```
    python3 Translator.py [input-file] [output-file]
    python3 Translator.py [input-file]
```
## Demo video
## Features
### Sensors and actuators supported [WIP]
Sensor/Actuator | Supported functions
----------------|---------------------
DC Engines      | digitalWrite
Ultrasonic sensors | delayMicroseconds, pulseIn
Infrared sensors | Not yet supported
### Python features supported [WIP]
Functionality we are currently working on giving support to

Feature | Limitations/Comments
----------------|---------------------
Variable declaration      | Working on giving support to integer, boolean, float and double types. INPUT/OUTPUT variables have to be declared on top
Function definition with return type | Argument types must be added on class definition. If no return type is provided, void is expected. This is made to be easier to understand by the translator
Operators | + - / * ^ %
Loops | for, while
sleep() | SUPPORTED
If | If/elif/else
Tuples | Future work

### Example
For the translator to better understand the problem, we divide the code in 2 sections. 
+ Variable declaration
+ Functions
```
import HALduino.halduino as halduino

def set_engine(direction: int):
    if direction == 0:
        halduino.setVEngine1(0, 0)
        halduino.setVEngine2(0, 0)
        halduino.setVEngine3(0, 0)
        halduino.setVEngine4(0, 0)
        print('STOP!')
    elif direction == 1:
        halduino.setVEngine1(0, 1)
        halduino.setVEngine2(0, 1)
        halduino.setVEngine3(0, 1)
        halduino.setVEngine4(0, 1)
        print('Forward')

def loop():
    sleep(100)
    if halduino.getUS() < 10:
        set_engine(0)
    else:
        set_engine(1)
```
