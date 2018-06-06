
int getUS() {
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
    digitalWrite(left_front_forward, forward);
    digitalWrite(left_front_backward, backward);
}

void setVEngine2(int forward, int  backward) {
    digitalWrite(right_front_forward, forward);
    digitalWrite(right_front_backward, backward);
}

void setVEngine3(int forward, int  backward) {
    digitalWrite(left_back_forward, forward);
    digitalWrite(left_back_backward, backward);
}

void setVEngine4(int forward, int  backward) {
    digitalWrite(right_back_forward, forward);
    digitalWrite(right_back_backward, backward);
}
