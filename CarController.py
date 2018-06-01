# Function that reads ultrasound sensor and stops the car if the distance to an object is lower than 10cm
def get_US():
    print()
    print('Ultrasound sensor manager. Car will be stopped if you are on a distance of 10cm or closer to an obstacle')
    distance = 11
    while distance > 10:
        try:
            distance = int(input('Distance: '))
        except ValueError:
            print('Not a number')
    print('STOP! You\'re to close to an obstacle')
    print()

# Function that allows you to set the engine forward or backward
def set_engine():
    direction = 0
    print()
    print('Engine direction manager')
    print('[0] Backward [1] Forward')
    while direction >= 0:
        try:
            direction = int(input('Enter direction: '))
            if direction == 0:
                print('Backward')
            elif direction == 1:
                print('Forward')
            else:
                print('[0] Backward [1] Forward')
        except ValueError:
            print('Not a number')
    print()

# Car controller that links you with the functionality available
def car_controller():
    value = -1
    while value != 0:
        print('Choose the program you want to use typing its number')
        print('0. End program')
        print('1. Get Ultrasound')
        print('2. Set Engine direction')
        try:
            value = int(input('Option: '))
            if value == 1:
                get_US()
            elif value == 2:
                set_engine()
        except ValueError:
            print('Not a number')
    print()
    print('Program ended! Bye!')

car_controller()

