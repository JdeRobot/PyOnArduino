# PyOnArduino
The purpose of PyOnArduino is to create a tool that can translate Python-like code to Arduino code. We 
pursue this target in order to program an educational robot that uses an Arduino microprocessor using 
Python.

## Requirements and installation
+ Python 3.6 [Download](https://www.python.org/downloads/)
+ Arduino Makefile [Download and installation](https://github.com/sudar/Arduino-Makefile)

To execute the project 
```
    python3 translator/Translator.py [input-file] [robot] [output-file]
    python3 translator/Translator.py [input-file] [robot]
```
## Demo video
## Features
### Sensors and actuators supported [WIP]
Sensor/Actuator | Supported functions
----------------|---------------------
DC Engines      | setSpeedEngine[1,2,3,4,5] (speed), setSpeedEngines(right,left)
Ultrasonic sensors | getUS()
Infrared sensors | getIR[1,2,3,4,5]
Beep emitter | playBeep(type)
Sound emitter | playMelody(melody)
Screen write | setScreenText(text), clearScreen()
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
Arrays | Arrays can be defined given the types we already supported
Boolean operations | and or
Tuples | Future work

### Example

Examples available in the repo, check them out!