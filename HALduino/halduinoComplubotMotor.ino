
void architecturalStop() {
    /*DynType errorX;errorX.tvar = INT;String x = "5";x.toCharArray(errorX.data, MinTypeSz);
    DynType errorY;errorY.tvar = INT;String y = "5";y.toCharArray(errorY.data, MinTypeSz);
    DynType var;var.tvar = STR;String errorString = "ERROR!!";errorString.toCharArray(var.data, MinTypeSz);
    setScreenText(var, errorX, errorY);*/
}

void stopMachine() {
    architecturalStop();
    for(;;){
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

void setSpeedEngines(DynType speedLeft, DynType  speedRight) {
    RobotMotor.motorsWrite(atoi(speedLeft.data), atoi(speedRight.data));
}

int getLineFollowValue() {
    if (getIR3() < 300)
        return 0;
    if (getIR4() < 300)
        return 1;
    if (getIR2() < 300)
        return 2;
    return 3;
}