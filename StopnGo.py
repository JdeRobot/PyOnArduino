left_front_forward = [5, 'OUTPUT']
left_front_backward = [4, 'OUTPUT']
echoUS = ['A5', 'INPUT']
triggerUS = ['A4', 'OUTPUT']

def get_US() -> int:
    #   Instead of reading the distance from keyboard we should get the measurement from the actual ultrasonic
    #   sensor
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
    #   Instead of just printing the direction the engines will have, we should actually set it within this function
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