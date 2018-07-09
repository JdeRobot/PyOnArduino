import ast
import unittest
import translator.Translator as translator

class ComplubotExamplesTests(unittest.TestCase):
    def setUp(self):
        global visitor
        translator.function_def = ''
        translator.robot = 'SergioRobot'
        translator.halduino_directory = '../HALduino/halduino'
        visitor = translator.MyVisitor()

    def translate_string(self, text):
        parsed_statement = ast.parse(text)
        visitor.visit(parsed_statement)
        return parsed_statement

    def test_ir_test(self):
        self.translate_string('''from time import sleep

import HALduino.halduino as halduino

def loop():
    sleep(100)
    print(halduino.getIR1())
''')
        expected_statement = '''void loop() {
delay(100);
   Serial.print(getIR1());
   }
'''
        self.assertEqual(expected_statement, translator.function_def)

    def test_stopngo_test(self):
        self.translate_string('''import HALduino.halduino as halduino

def set_engine(direction: int):
    if direction == 0:
        halduino.setSpeedEngine1(0)
        halduino.setSpeedEngine2(0)
        halduino.setSpeedEngine3(0)
        halduino.setSpeedEngine4(0)
        print('STOP!')
    elif direction == 1:
        halduino.setSpeedEngine1(255)
        halduino.setSpeedEngine2(255)
        halduino.setSpeedEngine3(255)
        halduino.setSpeedEngine4(255)
        print('Forward')''')
        expected_statement = '''void set_engine(int direction) {
if ((direction == 0)) {
setSpeedEngine1(0);
   setSpeedEngine2(0);
   setSpeedEngine3(0);
   setSpeedEngine4(0);
   Serial.print("STOP!");
   } else if ((direction == 1)) {
setSpeedEngine1(255);
   setSpeedEngine2(255);
   setSpeedEngine3(255);
   setSpeedEngine4(255);
   Serial.print("Forward");
   }
}
'''
        self.assertEqual(expected_statement, translator.function_def)
        self.translate_string('''import HALduino.halduino as halduino

def loop():
    if halduino.getUS() < 10:
        set_engine(0)
    else:
        set_engine(1)''')
        expected_statement = '''void loop() {
if ((getUS() < 10)) {
set_engine(0);
   } else {
set_engine(1);
   }
}
'''
        self.assertEqual(expected_statement, translator.function_def)
