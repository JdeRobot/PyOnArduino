import ast
import unittest
import translator.Translator as translator

try:
    import translator.TranslatorVariables as vars
    import translator.strings.TranslatorStrings as strings
except ModuleNotFoundError:
    print('Import failed')


class ComplubotExamplesTests(unittest.TestCase):
    def setUp(self):
        global visitor
        vars.Variables()
        translator.vars = vars
        translator.strings = strings
        translator.robot = 'ComplubotControl'
        vars.halduino_directory = '../HALduino/halduino'
        visitor = translator.TranslatorVisitor()

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
        self.assertEqual(expected_statement, vars.function_def)

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
        self.assertEqual(expected_statement, vars.function_def)
        self.translate_string('''
def loop():
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
        self.assertEqual(expected_statement, vars.function_def)

    def test_ir_test(self):
        translator.robot = 'ComplubotMotor'
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
    print(' ')
''')
        expected_statement = '''void loop() {
delay(100);
   Serial.print(getIR1());
   DynType var1;var1.tvar = CHAR;String har1 = " ";har1.toCharArray(var1.data, MinTypeSz);
Serial.print(var1.data);
   Serial.print(getIR2());
   DynType var2;var2.tvar = CHAR;String har2 = " ";har2.toCharArray(var2.data, MinTypeSz);
Serial.print(var2.data);
   Serial.print(getIR3());
   DynType var3;var3.tvar = CHAR;String har3 = " ";har3.toCharArray(var3.data, MinTypeSz);
Serial.print(var3.data);
   Serial.print(getIR4());
   DynType var4;var4.tvar = CHAR;String har4 = " ";har4.toCharArray(var4.data, MinTypeSz);
Serial.print(var4.data);
   Serial.print(getIR5());
   DynType var5;var5.tvar = CHAR;String har5 = " ";har5.toCharArray(var5.data, MinTypeSz);
Serial.print(var5.data);
   }
'''
        self.assertEqual(expected_statement, vars.function_def)

    def test_line_follow_no_library_test(self):
        translator.robot = 'ComplubotMotor'
        self.translate_string('''import HALduino.halduino as halduino


def loop():
    if halduino.getIR3() < 300:
        halduino.setSpeedEngines(110, 110)
    if halduino.getIR2() < 300:
        halduino.setSpeedEngines(110, 0)
    if halduino.getIR4() < 300:
        halduino.setSpeedEngines(0, 110)''')
        expected_statement = '''void loop() {
if ((getIR3() < 300)) {
DynType var0;var0.tvar = INT;String har0 = "110";har0.toCharArray(var0.data, MinTypeSz);
DynType var1;var1.tvar = INT;String har1 = "110";har1.toCharArray(var1.data, MinTypeSz);
setSpeedEngines(var0,var1);
   }
if ((getIR2() < 300)) {
DynType var2;var2.tvar = INT;String har2 = "110";har2.toCharArray(var2.data, MinTypeSz);
DynType var3;var3.tvar = INT;String har3 = "0";har3.toCharArray(var3.data, MinTypeSz);
setSpeedEngines(var2,var3);
   }
if ((getIR4() < 300)) {
DynType var4;var4.tvar = INT;String har4 = "0";har4.toCharArray(var4.data, MinTypeSz);
DynType var5;var5.tvar = INT;String har5 = "110";har5.toCharArray(var5.data, MinTypeSz);
setSpeedEngines(var4,var5);
   }
}
'''
        self.assertEqual(expected_statement, vars.function_def)

    def test_line_follow_test(self):
        translator.robot = 'ComplubotMotor'
        self.translate_string('''import HALduino.halduino as halduino


def loop():
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
        self.assertEqual(expected_statement, vars.function_def)

    def test_melody_test(self):
        self.translate_string('''import HALduino.halduino as halduino

def loop():
    melody = "8eF-FFga4b.a.g.F.8beee-d2e.1-"
    halduino.playMelody(melody)''')
        expected_statement = '''void loop() {
DynType melody;melody.tvar = STR;String har0 = "8eF-FFga4b.a.g.F.8beee-d2e.1-";har0.toCharArray(melody.data, MinTypeSz);
playMelody(melody);
   }
'''
        self.assertEqual(expected_statement, vars.function_def)

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
DynType var0;var0.tvar = STR;String har0 = "Hello World!";har0.toCharArray(var0.data, MinTypeSz);
DynType var1;var1.tvar = INT;String har1 = "5";har1.toCharArray(var1.data, MinTypeSz);
DynType var2;var2.tvar = INT;String har2 = "5";har2.toCharArray(var2.data, MinTypeSz);
setScreenText(var0,var1,var2);
   delay(2000);
   clearScreen();
   DynType var4;var4.tvar = STR;String har4 = "Complubot!!";har4.toCharArray(var4.data, MinTypeSz);
DynType var5;var5.tvar = INT;String har5 = "5";har5.toCharArray(var5.data, MinTypeSz);
DynType var6;var6.tvar = INT;String har6 = "5";har6.toCharArray(var6.data, MinTypeSz);
setScreenText(var4,var5,var6);
   delay(2000);
   clearScreen();
   }
'''
        function_def = vars.function_def
        self.assertEqual(expected_statement, vars.function_def)

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
        self.assertEqual(expected_statement, vars.function_def)
        self.translate_string('''import HALduino.halduino as halduino

def loop():
    if halduino.getUS() < 30:
        set_engine(0)
    else:
        set_engine(1)''')
        expected_statement = '''void loop() {
if ((getUS() < 30)) {
DynType var6;var6.tvar = INT;String har6 = "0";har6.toCharArray(var6.data, MinTypeSz);
set_engine(var6);
   } else {
DynType var7;var7.tvar = INT;String har7 = "1";har7.toCharArray(var7.data, MinTypeSz);
set_engine(var7);
   }
}
'''
        self.assertEqual(expected_statement, vars.function_def)
