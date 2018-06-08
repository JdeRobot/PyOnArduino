
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

void setVEngine1(int forward, int  backward) {
    int left_front_forward = 5;
    int left_front_backward = 4;
    pinMode(left_front_forward,OUTPUT);
    pinMode(left_front_backward,OUTPUT);
    digitalWrite(left_front_forward, forward);
    digitalWrite(left_front_backward, backward);
}

void setVEngine2(int forward, int  backward) {
    int right_front_forward = 2;
    int right_front_backward = 6;
    pinMode(right_front_forward,OUTPUT);
    pinMode(right_front_backward,OUTPUT);
    digitalWrite(right_front_forward, forward);
    digitalWrite(right_front_backward, backward);
}

}
void setVEngine3(int forward, int  backward) {
    int left_back_forward = 9;
    int left_back_backward = 10;
    pinMode(left_back_forward,OUTPUT);
    pinMode(left_back_backward,OUTPUT);
    digitalWrite(left_back_forward, forward);
    digitalWrite(left_back_backward, backward);
}

void setVEngine4(int forward, int  backward) {
    int right_back_forward = 11;
    int right_back_backward = 12;
    pinMode(right_back_forward,OUTPUT);
    pinMode(right_back_backward,OUTPUT);
    digitalWrite(right_back_forward, forward);
    digitalWrite(right_back_backward, backward);
}