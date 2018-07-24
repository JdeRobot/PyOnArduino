
void architecturalStop() {
    // TODO
}

void stopMachine() {
    architecturalStop();
    for(;;){
        //will stop here for sure
        delay(5000);
    }
}

void setSpeedEngines(DynType speedLeft, DynType  speedRight){
    MeDCMotor motor_9(9);
    MeDCMotor motor_10(10);
    motor_9.run(-atoi(speedLeft.data));
    motor_10.run(atoi(speedRight.data));
}

int getUS() {
    MeUltrasonicSensor ultrasonic(3);
    return ultrasonic.distanceCm();
}
