#include <MeMCore.h>


void architecturalStop() {
    DynType var0;var0.tvar = INT;String har0 = "0";har0.toCharArray(var0.data, MinTypeSz);
    DynType var1;var1.tvar = INT;String har1 = "150";har1.toCharArray(var1.data, MinTypeSz);
    DynType var2;var2.tvar = INT;String har2 = "330";har2.toCharArray(var2.data, MinTypeSz);
    DynType var3;var3.tvar = INT;String har3 = "100";har3.toCharArray(var3.data, MinTypeSz);
    DynType var4;var4.tvar = INT;String har4 = "300";har4.toCharArray(var4.data, MinTypeSz);
    for(int i = 0; i < 3; i++) {
        for(int j = 0; j < 3; j++) {
            playBuzzer(var2, var3);
            delay(100);
        }
        for(int j = 0; j < 3; j++) {
            playBuzzer(var2, var4);
            delay(100);
        }
        for(int j = 0; j < 3; j++) {
            playBuzzer(var2, var3);
            delay(100);
        }
        delay(400);
    }
    for(int j = 0; j < 10; j++) {
        setLeds(var0, var1, var0, var0);
        delay(100);
        setLeds(var0, var0, var0, var0);
        delay(100);
    }
}

void stopMachine() {
    architecturalStop();
    for(;;) {
        //will stop here for sure
        delay(5000);
    }
}

MeDCMotor motor_9(9);
MeDCMotor motor_10(10);
void setSpeedEngines(DynType speedLeft, DynType speedRight) {
    motor_9.run(-atoi(speedLeft.data));
    motor_10.run(atoi(speedRight.data));
}

MeUltrasonicSensor ultrasonic(3);
int getUS() {
    return ultrasonic.distanceCm();
}

MeRGBLed rgbled(7, 2);
void setLeds(DynType ledNumber, DynType red, DynType green, DynType blue) {
    rgbled.setColor(atoi(ledNumber.data),atoi(red.data),atoi(green.data),atoi(blue.data));
    rgbled.show();
}

MeBuzzer buzzer;
void playBuzzer(DynType tone, DynType length) {
    buzzer.tone(atoi(tone.data), atoi(length.data));
}

boolean isButtonPressed() {
    return (0^(analogRead(A7)>10?0:1));
}

boolean isButtonReleased() {
    return (1^(analogRead(A7)>10?0:1));
}

MeLightSensor lightSensor(6);
int getLightSensor() {
    return lightSensor.read();
}

MeIR ir;
void sendMessage(String message) {
    ir.begin();
    ir.sendString(message);
}

MeIR ir;
String getMessage() {
    ir.begin();
    return ir.getString();
}

MeLEDMatrix ledMtx(3);
void showClock(DynType hour, DynType min) {
    ledMtx.showClock(atoi(hour.data), atoi(min.data), PointOn);
    delay(500);
    ledMtx.showClock(atoi(hour.data), atoi(min.data), PointOff);
    delay(500);
}

MeLEDMatrix ledMtx(3);
void drawString(DynType name) {
    ledMtx.setColorIndex(1);
    ledMtx.setBrightness(6);
    ledMtx.drawStr(0,0+7, name.data);
}

MeLineFollower lineFollower(2);
int getLineFollowValue() {
    return lineFollower.readSensors();
}