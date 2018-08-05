import ast
import unittest
import translator.Translator as translator

try:
    import translator.TranslatorVariables as vars
    import translator.strings.TranslatorStrings as strings
except ModuleNotFoundError:
    print('Absolute import failed')


class SergioExamplesTests(unittest.TestCase):
    def setUp(self):
        global visitor
        vars.Variables()
        translator.vars = vars
        translator.strings = strings
        vars.halduino_directory = '../HALduino/halduino'
        translator.robot = 'SergioRobot'
        visitor = translator.TranslatorVisitor()

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
        self.assertEqual(expected_statement, vars.function_def)

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
        expected_statement = '''void set_engine(DynType direction) {
if ((atoi(direction.data) == 0)) {
DynType var0;var0.tvar = INT;String har0 = "0";har0.toCharArray(var0.data, MinTypeSz);
setSpeedEngine1(var0);
   DynType var1;var1.tvar = INT;String har1 = "0";har1.toCharArray(var1.data, MinTypeSz);
setSpeedEngine2(var1);
   DynType var2;var2.tvar = INT;String har2 = "0";har2.toCharArray(var2.data, MinTypeSz);
setSpeedEngine3(var2);
   DynType var3;var3.tvar = INT;String har3 = "0";har3.toCharArray(var3.data, MinTypeSz);
setSpeedEngine4(var3);
   DynType var4;var4.tvar = STR;String har4 = "STOP!";har4.toCharArray(var4.data, MinTypeSz);
Serial.print(var4.data);
   } else if ((atoi(direction.data) == 1)) {
DynType var5;var5.tvar = INT;String har5 = "255";har5.toCharArray(var5.data, MinTypeSz);
setSpeedEngine1(var5);
   DynType var6;var6.tvar = INT;String har6 = "255";har6.toCharArray(var6.data, MinTypeSz);
setSpeedEngine2(var6);
   DynType var7;var7.tvar = INT;String har7 = "255";har7.toCharArray(var7.data, MinTypeSz);
setSpeedEngine3(var7);
   DynType var8;var8.tvar = INT;String har8 = "255";har8.toCharArray(var8.data, MinTypeSz);
setSpeedEngine4(var8);
   DynType var9;var9.tvar = STR;String har9 = "Forward";har9.toCharArray(var9.data, MinTypeSz);
Serial.print(var9.data);
   }
}
'''
        self.assertEqual(expected_statement, vars.function_def)
        self.translate_string('''import HALduino.halduino as halduino

def loop():
    if halduino.getUS() < 10:
        set_engine(0)
    else:
        set_engine(1)''')
        expected_statement = '''void loop() {
if ((getUS() < 10)) {
DynType var10;var10.tvar = INT;String har10 = "0";har10.toCharArray(var10.data, MinTypeSz);
set_engine(var10);
   } else {
DynType var11;var11.tvar = INT;String har11 = "1";har11.toCharArray(var11.data, MinTypeSz);
set_engine(var11);
   }
}
'''
        self.assertEqual(expected_statement, vars.function_def)
