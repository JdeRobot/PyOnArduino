
int getUS() {

}

void setVEngine1(int forward, int  backward) {

}

int getIR1() {
    return RobotMotor.IRread(1);
}

int getIR2() {
    return RobotMotor.IRread(2);
}

int getIR3() {
    return RobotMotor.IRread(3);
}

int getIR4() {
    return RobotMotor.IRread(4);
}

int getIR5() {
    return RobotMotor.IRread(5);
}

void setVEngine1(int speedLeft, int  speedRight) {
    Robot.motorsWrite(speedLeft, speedRight);
}