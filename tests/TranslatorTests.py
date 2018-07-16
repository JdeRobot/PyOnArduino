import ast
import unittest
import translator.Translator as translator

class TranslatorTests(unittest.TestCase):
    def setUp(self):
        global visitor
        translator.robot = 'Complubot'
        translator.function_def = ''
        translator.parentheses = 0
        translator.brackets = 0
        translator.functions = {}
        translator.has_else_part = False
        translator.direction = ''
        translator.is_call = False
        translator.is_call_parameter = False
        translator.call_index = 0
        translator.is_Comparision = False
        translator.is_var_declaration = False
        translator.is_array = False
        translator.array_index = 0
        translator.array_length = 0
        translator.variable_def = ''
        translator.is_for = False
        translator.for_index = 0
        translator.is_if = False
        translator.bool_op = []
        translator.bin_op = False
        translator.global_vars = ''
        translator.halduino_directory = '../HALduino/halduino'
        translator.is_variable = False
        translator.call_def = ''
        translator.variables_counter = 0
        translator.is_built_in_func = False
        translator.var_sign = ''
        visitor = translator.MyVisitor()

    def translate_string(self, text):
        parsed_statement = ast.parse(text)
        visitor.visit(parsed_statement)
        return parsed_statement

    def test_print_hello_world(self):
        self.translate_string('print(\'Hello World!\')')
        expected_statement = 'Serial.print("Hello World!");\n   '
        self.assertEqual(expected_statement, translator.function_def)

    def test_sleep(self):
        self.translate_string('sleep(100)')
        expected_statement = 'delay(100);\n   '
        self.assertEqual(expected_statement, translator.function_def)

    def test_boolean_true_var_declaration(self):
        self.translate_string('var = True')
        expected_statement = 'boolean var = true;\n'
        self.assertEqual(expected_statement, translator.function_def)

    def test_boolean_false_var_declaration(self):
        self.translate_string('var = False')
        expected_statement = 'boolean var = false;\n'
        self.assertEqual(expected_statement, translator.function_def)

    def test_integer_var_declaration(self):
        self.translate_string('var = 9')
        expected_statement = 'int var = 9;\n'
        self.assertEqual(expected_statement, translator.function_def)

    def test_float_var_declaration(self):
        self.translate_string('var = 0.1')
        expected_statement = 'float var = 0.1;\n'
        self.assertEqual(expected_statement, translator.function_def)

    def test_char_var_declaration(self):
        self.translate_string('var = \'a\'')
        expected_statement = 'char var = \'a\';\n'
        self.assertEqual(expected_statement, translator.function_def)

    def test_string_var_declaration(self):
        self.translate_string('var = \'Hello World\'')
        expected_statement = 'String var = "Hello World";\n'
        self.assertEqual(expected_statement, translator.function_def)

    def test_operations_parentheses_1(self):
        self.translate_string('print(5 + 33 - 4 * 4)')
        expected_statement = 'Serial.print(((5 + 33) - (4 * 4)));\n   '
        self.assertEqual(expected_statement, translator.function_def)

    def test_operations_parentheses_2(self):
        self.translate_string('print(5 + (33 - 4) * 4)')
        expected_statement = 'Serial.print((5 + ((33 - 4) * 4)));\n   '
        self.assertEqual(expected_statement, translator.function_def)

    def test_operations_parentheses_3(self):
        self.translate_string('print((5 + 33 - 4) * 4)')
        expected_statement = 'Serial.print((((5 + 33) - 4) * 4));\n   '
        self.assertEqual(expected_statement, translator.function_def)

    def test_operations_parentheses_4(self):
        self.translate_string('print((5 + 33) - 4 * 4)')
        expected_statement = 'Serial.print(((5 + 33) - (4 * 4)));\n   '
        self.assertEqual(expected_statement, translator.function_def)

    def test_operations_parentheses_5(self):
        self.translate_string('print(5 + (33 - 4 * 4))')
        expected_statement = 'Serial.print((5 + (33 - (4 * 4))));\n   '
        self.assertEqual(expected_statement, translator.function_def)

    def test_operations_parentheses_6(self):
        self.translate_string('print(5 + 33 - (4 * 4))')
        expected_statement = 'Serial.print(((5 + 33) - (4 * 4)));\n   '
        self.assertEqual(expected_statement, translator.function_def)

    def test_operations_parentheses_7(self):
        self.translate_string('print(5 - 3 / 5)')
        expected_statement = 'Serial.print((5 - (3 / 5)));\n   '
        self.assertEqual(expected_statement, translator.function_def)

    def test_operations_parentheses_8(self):
        self.translate_string('print(5 * 3)')
        expected_statement = 'Serial.print((5 * 3));\n   '
        self.assertEqual(expected_statement, translator.function_def)

    def test_operations_parentheses_9(self):
        self.translate_string('print(5 / 3)')
        expected_statement = '''Serial.print((5 / 3));\n   '''
        self.assertEqual(expected_statement, translator.function_def)

    def test_operations_parentheses_10(self):
        self.translate_string('print(5 % 3)')
        expected_statement = 'Serial.print((5 % 3));\n   '
        self.assertEqual(expected_statement, translator.function_def)

    def test_string_array_declaration(self):
        self.translate_string('array = [\'hello\', \'bye\']')
        expected_statement = 'String array[] = {"hello","bye"};\n'
        self.assertEqual(expected_statement, translator.function_def)

    def test_boolean_array_declaration(self):
        self.translate_string('array = [True, False, True]')
        expected_statement = 'boolean array[] = {true,false,true};\n'
        self.assertEqual(expected_statement, translator.function_def)

    def test_float_array_declaration(self):
        self.translate_string('array = [2.2, 3.4]')
        expected_statement = 'float array[] = {2.2,3.4};\n'
        self.assertEqual(expected_statement, translator.function_def)

    def test_integer_array_declaration(self):
        self.translate_string('array = [1,2,3,4]')
        expected_statement = 'int array[] = {1,2,3,4};\n'
        self.assertEqual(expected_statement, translator.function_def)

    def test_print_string_array_index_0(self):
        self.translate_string('print(array[0])')
        expected_statement = 'Serial.print(array[0]);\n   '
        self.assertEqual(expected_statement, translator.function_def)

    def test_for_print_array(self):
        self.translate_string('''for x in array:
        print(x)''')
        expected_statement =  '''for(int x = 0; sizeof(array); x++) {\nSerial.print(x);\n   }\n'''
        '''
        for(int  = 0; sizeof(); x++) {
            Serial.print(x);
       }
        '''
        self.assertEqual(expected_statement, translator.function_def)

    def test_function_def_print_strings(self):
        self.translate_string('''def print_name_surname(name: str, surname: str, second: str, another, thrid: int):
    print(name + surname + second + another)''')
        expected_statement = '''void print_name_surname(DynType name, DynType surname, DynType second, DynType another, DynType thrid) {
Serial.print((((name + surname) + second) + another));
   }
'''
        self.assertEqual(expected_statement, translator.function_def)

    def test_function_call(self):
        self.translate_string('print_name_surname(\'Name\', \'Surname\', \'Surname\', 2, array, array)')
        expected_statement = '''DynType var0;var0.tvar = INT;String har0 = "2";har0.toCharArray(var0.data, MinTypeSz);
print_name_surname("Name","Surname","Surname",var0,array,array);
   '''
        self.assertEqual(expected_statement, translator.function_def)

    def test_if_true_else_if_else_statement(self):
        self.translate_string('''if True:
    print('HELLO')
elif halduino.getUS() <= 10:
    set_engine(0)
else:
    set_engine(1)''')
        expected_statement = '''if (true) {
Serial.print("HELLO");
   } else if ((getUS() <= 10)) {
DynType var0;var0.tvar = INT;String har0 = "0";har0.toCharArray(var0.data, MinTypeSz);
set_engine(var0);
   } else {
DynType var1;var1.tvar = INT;String har1 = "1";har1.toCharArray(var1.data, MinTypeSz);
set_engine(var1);
   }
'''
        self.assertEqual(expected_statement, translator.function_def)

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
Serial.print("Hello");
   }
if (array[0] && array[1]) {
Serial.print("Hello");
   }
}
'''
        self.assertEqual(expected_statement, translator.function_def)
