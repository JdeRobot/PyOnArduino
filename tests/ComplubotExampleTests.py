import ast
import unittest
import translator.Translator as translator

class ComplubotExamplesTests(unittest.TestCase):
    def setUp(self):
        global visitor
        translator.function_def = ''
        translator.variables_counter = 0
        translator.robot = 'Complubot'
        translator.halduino_directory = '../HALduino/halduino'
        visitor = translator.MyVisitor()

    def translate_string(self, text):
        parsed_statement = ast.parse(text)
        visitor.visit(parsed_statement)
        return parsed_statement

    def test_beep_test(self):
        self.translate_string('''from time import sleep
import HALduino.halduino as halduino


def loop():
    halduino.playBeep(0)
    sleep(100)
    halduino.playBeep(1)
    sleep(100)
    halduino.playBeep(2)
    sleep(100)''')
        expected_statement = '''void loop() {
DynType var0;var0.tvar = INT;String har0 = "0";har0.toCharArray(var0.data, MinTypeSz);
playBeep(var0);
   delay(100);
   DynType var2;var2.tvar = INT;String har2 = "1";har2.toCharArray(var2.data, MinTypeSz);
playBeep(var2);
   delay(100);
   DynType var4;var4.tvar = INT;String har4 = "2";har4.toCharArray(var4.data, MinTypeSz);
playBeep(var4);
   delay(100);
   }
'''
        self.assertEqual(expected_statement, translator.function_def)

    def test_hitnrotate_test(self):
        self.translate_string('''from time import sleep

import HALduino.halduino as halduino

def set_engine(direction: int):
    if direction == 0:
        halduino.setSpeedEngines(0, 0)
        sleep(500)
        halduino.setSpeedEngines(-100, -100)
        sleep(500)
        halduino.setSpeedEngines(100, 0)
        sleep(100)
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
   delay(100);
   Serial.print("Rotate!");
   } else if ((atoi(direction.data) == 1)) {
DynType var9;var9.tvar = INT;String har9 = "100";har9.toCharArray(var9.data, MinTypeSz);
DynType var10;var10.tvar = INT;String har10 = "100";har10.toCharArray(var10.data, MinTypeSz);
setSpeedEngines(var9,var10);
   Serial.print("Forward");
   }
}
'''
        self.assertEqual(expected_statement, translator.function_def)
        self.translate_string('''
def loop():
    if halduino.getUS() < 30:
        set_engine(0)
    else:
        set_engine(1)''')
        expected_statement = '''void loop() {
if ((getUS() < 30)) {
DynType var11;var11.tvar = INT;String har11 = "0";har11.toCharArray(var11.data, MinTypeSz);
set_engine(var11);
   } else {
DynType var12;var12.tvar = INT;String har12 = "1";har12.toCharArray(var12.data, MinTypeSz);
set_engine(var12);
   }
}
'''
        self.assertEqual(expected_statement, translator.function_def)

    def test_ir_test(self):
        self.translate_string('''from time import sleep

import HALduino.halduino as halduino

def loop():
    sleep(100)
    print(halduino.getIR1())
    print(' ')
    print(halduino.getIR2())
    print(' ')
    print(halduino.getIR3())
    print(' ')
    print(halduino.getIR4())
    print(' ')
    print(halduino.getIR5())
    print()
''')
        expected_statement = '''void loop() {
delay(100);
   Serial.print(getIR1());
   Serial.print(" ");
   Serial.print(getIR2());
   Serial.print(" ");
   Serial.print(getIR3());
   Serial.print(" ");
   Serial.print(getIR4());
   Serial.print(" ");
   Serial.print(getIR5());
   Serial.print();
   }
'''
        self.assertEqual(expected_statement, translator.function_def)


    def test_line_follow_no_library_test(self):
        self.translate_string('''import HALduino.halduino as halduino

def loop():
    if halduino.getIR2() < halduino.getIR4() and halduino.getIR5() < 990:
        halduino.setSpeedEngines(0,110)
    else:
        halduino.setSpeedEngines(110, 0)''')
        expected_statement = '''void loop() {
if ((getIR2() < getIR4()) && (getIR5() < 990)) {
DynType var0;var0.tvar = INT;String har0 = "0";har0.toCharArray(var0.data, MinTypeSz);
DynType var1;var1.tvar = INT;String har1 = "110";har1.toCharArray(var1.data, MinTypeSz);
setSpeedEngines(var0,var1);
   } else {
DynType var2;var2.tvar = INT;String har2 = "110";har2.toCharArray(var2.data, MinTypeSz);
DynType var3;var3.tvar = INT;String har3 = "0";har3.toCharArray(var3.data, MinTypeSz);
setSpeedEngines(var2,var3);
   }
}
'''
        self.assertEqual(expected_statement, translator.function_def)


    def test_line_follow_test(self):
        self.translate_string('''import HALduino.halduino as halduino

def setup():
    halduino.lineFollow(11,5,50,10)''')
        expected_statement = '''void setup() {
DynType var0;var0.tvar = INT;String har0 = "11";har0.toCharArray(var0.data, MinTypeSz);
DynType var1;var1.tvar = INT;String har1 = "5";har1.toCharArray(var1.data, MinTypeSz);
DynType var2;var2.tvar = INT;String har2 = "50";har2.toCharArray(var2.data, MinTypeSz);
DynType var3;var3.tvar = INT;String har3 = "10";har3.toCharArray(var3.data, MinTypeSz);
lineFollow(var0,var1,var2,var3);
   }
'''
        self.assertEqual(expected_statement, translator.function_def)

    def test_melody_test(self):
        self.translate_string('''import HALduino.halduino as halduino

def loop():
    melody = "8eF-FFga4b.a.g.F.8beee-d2e.1-"
    halduino.playMelody(melody)''')
        expected_statement = '''void loop() {
String melody = "8eF-FFga4b.a.g.F.8beee-d2e.1-";
playMelody(melody);
   }
'''
        self.assertEqual(expected_statement, translator.function_def)

    def test_screen_test_test(self):
        self.translate_string('''from time import sleep

import HALduino.halduino as halduino


def loop():
    halduino.setScreenText("Hello World!", 5, 5)
    sleep(2000)
    halduino.clearScreen()
    halduino.setScreenText("Complubot!!", 5, 5)
    sleep(2000)
    halduino.clearScreen()
''')
        expected_statement = '''void loop() {
DynType var0;var0.tvar = INT;String har0 = "5";har0.toCharArray(var0.data, MinTypeSz);
DynType var1;var1.tvar = INT;String har1 = "5";har1.toCharArray(var1.data, MinTypeSz);
setScreenText("Hello World!",var0,var1);
   delay(2000);
   clearScreen();
   DynType var3;var3.tvar = INT;String har3 = "5";har3.toCharArray(var3.data, MinTypeSz);
DynType var4;var4.tvar = INT;String har4 = "5";har4.toCharArray(var4.data, MinTypeSz);
setScreenText("Complubot!!",var3,var4);
   delay(2000);
   clearScreen();
   }
'''
        self.assertEqual(expected_statement, translator.function_def)

    def test_stopngo_test(self):
        self.translate_string('''import HALduino.halduino as halduino

def set_engine(direction: int):
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
   Serial.print("STOP!");
   } else if ((atoi(direction.data) == 1)) {
DynType var2;var2.tvar = INT;String har2 = "100";har2.toCharArray(var2.data, MinTypeSz);
DynType var3;var3.tvar = INT;String har3 = "100";har3.toCharArray(var3.data, MinTypeSz);
setSpeedEngines(var2,var3);
   Serial.print("Forward");
   }
}
'''
        self.assertEqual(expected_statement, translator.function_def)
        self.translate_string('''import HALduino.halduino as halduino

def loop():
    if halduino.getUS() < 30:
        set_engine(0)
    else:
        set_engine(1)''')
        expected_statement = '''void loop() {
if ((getUS() < 30)) {
DynType var4;var4.tvar = INT;String har4 = "0";har4.toCharArray(var4.data, MinTypeSz);
set_engine(var4);
   } else {
DynType var5;var5.tvar = INT;String har5 = "1";har5.toCharArray(var5.data, MinTypeSz);
set_engine(var5);
   }
}
'''
        self.assertEqual(expected_statement, translator.function_def)