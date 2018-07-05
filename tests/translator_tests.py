import ast
import unittest
import translator.Translator as translator

class MyTest(unittest.TestCase):
    def test_print_hello_world(self):
        translator.function_def = ''
        visitor = translator.MyVisitor()
        parsed_statement = ast.parse('print(\'Hello World!\')')
        visitor.visit(parsed_statement)
        expected_statement = 'Serial.print("Hello World!");\n   '
        self.assertEqual(expected_statement, translator.function_def)

    def test_sleep(self):
        translator.function_def = ''
        visitor = translator.MyVisitor()
        parsed_statement = ast.parse('sleep(100)')
        visitor.visit(parsed_statement)
        expected_statement = 'delay(100);\n   '
        self.assertEqual(expected_statement, translator.function_def)