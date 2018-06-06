import HALduino.halduino as halduino

left_front_forward = [5, 'OUTPUT']
left_front_backward = [4, 'OUTPUT']
right_front_forward = [2, 'OUTPUT']
right_front_backward = [6, 'OUTPUT']
left_back_forward = [9, 'OUTPUT']
left_back_backward = [10, 'OUTPUT']
right_back_forward = [11, 'OUTPUT']
right_back_backward = [12, 'OUTPUT']
echoUS = ['A5', 'INPUT']
triggerUS = ['A4', 'OUTPUT']

def set_engine(direction):
    #   Instead of just printing the direction the engines will have, we should actually set it within this function
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

# This is the part that should go inside loop
while True:
    if halduino.getUS() < 10:
        set_engine(0)
    else:
        set_engine(1)