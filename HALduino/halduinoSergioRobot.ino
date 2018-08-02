
void architecturalStop() {
    #define LIGHTPIN 8
    pinMode(LIGHTPIN, OUTPUT);
    delay(100);
}

void stopMachine() {
    architecturalStop();
    for(;;){
        //will stop here for sure
        delay(5000);
    }
}

int echoUS = A5;
int triggerUS = A4;
pinMode(echoUS,INPUT);
pinMode(triggerUS,OUTPUT);
int getUS() {
    delay(2);
    delay(10);
    int timeUS = pulseIn(echoUS, 1);
    int distanceUS = timeUS / 58;
    return distanceUS;
}

int left_front_forward = 5;
int left_front_backward = 4;
pinMode(left_front_forward,OUTPUT);
pinMode(left_front_backward,OUTPUT);
void setSpeedEngine1(DynType speed) {
    int speedData = atoi(speed.data);
    if (atoi(speed.data) < 0) {
        analogWrite(left_front_forward, speedData);
    } else {
        analogWrite(left_front_backward, speedData);
    }
}

int right_front_forward = 2;
int right_front_backward = 6;
pinMode(right_front_forward,OUTPUT);
pinMode(right_front_backward,OUTPUT);
void setSpeedEngine2(DynType speed) {
    int speedData = atoi(speed.data);
    if (atoi(speed.data) < 0) {
        analogWrite(right_front_forward, speedData);
    } else {
        analogWrite(right_front_backward, speedData);
    }
}

int left_back_forward = 9;
int left_back_backward = 10;
pinMode(left_back_forward,OUTPUT);
pinMode(left_back_backward,OUTPUT);
void setSpeedEngine3(DynType speed) {
    int speedData = atoi(speed.data);
    if (atoi(speed.data) < 0) {
        analogWrite(left_back_forward, speedData);
    } else {
        analogWrite(left_back_backward, speedData);
    }
}

int right_back_forward = 11;
int right_back_backward = 12;
pinMode(right_back_forward,OUTPUT);
pinMode(right_back_backward,OUTPUT);
void setSpeedEngine4(DynType speed) {
    int speedData = atoi(speed.data);
    if (atoi(speed.data) < 0) {
        analogWrite(right_back_forward, speedData);
    } else {
        analogWrite(right_back_backward, speedData);
    }
}

#define IR1PIN 3
IRrecv irrecv(IR1PIN);
void setupIR1() {
  Serial.begin(9600) ;
  Serial.println("NEC IR1 code reception");
  irrecv.enableIRIn();
}

decode_results resultsIR1;
int getIR1() {
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