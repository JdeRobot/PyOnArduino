import ast
import unittest
import sys

try:
    sys.path.append (".")
    import translator.Translator as translator
    import translator.TranslatorVariables as vars
    import translator.strings.TranslatorStrings as strings
except ModuleNotFoundError:
    print('Import failed')


class MBotExamplesTests(unittest.TestCase):
    def setUp(self):
        global visitor
        vars.Variables()
        translator.vars = vars
        translator.strings = strings
        translator.robot = 'MBot'
        translator.robot_architecture = ''
        vars.halduino_directory = 'HALduino/halduino'
        visitor = translator.TranslatorVisitor()

    def trim (self, st : str):
        return ' '.join(st.replace('\n', ' ').split())

    def translate_string(self, text):
        parsed_statement = ast.parse(text)
        visitor.visit(parsed_statement)
        return parsed_statement

    def test_button_test(self):
        self.translate_string('''def loop():
    if halduino.isButtonPressed():
        halduino.playBuzzer(330, 1000)
    elif halduino.isButtonReleased() is True:
        halduino.playBuzzer(249, 1000)''')
        expected_statement = '''void loop() {
if (isButtonPressed()) {
DynType var0;var0.tvar = INT;String har0 = "330";har0.toCharArray(var0.data, MinTypeSz);
DynType var1;var1.tvar = INT;String har1 = "1000";har1.toCharArray(var1.data, MinTypeSz);
playBuzzer(var0,var1);
   } else if ((isButtonReleased() == true)) {
DynType var2;var2.tvar = INT;String har2 = "249";har2.toCharArray(var2.data, MinTypeSz);
DynType var3;var3.tvar = INT;String har3 = "1000";har3.toCharArray(var3.data, MinTypeSz);
playBuzzer(var2,var3);
   }
}
'''
        self.assertEqual(self.trim (expected_statement), self.trim (vars.function_def))

    def test_buzzer_test(self):
        self.translate_string('''from time import sleep

import HALduino.halduino as halduino

def loop():
    halduino.playBuzzer(330, 1000)
    halduino.playBuzzer(330, 1000)
    halduino.playBuzzer(349, 1000)
    halduino.playBuzzer(392, 1000)
    halduino.playBuzzer(392, 1000)
    halduino.playBuzzer(349, 1000)
    halduino.playBuzzer(330, 1000)
    halduino.playBuzzer(294, 1000)
    halduino.playBuzzer(262, 1000)
    halduino.playBuzzer(262, 1000)
    halduino.playBuzzer(294, 1000)
    halduino.playBuzzer(330, 1000)
    halduino.playBuzzer(330, 1500)
    halduino.playBuzzer(294, 500)
    halduino.playBuzzer(294, 2000)
    halduino.playBuzzer(330, 1000)
    halduino.playBuzzer(330, 1000)
    halduino.playBuzzer(349, 1000)
    halduino.playBuzzer(392, 1000)
    halduino.playBuzzer(392, 1000)
    halduino.playBuzzer(349, 1000)
    halduino.playBuzzer(330, 1000)
    halduino.playBuzzer(294, 1000)
    halduino.playBuzzer(262, 1000)
    halduino.playBuzzer(262, 1000)
    halduino.playBuzzer(294, 1000)
    halduino.playBuzzer(330, 1000)
    halduino.playBuzzer(294, 1500)
    halduino.playBuzzer(262, 500)
    halduino.playBuzzer(262, 1000)
    sleep(1000)''')
        expected_statement = '''void loop() {
DynType var0;var0.tvar = INT;String har0 = "330";har0.toCharArray(var0.data, MinTypeSz);
DynType var1;var1.tvar = INT;String har1 = "1000";har1.toCharArray(var1.data, MinTypeSz);
playBuzzer(var0,var1);
   DynType var2;var2.tvar = INT;String har2 = "330";har2.toCharArray(var2.data, MinTypeSz);
DynType var3;var3.tvar = INT;String har3 = "1000";har3.toCharArray(var3.data, MinTypeSz);
playBuzzer(var2,var3);
   DynType var4;var4.tvar = INT;String har4 = "349";har4.toCharArray(var4.data, MinTypeSz);
DynType var5;var5.tvar = INT;String har5 = "1000";har5.toCharArray(var5.data, MinTypeSz);
playBuzzer(var4,var5);
   DynType var6;var6.tvar = INT;String har6 = "392";har6.toCharArray(var6.data, MinTypeSz);
DynType var7;var7.tvar = INT;String har7 = "1000";har7.toCharArray(var7.data, MinTypeSz);
playBuzzer(var6,var7);
   DynType var8;var8.tvar = INT;String har8 = "392";har8.toCharArray(var8.data, MinTypeSz);
DynType var9;var9.tvar = INT;String har9 = "1000";har9.toCharArray(var9.data, MinTypeSz);
playBuzzer(var8,var9);
   DynType var10;var10.tvar = INT;String har10 = "349";har10.toCharArray(var10.data, MinTypeSz);
DynType var11;var11.tvar = INT;String har11 = "1000";har11.toCharArray(var11.data, MinTypeSz);
playBuzzer(var10,var11);
   DynType var12;var12.tvar = INT;String har12 = "330";har12.toCharArray(var12.data, MinTypeSz);
DynType var13;var13.tvar = INT;String har13 = "1000";har13.toCharArray(var13.data, MinTypeSz);
playBuzzer(var12,var13);
   DynType var14;var14.tvar = INT;String har14 = "294";har14.toCharArray(var14.data, MinTypeSz);
DynType var15;var15.tvar = INT;String har15 = "1000";har15.toCharArray(var15.data, MinTypeSz);
playBuzzer(var14,var15);
   DynType var16;var16.tvar = INT;String har16 = "262";har16.toCharArray(var16.data, MinTypeSz);
DynType var17;var17.tvar = INT;String har17 = "1000";har17.toCharArray(var17.data, MinTypeSz);
playBuzzer(var16,var17);
   DynType var18;var18.tvar = INT;String har18 = "262";har18.toCharArray(var18.data, MinTypeSz);
DynType var19;var19.tvar = INT;String har19 = "1000";har19.toCharArray(var19.data, MinTypeSz);
playBuzzer(var18,var19);
   DynType var20;var20.tvar = INT;String har20 = "294";har20.toCharArray(var20.data, MinTypeSz);
DynType var21;var21.tvar = INT;String har21 = "1000";har21.toCharArray(var21.data, MinTypeSz);
playBuzzer(var20,var21);
   DynType var22;var22.tvar = INT;String har22 = "330";har22.toCharArray(var22.data, MinTypeSz);
DynType var23;var23.tvar = INT;String har23 = "1000";har23.toCharArray(var23.data, MinTypeSz);
playBuzzer(var22,var23);
   DynType var24;var24.tvar = INT;String har24 = "330";har24.toCharArray(var24.data, MinTypeSz);
DynType var25;var25.tvar = INT;String har25 = "1500";har25.toCharArray(var25.data, MinTypeSz);
playBuzzer(var24,var25);
   DynType var26;var26.tvar = INT;String har26 = "294";har26.toCharArray(var26.data, MinTypeSz);
DynType var27;var27.tvar = INT;String har27 = "500";har27.toCharArray(var27.data, MinTypeSz);
playBuzzer(var26,var27);
   DynType var28;var28.tvar = INT;String har28 = "294";har28.toCharArray(var28.data, MinTypeSz);
DynType var29;var29.tvar = INT;String har29 = "2000";har29.toCharArray(var29.data, MinTypeSz);
playBuzzer(var28,var29);
   DynType var30;var30.tvar = INT;String har30 = "330";har30.toCharArray(var30.data, MinTypeSz);
DynType var31;var31.tvar = INT;String har31 = "1000";har31.toCharArray(var31.data, MinTypeSz);
playBuzzer(var30,var31);
   DynType var32;var32.tvar = INT;String har32 = "330";har32.toCharArray(var32.data, MinTypeSz);
DynType var33;var33.tvar = INT;String har33 = "1000";har33.toCharArray(var33.data, MinTypeSz);
playBuzzer(var32,var33);
   DynType var34;var34.tvar = INT;String har34 = "349";har34.toCharArray(var34.data, MinTypeSz);
DynType var35;var35.tvar = INT;String har35 = "1000";har35.toCharArray(var35.data, MinTypeSz);
playBuzzer(var34,var35);
   DynType var36;var36.tvar = INT;String har36 = "392";har36.toCharArray(var36.data, MinTypeSz);
DynType var37;var37.tvar = INT;String har37 = "1000";har37.toCharArray(var37.data, MinTypeSz);
playBuzzer(var36,var37);
   DynType var38;var38.tvar = INT;String har38 = "392";har38.toCharArray(var38.data, MinTypeSz);
DynType var39;var39.tvar = INT;String har39 = "1000";har39.toCharArray(var39.data, MinTypeSz);
playBuzzer(var38,var39);
   DynType var40;var40.tvar = INT;String har40 = "349";har40.toCharArray(var40.data, MinTypeSz);
DynType var41;var41.tvar = INT;String har41 = "1000";har41.toCharArray(var41.data, MinTypeSz);
playBuzzer(var40,var41);
   DynType var42;var42.tvar = INT;String har42 = "330";har42.toCharArray(var42.data, MinTypeSz);
DynType var43;var43.tvar = INT;String har43 = "1000";har43.toCharArray(var43.data, MinTypeSz);
playBuzzer(var42,var43);
   DynType var44;var44.tvar = INT;String har44 = "294";har44.toCharArray(var44.data, MinTypeSz);
DynType var45;var45.tvar = INT;String har45 = "1000";har45.toCharArray(var45.data, MinTypeSz);
playBuzzer(var44,var45);
   DynType var46;var46.tvar = INT;String har46 = "262";har46.toCharArray(var46.data, MinTypeSz);
DynType var47;var47.tvar = INT;String har47 = "1000";har47.toCharArray(var47.data, MinTypeSz);
playBuzzer(var46,var47);
   DynType var48;var48.tvar = INT;String har48 = "262";har48.toCharArray(var48.data, MinTypeSz);
DynType var49;var49.tvar = INT;String har49 = "1000";har49.toCharArray(var49.data, MinTypeSz);
playBuzzer(var48,var49);
   DynType var50;var50.tvar = INT;String har50 = "294";har50.toCharArray(var50.data, MinTypeSz);
DynType var51;var51.tvar = INT;String har51 = "1000";har51.toCharArray(var51.data, MinTypeSz);
playBuzzer(var50,var51);
   DynType var52;var52.tvar = INT;String har52 = "330";har52.toCharArray(var52.data, MinTypeSz);
DynType var53;var53.tvar = INT;String har53 = "1000";har53.toCharArray(var53.data, MinTypeSz);
playBuzzer(var52,var53);
   DynType var54;var54.tvar = INT;String har54 = "294";har54.toCharArray(var54.data, MinTypeSz);
DynType var55;var55.tvar = INT;String har55 = "1500";har55.toCharArray(var55.data, MinTypeSz);
playBuzzer(var54,var55);
   DynType var56;var56.tvar = INT;String har56 = "262";har56.toCharArray(var56.data, MinTypeSz);
DynType var57;var57.tvar = INT;String har57 = "500";har57.toCharArray(var57.data, MinTypeSz);
playBuzzer(var56,var57);
   DynType var58;var58.tvar = INT;String har58 = "262";har58.toCharArray(var58.data, MinTypeSz);
DynType var59;var59.tvar = INT;String har59 = "1000";har59.toCharArray(var59.data, MinTypeSz);
playBuzzer(var58,var59);
   delay(1000);
   }
'''
        self.assertEqual(self.trim(expected_statement), self.trim(vars.function_def))

    def test_draw_string_test(self):
        self.translate_string('''def loop():
    halduino.drawString('Hi!')''')
        expected_statement = '''void loop() {
DynType var0;var0.tvar = STR;String har0 = "Hi!";har0.toCharArray(var0.data, MinTypeSz);
drawString(var0);
   }
'''
        self.assertEqual(self.trim(expected_statement), self.trim(vars.function_def))

    def test_get_message_test(self):
        self.translate_string('''def loop():
    print(halduino.getMessage())''')
        expected_statement = '''void loop() {
Serial.print(getMessage());
   }
'''
        self.assertEqual(self.trim(expected_statement), self.trim(vars.function_def))

    def test_hitnrotate_test(self):
        self.translate_string('''def set_engine(direction: int):
    if direction == 0:
        halduino.setSpeedEngines(0, 0)
        sleep(500)
        halduino.setSpeedEngines(-100, -100)
        sleep(500)
        halduino.setSpeedEngines(100, 0)
        sleep(500)
        print('Rotate!')
    elif direction == 1:
        halduino.setSpeedEngines(100, 100)
        print('Forward')''')
        expected_statement = '''void set_engine(DynType direction) {
if ((atoi(direction.data) == 0)) {
DynType var0;var0.tvar = INT;String har0 = "0";har0.toCharArray(var0.data, MinTypeSz);
DynType var1;var1.tvar = INT;String har1 = "0";har1.toCharArray(var1.data, MinTypeSz);
setSpeedEngines(var0,var1);
   delay(500);
   DynType var3;var3.tvar = INT;String har3 = "-100";har3.toCharArray(var3.data, MinTypeSz);
DynType var4;var4.tvar = INT;String har4 = "-100";har4.toCharArray(var4.data, MinTypeSz);
setSpeedEngines(var3,var4);
   delay(500);
   DynType var6;var6.tvar = INT;String har6 = "100";har6.toCharArray(var6.data, MinTypeSz);
DynType var7;var7.tvar = INT;String har7 = "0";har7.toCharArray(var7.data, MinTypeSz);
setSpeedEngines(var6,var7);
   delay(500);
   DynType var9;var9.tvar = STR;String har9 = "Rotate!";har9.toCharArray(var9.data, MinTypeSz);
Serial.print(var9.data);
   } else if ((atoi(direction.data) == 1)) {
DynType var10;var10.tvar = INT;String har10 = "100";har10.toCharArray(var10.data, MinTypeSz);
DynType var11;var11.tvar = INT;String har11 = "100";har11.toCharArray(var11.data, MinTypeSz);
setSpeedEngines(var10,var11);
   DynType var12;var12.tvar = STR;String har12 = "Forward";har12.toCharArray(var12.data, MinTypeSz);
Serial.print(var12.data);
   }
}
'''
        self.assertEqual(self.trim(expected_statement), self.trim(vars.function_def))
        self.translate_string('''def loop():
    if halduino.getUS() < 30:
        set_engine(0)
    else:
        set_engine(1)''')
        expected_statement = '''void loop() {
if ((getUS() < 30)) {
DynType var13;var13.tvar = INT;String har13 = "0";har13.toCharArray(var13.data, MinTypeSz);
set_engine(var13);
   } else {
DynType var14;var14.tvar = INT;String har14 = "1";har14.toCharArray(var14.data, MinTypeSz);
set_engine(var14);
   }
}
'''
        self.assertEqual(self.trim(expected_statement), self.trim(vars.function_def))

    def test_leds_test(self):
        self.translate_string('''def loop():
    halduino.setLeds(0, 150, 0, 0)
    sleep(500)
    halduino.setLeds(1, 0, 150, 0)
    sleep(500)
    halduino.setLeds(2, 0, 0, 150)
    sleep(500)
    halduino.setLeds(0, 150, 150, 150)
    sleep(500)''')
        expected_statement = '''void loop() {
DynType var0;var0.tvar = INT;String har0 = "0";har0.toCharArray(var0.data, MinTypeSz);
DynType var1;var1.tvar = INT;String har1 = "150";har1.toCharArray(var1.data, MinTypeSz);
DynType var2;var2.tvar = INT;String har2 = "0";har2.toCharArray(var2.data, MinTypeSz);
DynType var3;var3.tvar = INT;String har3 = "0";har3.toCharArray(var3.data, MinTypeSz);
setLeds(var0,var1,var2,var3);
   delay(500);
   DynType var5;var5.tvar = INT;String har5 = "1";har5.toCharArray(var5.data, MinTypeSz);
DynType var6;var6.tvar = INT;String har6 = "0";har6.toCharArray(var6.data, MinTypeSz);
DynType var7;var7.tvar = INT;String har7 = "150";har7.toCharArray(var7.data, MinTypeSz);
DynType var8;var8.tvar = INT;String har8 = "0";har8.toCharArray(var8.data, MinTypeSz);
setLeds(var5,var6,var7,var8);
   delay(500);
   DynType var10;var10.tvar = INT;String har10 = "2";har10.toCharArray(var10.data, MinTypeSz);
DynType var11;var11.tvar = INT;String har11 = "0";har11.toCharArray(var11.data, MinTypeSz);
DynType var12;var12.tvar = INT;String har12 = "0";har12.toCharArray(var12.data, MinTypeSz);
DynType var13;var13.tvar = INT;String har13 = "150";har13.toCharArray(var13.data, MinTypeSz);
setLeds(var10,var11,var12,var13);
   delay(500);
   DynType var15;var15.tvar = INT;String har15 = "0";har15.toCharArray(var15.data, MinTypeSz);
DynType var16;var16.tvar = INT;String har16 = "150";har16.toCharArray(var16.data, MinTypeSz);
DynType var17;var17.tvar = INT;String har17 = "150";har17.toCharArray(var17.data, MinTypeSz);
DynType var18;var18.tvar = INT;String har18 = "150";har18.toCharArray(var18.data, MinTypeSz);
setLeds(var15,var16,var17,var18);
   delay(500);
   }
'''
        self.assertEqual(self.trim(expected_statement), self.trim(vars.function_def))

    def test_light_sensor_test(self):
        self.translate_string('''def set_engine(direction: int):
    if direction == 0:
        halduino.setSpeedEngines(0, 0)
        sleep(500)
        halduino.playBuzzer(330, 1000)
        halduino.setSpeedEngines(-100, -100)
        sleep(500)
        halduino.setSpeedEngines(100, 0)
        sleep(1200)
    elif direction == 1:
        halduino.setSpeedEngines(100, 100)''')
        expected_statement = '''void set_engine(DynType direction) {
if ((atoi(direction.data) == 0)) {
DynType var0;var0.tvar = INT;String har0 = "0";har0.toCharArray(var0.data, MinTypeSz);
DynType var1;var1.tvar = INT;String har1 = "0";har1.toCharArray(var1.data, MinTypeSz);
setSpeedEngines(var0,var1);
   delay(500);
   DynType var3;var3.tvar = INT;String har3 = "330";har3.toCharArray(var3.data, MinTypeSz);
DynType var4;var4.tvar = INT;String har4 = "1000";har4.toCharArray(var4.data, MinTypeSz);
playBuzzer(var3,var4);
   DynType var5;var5.tvar = INT;String har5 = "-100";har5.toCharArray(var5.data, MinTypeSz);
DynType var6;var6.tvar = INT;String har6 = "-100";har6.toCharArray(var6.data, MinTypeSz);
setSpeedEngines(var5,var6);
   delay(500);
   DynType var8;var8.tvar = INT;String har8 = "100";har8.toCharArray(var8.data, MinTypeSz);
DynType var9;var9.tvar = INT;String har9 = "0";har9.toCharArray(var9.data, MinTypeSz);
setSpeedEngines(var8,var9);
   delay(1200);
   } else if ((atoi(direction.data) == 1)) {
DynType var11;var11.tvar = INT;String har11 = "100";har11.toCharArray(var11.data, MinTypeSz);
DynType var12;var12.tvar = INT;String har12 = "100";har12.toCharArray(var12.data, MinTypeSz);
setSpeedEngines(var11,var12);
   }
}
'''
        self.assertEqual(self.trim(expected_statement), self.trim(vars.function_def))
        self.translate_string('''def loop():
    if halduino.getLightSensor() < 100:
        set_engine(0)
    else:
        set_engine(1)''')
        expected_statement = '''void loop() {
if ((getLightSensor() < 100)) {
DynType var13;var13.tvar = INT;String har13 = "0";har13.toCharArray(var13.data, MinTypeSz);
set_engine(var13);
   } else {
DynType var14;var14.tvar = INT;String har14 = "1";har14.toCharArray(var14.data, MinTypeSz);
set_engine(var14);
   }
}
'''
        self.assertEqual(self.trim(expected_statement), self.trim(vars.function_def))

    def test_line_follow_test(self):
        self.translate_string('''def loop():
    if halduino.getLineFollowValue() == 0:
        halduino.setSpeedEngines(100, 100)
    elif halduino.getLineFollowValue() == 1:
        halduino.setSpeedEngines(0, 100)
    elif halduino.getLineFollowValue() == 2:
        halduino.setSpeedEngines(100, 0)
    elif halduino.getLineFollowValue() == 3:
        halduino.setSpeedEngines(-100, -100)''')
        expected_statement = '''void loop() {
if ((getLineFollowValue() == 0)) {
DynType var0;var0.tvar = INT;String har0 = "100";har0.toCharArray(var0.data, MinTypeSz);
DynType var1;var1.tvar = INT;String har1 = "100";har1.toCharArray(var1.data, MinTypeSz);
setSpeedEngines(var0,var1);
   } else if ((getLineFollowValue() == 1)) {
DynType var2;var2.tvar = INT;String har2 = "0";har2.toCharArray(var2.data, MinTypeSz);
DynType var3;var3.tvar = INT;String har3 = "100";har3.toCharArray(var3.data, MinTypeSz);
setSpeedEngines(var2,var3);
   } else if ((getLineFollowValue() == 2)) {
DynType var4;var4.tvar = INT;String har4 = "100";har4.toCharArray(var4.data, MinTypeSz);
DynType var5;var5.tvar = INT;String har5 = "0";har5.toCharArray(var5.data, MinTypeSz);
setSpeedEngines(var4,var5);
   } else if ((getLineFollowValue() == 3)) {
DynType var6;var6.tvar = INT;String har6 = "-100";har6.toCharArray(var6.data, MinTypeSz);
DynType var7;var7.tvar = INT;String har7 = "-100";har7.toCharArray(var7.data, MinTypeSz);
setSpeedEngines(var6,var7);
   }
}
'''
        function_def = vars.function_def
        self.assertEqual(self.trim(expected_statement), self.trim(vars.function_def))
        self.translate_string('''def setup():
    while halduino.isButtonPressed() is False:
        pass''')
        expected_statement = '''void setup() {
while(isButtonPressed() == false) {}
}
'''
        self.assertEqual(self.trim(expected_statement), self.trim(vars.function_def))

    def test_send_message_test(self):
        self.translate_string('''def loop():
    if halduino.isButtonPressed():
        halduino.sendMessage('hello')
        halduino.playBuzzer(330, 500)''')
        expected_statement = '''void loop() {
if (isButtonPressed()) {
DynType var0;var0.tvar = STR;String har0 = "hello";har0.toCharArray(var0.data, MinTypeSz);
sendMessage(var0);
   DynType var1;var1.tvar = INT;String har1 = "330";har1.toCharArray(var1.data, MinTypeSz);
DynType var2;var2.tvar = INT;String har2 = "500";har2.toCharArray(var2.data, MinTypeSz);
playBuzzer(var1,var2);
   }
}
'''
        self.assertEqual(self.trim(expected_statement), self.trim(vars.function_def))

    def test_show_time_test(self):
        self.translate_string('''def loop():
    hour = 19
    min = 20
    halduino.showClock(hour, min)''')
        expected_statement = '''void loop() {
DynType hour;hour.tvar = INT;String har0 = "19";har0.toCharArray(hour.data, MinTypeSz);
DynType min;min.tvar = INT;String har1 = "20";har1.toCharArray(min.data, MinTypeSz);
showClock(hour,min);
   }
'''
        self.assertEqual(self.trim(expected_statement), self.trim(vars.function_def))

    def test_stopngo_test(self):
        self.translate_string('''def set_engine(direction: int):
    if direction == 0:
        halduino.setSpeedEngines(0, 0)
        print('STOP!')
    elif direction == 1:
        halduino.setSpeedEngines(100, 100)
        print('Forward')''')
        expected_statement = '''void set_engine(DynType direction) {
if ((atoi(direction.data) == 0)) {
DynType var0;var0.tvar = INT;String har0 = "0";har0.toCharArray(var0.data, MinTypeSz);
DynType var1;var1.tvar = INT;String har1 = "0";har1.toCharArray(var1.data, MinTypeSz);
setSpeedEngines(var0,var1);
   DynType var2;var2.tvar = STR;String har2 = "STOP!";har2.toCharArray(var2.data, MinTypeSz);
Serial.print(var2.data);
   } else if ((atoi(direction.data) == 1)) {
DynType var3;var3.tvar = INT;String har3 = "100";har3.toCharArray(var3.data, MinTypeSz);
DynType var4;var4.tvar = INT;String har4 = "100";har4.toCharArray(var4.data, MinTypeSz);
setSpeedEngines(var3,var4);
   DynType var5;var5.tvar = STR;String har5 = "Forward";har5.toCharArray(var5.data, MinTypeSz);
Serial.print(var5.data);
   }
}
'''
        self.assertEqual(self.trim(expected_statement), self.trim(vars.function_def))
        self.translate_string('''def loop():
    if halduino.getUS() < 10:
        set_engine(0)
    else:
        set_engine(1)''')
        expected_statement = '''void loop() {
if ((getUS() < 10)) {
DynType var6;var6.tvar = INT;String har6 = "0";har6.toCharArray(var6.data, MinTypeSz);
set_engine(var6);
   } else {
DynType var7;var7.tvar = INT;String har7 = "1";har7.toCharArray(var7.data, MinTypeSz);
set_engine(var7);
   }
}
'''
        self.assertEqual(self.trim(expected_statement), self.trim(vars.function_def))


if __name__ == '__main__':
   m = MBotExamplesTests()
   m.setUp()
   m.test_buzzer_test()