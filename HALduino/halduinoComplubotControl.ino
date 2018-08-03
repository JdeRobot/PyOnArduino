Robot.begin();


void architecturalStop() {
    DynType errorX;errorX.tvar = INT;String x = "5";x.toCharArray(errorX.data, MinTypeSz);
    DynType errorY;errorY.tvar = INT;String y = "5";y.toCharArray(errorY.data, MinTypeSz);
    DynType var;var.tvar = STR;String errorString = "ERROR!!";errorString.toCharArray(var.data, MinTypeSz);
    setScreenText(var, errorX, errorY);
}

void stopMachine() {
    architecturalStop();
    for(;;) {
        //will stop here for sure
        delay(5000);
    }
}

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

void setSpeedEngines(DynType speedLeft, DynType  speedRight) {
    Robot.motorsWrite(atoi(speedLeft.data), atoi(speedRight.data));
}

void lineFollow(DynType KP, DynType KD, DynType robotSpeed, DynType integrationTime) {
    Robot.lineFollowConfig(atoi(KP.data),atoi(KD.data),atoi(robotSpeed.data),atoi(integrationTime.data));//set PID parameters
    Robot.setMode(MODE_LINE_FOLLOW);
    while(!Robot.isActionDone()) {
    }
}

Robot.beginSpeaker();
void playBeep(DynType type) {
    Robot.beep(atoi(type.data));
}

Robot.beginSpeaker();
void playMelody(DynType melody) {
    String text = melody.data;
    char buffer[VarTypesSz[STR]];
    text.toCharArray(buffer, VarTypesSz[STR]);
    Robot.playMelody(buffer);
}

Robot.beginTFT();
void setScreenText(DynType textVar, DynType x, DynType y) {
    Robot.stroke(0, 0, 0);
    String text = textVar.data;
    char buffer[VarTypesSz[STR]];
    text.toCharArray(buffer, VarTypesSz[STR]);
    Robot.text(buffer, atoi(x.data), atoi(y.data));
}

Robot.beginTFT();
void clearScreen() {
    Robot.clearScreen();
}