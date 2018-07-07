import ast
import unittest
import translator.Translator as translator

class ComplubotExamplesTests(unittest.TestCase):
    def setUp(self):
        global visitor
        translator.function_def = ''
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
playBeep(0);
   delay(100);
   playBeep(1);
   delay(100);
   playBeep(2);
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
        print('Forward')

def loop():
    if halduino.getUS() < 30:
        set_engine(0)
    else:
        set_engine(1)''')
        expected_statement = '''void loop() {
if ((getUS() < 30)) {
set_engine(0);
   } else {
set_engine(1);
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
setSpeedEngines(0,110);
   } else {
setSpeedEngines(110,0);
   }
}
'''
        self.assertEqual(expected_statement, translator.function_def)


    def test_line_follow_test(self):
        self.translate_string('''import HALduino.halduino as halduino

def setup():
    halduino.lineFollow(11,5,50,10)''')
        expected_statement = '''void setup() {
lineFollow(11,5,50,10);
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
setScreenText("Hello World!",5,5);
   delay(2000);
   clearScreen();
   setScreenText("Complubot!!",5,5);
   delay(2000);
   clearScreen();
   }
'''
        self.assertEqual(expected_statement, translator.function_def)

    def test_stop_n_go_test(self):
        self.translate_string('''import HALduino.halduino as halduino

def set_engine(direction: int):
    if direction == 0:
        halduino.setSpeedEngines(0, 0)
        print('STOP!')
    elif direction == 1:
        halduino.setSpeedEngines(100, 100)
        print('Forward')

def loop():
    if halduino.getUS() < 30:
        set_engine(0)
    else:
        set_engine(1)''')
        expected_statement = '''void loop() {
if ((getUS() < 30)) {
set_engine(0);
   } else {
set_engine(1);
   }
}
'''
        self.assertEqual(expected_statement, translator.function_def)