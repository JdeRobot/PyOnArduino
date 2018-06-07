int left_front_forward = 5;
int left_front_backward = 4;
int right_front_forward = 2;
int right_front_backward = 6;
int left_back_forward = 9;
int left_back_backward = 10;
int right_back_forward = 11;
int right_back_backward = 12;
int echoUS = A5;
int triggerUS = A4;

void setup() {
    // put your setup code here, to run once:
pinMode(left_front_forward,OUTPUT);
pinMode(left_front_backward,OUTPUT);
pinMode(right_front_forward,OUTPUT);
pinMode(right_front_backward,OUTPUT);
pinMode(left_back_forward,OUTPUT);
pinMode(left_back_backward,OUTPUT);
pinMode(right_back_forward,OUTPUT);
pinMode(right_back_backward,OUTPUT);
pinMode(echoUS,INPUT);
pinMode(triggerUS,OUTPUT);

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
void set_engine(int direction) {
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
   }if (true) {
  Serial.print("HELLO");
   } else if (getUS() <= 10) {
  set_engine(0);
   } else {
   set_engine(1);
   }}
void print_name_surname(String name, String surname, String second, String another) {
Serial.print(name + surname + second + another);
   }
