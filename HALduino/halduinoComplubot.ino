
int getUS() {
  long anVolt, inches, cm;
  int sum = 0; //Create sum variable so it can be averaged
  int avgrange = 60; //Quantity of values to average (sample size)
  for (int i = 0; i < avgrange ; i++)
  {
    //Used to read in the analog voltage output that is being sent by the MaxSonar device.
    //Scale factor is (Vcc/512) per inch. A 5V supply yields ~9.8mV/in
    //Arduino analog pin goes from 0 to 1024, so the value has to be divided by 2 to get the actual inches
    anVolt = Robot.analogRead(TK2) / 2;
    sum += anVolt;
    delay(10);
  }
  inches = sum / avgrange;
  cm = inches * 2.54;
  sum = 0;
  return cm;
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

void setSpeedEngines(int speedLeft, int  speedRight) {
    RobotMotor.motorsWrite(speedLeft, speedRight);
}

void lineFollow(int KP, int KD, int robotSpeed, int integrationTime) {
    Robot.lineFollowConfig(KP,KD,robotSpeed,integrationTime);//set PID parameters
    Robot.setMode(MODE_LINE_FOLLOW);
    while(!Robot.isActionDone()){
    }
}

void playBeep(int type) {
    Robot.beep(type);
}

void playMelody(String melody) {
    char buffer[melody.length()];
    melody.toCharArray(buffer, melody.length());
    Robot.playMelody(buffer);
}

void setScreenText(String text, int x, int y) {
    Robot.stroke(0, 0, 0);
    char buffer[text.length()];
    text.toCharArray(buffer, text.length());
    Robot.text(buffer, x, y);
}

void clearScreen() {
    Robot.clearScreen();
}