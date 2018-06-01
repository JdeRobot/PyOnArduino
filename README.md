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
### Python features supported [WIP]
Feature | Limitations/Comments
----------------|---------------------
Variable declaration      | INPUT/OUTPUT variables have to be declared on top
Function definition with return type | If no return type is provided, void is expected. This is made to be easier to understand by the translator

### Example
For the translator to better understand the problem, we divide the code in 3 sections. 
+ Variable declaration
+ Functions
+ While True statement. Equivalent to loop() in Arduino
```
left_front_forward = [5, 'OUTPUT']
left_front_backward = [4, 'OUTPUT']
echoUS = ['A5', 'INPUT']
triggerUS = ['A4', 'OUTPUT']

def get_US() -> int:
    digitalWrite(triggerUS, LOW)
    delayMicroseconds(2)
    digitalWrite(triggerUS, HIGH)
    delayMicroseconds(10)
    digitalWrite(triggerUS, LOW)
    timeUS = pulseIn(echoUS, HIGH)
    distanceUS = timeUS / 58
    return distanceUS
    # return int(input('Distance: '))

def set_engine(direction):
    if direction == 0:
        digitalWrite(left_front_forward, 0)
        digitalWrite(left_front_backward, 0)
        print('STOP! ')
    elif direction == 1:
        digitalWrite(left_front_forward, 0)
        digitalWrite(left_front_backward, 1)
        print('Forward')

# This is the part that should go inside loop
while True:
    if get_US() < 10:
        set_engine(0)
    else:
        set_engine(1)
```
