import ast
import unittest
import translator.Translator as translator

class TranslatorTests(unittest.TestCase):
    def setUp(self):
        global visitor
        translator.function_def = ''
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