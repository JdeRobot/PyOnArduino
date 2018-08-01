import ast
import unittest
import translator.Translator as translator
try:
    import translator.TranslatorVariables as vars
    vars.Variables()
except ModuleNotFoundError:
    print('Absolute import failed')

class TranslatorTests(unittest.TestCase):
    def setUp(self):
        global visitor
        translator.vars = vars
        vars.function_def = ''
        vars.variables_counter = 0
        translator.robot = 'Complubot'
        vars.halduino_directory = '../HALduino/halduino'
        visitor = translator.MyVisitor()

    def translate_string(self, text):
        parsed_statement = ast.parse(text)
        visitor.visit(parsed_statement)
        return parsed_statement

    def test_print_hello_world(self):
        self.translate_string('print(\'Hello World!\')')
        expected_statement = '''DynType var0;var0.tvar = STR;String har0 = "Hello World!";har0.toCharArray(var0.data, MinTypeSz);
Serial.print(var0.data);
   '''
        self.assertEqual(expected_statement, vars.function_def)

    def test_sleep(self):
        self.translate_string('sleep(100)')
        expected_statement = 'delay(100);\n   '
        self.assertEqual(expected_statement, vars.function_def)

    def test_boolean_true_var_declaration(self):
        self.translate_string('var = True')
        expected_statement = 'DynType var0;var0.tvar = BOOL;String har0 = "true";har0.toCharArray(var0.data, MinTypeSz);\n'
        self.assertEqual(expected_statement, vars.function_def)

    def test_boolean_false_var_declaration(self):
        self.translate_string('var = False')
        expected_statement = 'DynType var0;var0.tvar = BOOL;String har0 = "false";har0.toCharArray(var0.data, MinTypeSz);\n'
        self.assertEqual(expected_statement, vars.function_def)

    def test_integer_var_declaration(self):
        self.translate_string('var = 9')
        expected_statement = 'DynType var;var.tvar = INT;String har0 = "9";har0.toCharArray(var.data, MinTypeSz);\n'
        self.assertEqual(expected_statement, vars.function_def)

    def test_float_var_declaration(self):
        self.translate_string('var = 0.1')
        expected_statement = 'DynType var;var.tvar = FLOAT;String har0 = "0.1";har0.toCharArray(var.data, MinTypeSz);\n'
        self.assertEqual(expected_statement, vars.function_def)

    def test_char_var_declaration(self):
        self.translate_string('var = \'a\'')
        expected_statement = 'DynType var0;var0.tvar = CHAR;String har0 = "a";har0.toCharArray(var0.data, MinTypeSz);\n'
        self.assertEqual(expected_statement, vars.function_def)

    def test_string_var_declaration(self):
        self.translate_string('var = \'Hello World\'')
        expected_statement ='DynType var;var.tvar = STR;String har0 = "Hello World";har0.toCharArray(var.data, MinTypeSz);\n'
        self.assertEqual(expected_statement, vars.function_def)

    def test_operations_parentheses_1(self):
        self.translate_string('print(5 + 33 - 4 * 4)')
        expected_statement = 'Serial.print(((5 + 33) - (4 * 4)));\n   '
        self.assertEqual(expected_statement, vars.function_def)

    def test_operations_parentheses_2(self):
        self.translate_string('print(5 + (33 - 4) * 4)')
        expected_statement = 'Serial.print((5 + ((33 - 4) * 4)));\n   '
        self.assertEqual(expected_statement, vars.function_def)

    def test_operations_parentheses_3(self):
        self.translate_string('print((5 + 33 - 4) * 4)')
        expected_statement = 'Serial.print((((5 + 33) - 4) * 4));\n   '
        self.assertEqual(expected_statement, vars.function_def)

    def test_operations_parentheses_4(self):
        self.translate_string('print((5 + 33) - 4 * 4)')
        expected_statement = 'Serial.print(((5 + 33) - (4 * 4)));\n   '
        self.assertEqual(expected_statement, vars.function_def)

    def test_operations_parentheses_5(self):
        self.translate_string('print(5 + (33 - 4 * 4))')
        expected_statement = 'Serial.print((5 + (33 - (4 * 4))));\n   '
        self.assertEqual(expected_statement, vars.function_def)

    def test_operations_parentheses_6(self):
        self.translate_string('print(5 + 33 - (4 * 4))')
        expected_statement = 'Serial.print(((5 + 33) - (4 * 4)));\n   '
        self.assertEqual(expected_statement, vars.function_def)

    def test_operations_parentheses_7(self):
        self.translate_string('print(5 - 3 / 5)')
        expected_statement = 'Serial.print((5 - (3 / 5)));\n   '
        self.assertEqual(expected_statement, vars.function_def)

    def test_operations_parentheses_8(self):
        self.translate_string('print(5 * 3)')
        expected_statement = 'Serial.print((5 * 3));\n   '
        self.assertEqual(expected_statement, vars.function_def)

    def test_operations_parentheses_9(self):
        self.translate_string('print(5 / 3)')
        expected_statement = '''Serial.print((5 / 3));\n   '''
        self.assertEqual(expected_statement, vars.function_def)

    def test_operations_parentheses_10(self):
        self.translate_string('print(5 % 3)')
        expected_statement = 'Serial.print((5 % 3));\n   '
        self.assertEqual(expected_statement, vars.function_def)

    def test_string_array_declaration(self):
        self.translate_string('array = [\'hello\', \'bye\']')
        expected_statement = 'String array[] = {"hello","bye"};\n'
        self.assertEqual(expected_statement, vars.function_def)

    def test_boolean_array_declaration(self):
        self.translate_string('array = [True, False, True]')
        expected_statement = 'boolean array[] = {true,false,true};\n'
        self.assertEqual(expected_statement, vars.function_def)

    def test_float_array_declaration(self):
        self.translate_string('array = [2.2, 3.4]')
        expected_statement = 'float array[] = {2.2,3.4};\n'
        self.assertEqual(expected_statement, vars.function_def)

    def test_integer_array_declaration(self):
        self.translate_string('array = [1,2,3,4]')
        expected_statement = 'int array[] = {1,2,3,4};\n'
        self.assertEqual(expected_statement, vars.function_def)

    def test_print_string_array_index_0(self):
        self.translate_string('print(array[0])')
        expected_statement = 'Serial.print(array[0]);\n   '
        self.assertEqual(expected_statement, vars.function_def)

    def test_for_print_array(self):
        self.translate_string('''for x in array:
        print(x)''')
        expected_statement =  '''for(int x = 0; sizeof(array); x++) {\nSerial.print(x);\n   }\n'''
        '''
        for(int  = 0; sizeof(); x++) {
            Serial.print(x);
       }
        '''
        self.assertEqual(expected_statement, vars.function_def)

    def test_function_def_print_strings(self):
        self.translate_string('''def print_name_surname(name: str, surname: str, second: str, another, thrid: int):
    print(name + surname + second + another)''')
        expected_statement = '''void print_name_surname(DynType name, DynType surname, DynType second, DynType another, DynType thrid) {
Serial.print((((name + surname) + second) + another));
   }
'''
        self.assertEqual(expected_statement, vars.function_def)

    def test_function_call(self):
        self.translate_string('print_name_surname(\'Name\', \'Surname\', \'Surname\', 2, array, array)')
        expected_statement = '''DynType var0;var0.tvar = STR;String har0 = "Name";har0.toCharArray(var0.data, MinTypeSz);
DynType var1;var1.tvar = STR;String har1 = "Surname";har1.toCharArray(var1.data, MinTypeSz);
DynType var2;var2.tvar = STR;String har2 = "Surname";har2.toCharArray(var2.data, MinTypeSz);
DynType var3;var3.tvar = INT;String har3 = "2";har3.toCharArray(var3.data, MinTypeSz);
print_name_surname(var0,var1,var2,var3,array,array);
   '''
        self.assertEqual(expected_statement, vars.function_def)

    def test_if_true_else_if_else_statement(self):
        self.translate_string('''if True:
    print('HELLO')
elif halduino.getUS() <= 10:
    set_engine(0)
else:
    set_engine(1)''')
        expected_statement = '''if (true) {
DynType var0;var0.tvar = STR;String har0 = "HELLO";har0.toCharArray(var0.data, MinTypeSz);
Serial.print(var0.data);
   } else if ((getUS() <= 10)) {
DynType var1;var1.tvar = INT;String har1 = "0";har1.toCharArray(var1.data, MinTypeSz);
set_engine(var1);
   } else {
DynType var2;var2.tvar = INT;String har2 = "1";har2.toCharArray(var2.data, MinTypeSz);
set_engine(var2);
   }
'''
        self.assertEqual(expected_statement, vars.function_def)

    def test_and_or_if(self):
        self.translate_string('''def loop():
    array = [True, False, True]
    if True and False:
        print('Hello')
    if array[0] and array[1]:
        print('Hello')''')
        expected_statement = '''void loop() {
boolean array[] = {true,false,true};
if (true && false) {
DynType var0;var0.tvar = STR;String har0 = "Hello";har0.toCharArray(var0.data, MinTypeSz);
Serial.print(var0.data);
   }
if (array[0] && array[1]) {
DynType var1;var1.tvar = STR;String har1 = "Hello";har1.toCharArray(var1.data, MinTypeSz);
Serial.print(var1.data);
   }
}
'''
        self.assertEqual(expected_statement, vars.function_def)
