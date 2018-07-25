
void architecturalStop() {
    DynType var0;var0.tvar = INT;String har0 = "0";har0.toCharArray(var0.data, MinTypeSz);
    DynType var1;var1.tvar = INT;String har1 = "1";har1.toCharArray(var1.data, MinTypeSz);
    DynType var2;var2.tvar = INT;String har2 = "2";har2.toCharArray(var2.data, MinTypeSz);
    DynType var3;var3.tvar = INT;String har3 = "150";har3.toCharArray(var3.data, MinTypeSz);
    for(int i = 0; i < 3; i++) {
        for(int j = 0; j < 10; j++) {
            setLeds(var1,var3,var0,var0);
            delay(100);
            setLeds(var2,var0,var3,var0);
            delay(100);
        }
        for(int j = 0; j < 10; j++) {
            setLeds(var0,var0,var3,var0);
            delay(100);
            setLeds(var0,var0,var0,var0);
            delay(100);
        }
        for(int j = 0; j < 10; j++) {
            setLeds(var0,var3,var0,var0);
            delay(100);
            setLeds(var0,var0,var0,var0);
            delay(100);
        }
    }
}

void stopMachine() {
    architecturalStop();
    for(;;){
        //will stop here for sure
        delay(5000);
    }
}

void setSpeedEngines(DynType speedLeft, DynType speedRight){
    MeDCMotor motor_9(9);
    MeDCMotor motor_10(10);
    motor_9.run(-atoi(speedLeft.data));
    motor_10.run(atoi(speedRight.data));
}

int getUS() {
    MeUltrasonicSensor ultrasonic(3);
    return ultrasonic.distanceCm();
}

void setLeds(DynType ledNumber, DynType red, DynType green, DynType blue) {
    MeRGBLed rgbled(7, 2);
    rgbled.setColor(atoi(ledNumber.data),atoi(red.data),atoi(green.data),atoi(blue.data));
    rgbled.show();
}

void playBuzzer(DynType tone, DynType length) {
    MeBuzzer buzzer;
    buzzer.tone(atoi(tone.data), atoi(length.data));
}
