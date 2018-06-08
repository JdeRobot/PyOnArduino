void setup() {
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
}void set_engine(int direction) {
if (direction == 0) {
  setVEngine1(0, 0);
   setVEngine2(0, 0);
   setVEngine3(0, 0);
   setVEngine4(0, 0);
   Serial.print("STOP!");
   } else if (direction == 1) {
  setVEngine1(0, 1);
   setVEngine2(0, 1);
   setVEngine3(0, 1);
   setVEngine4(0, 1);
   Serial.print("Forward");
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
void loop() {
delay(100);
   if (getUS() < 10) {
  set_engine(0);
   } else {
   set_engine(1);
   }
Serial.print(5 + 33 - 4 * 4);
   Serial.print(5 - 3 / 5);
   Serial.print(5 * 3);
   Serial.print(5 / 3);
   Serial.print(5 % 3);
   int y[] = {1,2,3,4};
for(int x = 0; sizeof(y); x++) {
Serial.print(x);
   }
if (true) {
  Serial.print("HELLO");
   } else if (getUS() <= 10) {
  set_engine(0);
   } else {
   set_engine(1);
   }
}
void print_name_surname(String name, String surname, String second, String another) {
Serial.print(name + surname + second + another);
   }
