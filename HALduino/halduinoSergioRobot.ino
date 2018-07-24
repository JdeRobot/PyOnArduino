
void architecturalStop() {
    #define LIGHTPIN 8
    pinMode(LIGHTPIN, OUTPUT);
    digitalWrite(LIGHTPIN, HIGH);
    delay(100);
    digitalWrite(LIGHTPIN, LOW);
}

void stopMachine() {
    architecturalStop();
    for(;;){
        //will stop here for sure
        delay(5000);
    }
}

int getUS() {
    int echoUS = A5;
    int triggerUS = A4;
    pinMode(echoUS,INPUT);
    pinMode(triggerUS,OUTPUT);
    digitalWrite(triggerUS, 0);
    delay(2);
    digitalWrite(triggerUS, 1);
    delay(10);
    digitalWrite(triggerUS, 0);
    int timeUS = pulseIn(echoUS, 1);
    int distanceUS = timeUS / 58;
    return distanceUS;
}

void setSpeedEngine1(DynType speed) {
    int left_front_forward = 5;
    int left_front_backward = 4;
    pinMode(left_front_forward,OUTPUT);
    pinMode(left_front_backward,OUTPUT);
    if (atoi(speed.data) < 0) {
        analogWrite(left_front_forward, atoi(speed.data));
    } else {
        analogWrite(left_front_backward, atoi(speed.data));
    }
}

void setSpeedEngine2(DynType speed) {
    int right_front_forward = 2;
    int right_front_backward = 6;
    pinMode(right_front_forward,OUTPUT);
    pinMode(right_front_backward,OUTPUT);
    if (atoi(speed.data) < 0) {
        analogWrite(right_front_forward, atoi(speed.data));
    } else {
        analogWrite(right_front_backward, atoi(speed.data));
    }
}

void setSpeedEngine3(DynType speed) {
    int left_back_forward = 9;
    int left_back_backward = 10;
    pinMode(left_back_forward,OUTPUT);
    pinMode(left_back_backward,OUTPUT);
    if (atoi(speed.data) < 0) {
        analogWrite(left_back_forward, atoi(speed.data));
    } else {
        analogWrite(left_back_backward, atoi(speed.data));
    }
}

void setSpeedEngine4(DynType speed) {
    int right_back_forward = 11;
    int right_back_backward = 12;
    pinMode(right_back_forward,OUTPUT);
    pinMode(right_back_backward,OUTPUT);
    if (atoi(speed.data) < 0) {
        analogWrite(right_back_forward, atoi(speed.data));
    } else {
        analogWrite(right_back_backward, atoi(speed.data));
    }
}

#define IR1PIN 3
IRrecv irrecv(IR1PIN);

void setupIR1() {
  Serial.begin(9600) ;
  Serial.println("NEC IR1 code reception") ;
  irrecv.enableIRIn();
}

int getIR1() {
    decode_results resultsIR1;
    if (irrecv.decode(&resultsIR1)) { // have we received an IR signal
        Serial.println(resultsIR1.value);
        irrecv.resume();
        return resultsIR1.value;
    }
}

void setupIR2() {
  Serial.begin(9600) ;
  Serial.println("NEC IR2 code reception") ;
  irrecv.enableIRIn();
}

#define IR2PIN 4
IRrecv irrecv(IR2PIN);

int getIR2() {
    decode_results resultsIR2;
    if (irrecv.decode(&resultsIR2)) { // have we received an IR signal
        Serial.println(resultsIR2.value);
        irrecv.resume();
        return resultsIR2.value;
    }
}