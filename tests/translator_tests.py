import ast
import unittest
import translator.Translator as translator

class TranslatorTests(unittest.TestCase):
    def setUp(self):
        global visitor
        translator.function_def = ''
        translator.robot = 'Complubot'
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
        expected_statement = 'Serial.print((5 / 3));\n   '
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
        self.assertEqual(expected_statement, translator.function_def)

    def test_function_def_print_strings(self):
        self.translate_string('''def print_name_surname(name: str, surname: str, second: str, another, thrid: int):
    print(name + surname + second + another)''')
        expected_statement = '''void print_name_surname(String name, String surname, String second, int another, int thrid) {
Serial.print((((name + surname) + second) + another));
   }
'''
        self.assertEqual(expected_statement, translator.function_def)

    def test_function_call(self):
        self.translate_string('print_name_surname(\'Name\', \'Surname\', \'Surname\', 2, array, array)')
        expected_statement = 'print_name_surname("Name","Surname","Surname",2,array,array);\n   '
        self.assertEqual(expected_statement, translator.function_def)

    def test_if_true_else_if_else_statement(self):
        self.translate_string('''if True:
    print('HELLO')
elif halduino.getUS() <= 10:
    set_engine(0)
else:
    set_engine(1)''')
        expected_statement = ''
        function_def = translator.function_def
        self.assertEqual(expected_statement, translator.function_def)
